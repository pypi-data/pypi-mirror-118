import logging
from abc import ABCMeta, abstractmethod

import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

from abcpy.acceptedparametersmanager import *
from abcpy.graphtools import GraphTools
# import dataset and networks definition:
from abcpy.statistics import LinearTransformation
from abcpy.transformers import BoundedVarScaler

# Different torch components
try:
    import torch
except ImportError:
    has_torch = False
else:
    has_torch = True
    from abcpy.NN_utilities.networks import createDefaultNN, ScalerAndNet, createDefaultNNWithDerivatives, \
        DiscardLastOutputNet
    from abcpy.statistics import NeuralEmbedding
    from torch.optim import Adam, lr_scheduler
    import torch.autograd as autograd
    from abcpy.NN_utilities.utilities import jacobian_second_order, set_requires_grad
    from abcpy.NN_utilities.losses import Fisher_divergence_loss_with_c_x

from abcpy.NN_utilities.algorithms import FP_nn_training, triplet_training, contrastive_training
from abcpy.NN_utilities.utilities import compute_similarity_matrix


# TODO: there seems to be issue when n_samples_per_param >1. Check that. Should you modify the _sample_parameters-statistics function?

class StatisticsLearning(metaclass=ABCMeta):
    """This abstract base class defines a way to choose the summary statistics.
    """

    def __init__(self, model, statistics_calc, backend, n_samples=1000, n_samples_val=0, n_samples_per_param=1,
                 parameters=None, simulations=None, parameters_val=None, simulations_val=None, seed=None):

        """The constructor of a sub-class must accept a non-optional model, statistics calculator and
        backend which are stored to self.model, self.statistics_calc and self.backend. Further it
        accepts two optional parameters n_samples and seed defining the number of simulated dataset
        used for the pilot to decide the summary statistics and the integer to initialize the random
        number generator.

        This __init__ takes care of sample-statistics generation, with the parallelization; however, you can choose
        to provide simulations and corresponding parameters that have been previously generated, with the parameters
        `parameters` and `simulations`.

        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_calc: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set.
            These are transformed by the `statistics_calc` statistics before the learning step is done. Default
            value is None.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        """
        if (parameters is None) != (simulations is None):
            raise RuntimeError("parameters and simulations need to be provided together.")

        if (parameters_val is None) != (simulations_val is None):
            raise RuntimeError("parameters_val and simulations_val need to be provided together.")

        self.model = model
        self.statistics_calc = statistics_calc
        self.backend = backend
        self.rng = np.random.RandomState(seed)
        self.n_samples_per_param = n_samples_per_param
        self.logger = logging.getLogger(__name__)

        n_samples_to_generate = n_samples * (parameters is None) + n_samples_val * (parameters_val is None)

        if n_samples_to_generate > 0:  # need to generate some data
            self.logger.info('Generation of data...')

            self.logger.debug("Definitions for parallelization.")
            # An object managing the bds objects
            self.accepted_parameters_manager = AcceptedParametersManager(self.model)
            self.accepted_parameters_manager.broadcast(self.backend, [])

            self.logger.debug("Map phase.")
            # main algorithm
            seed_arr = self.rng.randint(1, n_samples_to_generate * n_samples_to_generate, size=n_samples_to_generate,
                                        dtype=np.int32)
            rng_arr = np.array([np.random.RandomState(seed) for seed in seed_arr])
            rng_pds = self.backend.parallelize(rng_arr)

            self.logger.debug("Collect phase.")
            sample_parameters_statistics_pds = self.backend.map(self._sample_parameter_statistics, rng_pds)

            sample_parameters_and_statistics = self.backend.collect(sample_parameters_statistics_pds)
            sample_parameters, sample_statistics = [list(t) for t in zip(*sample_parameters_and_statistics)]
            sample_parameters = np.array(sample_parameters)
            self.sample_statistics = np.concatenate(sample_statistics)

            self.logger.debug("Reshape data")
            # reshape the sample parameters; so that we can also work with multidimensional parameters
            self.sample_parameters = sample_parameters.reshape((n_samples_to_generate, -1))

            # now reshape the statistics in the case in which several n_samples_per_param > 1, and repeat the array with
            # the parameters so that the regression algorithms can work on the pair of arrays. Maybe there are smarter
            # ways of doing this.

            sample_statistics_generated = self.sample_statistics.reshape(
                n_samples_to_generate * self.n_samples_per_param, -1)
            sample_parameters_generated = np.repeat(self.sample_parameters, self.n_samples_per_param, axis=0)
            # now split between train and validation set:
            self.sample_statistics = sample_statistics_generated[
                                     0: n_samples * self.n_samples_per_param * (parameters is None)]
            self.sample_parameters = sample_parameters_generated[
                                     0: n_samples * self.n_samples_per_param * (parameters is None)]

            self.sample_statistics_val = sample_statistics_generated[
                                         n_samples * self.n_samples_per_param * (parameters is None):len(
                                             sample_statistics_generated)]
            self.sample_parameters_val = sample_parameters_generated[
                                         n_samples * self.n_samples_per_param * (parameters is None):len(
                                             sample_parameters_generated)]

            self.logger.info('Data generation finished.')

        if parameters is not None:
            # do all the checks on dimensions:
            if not isinstance(parameters, np.ndarray) or not isinstance(simulations, np.ndarray):
                raise TypeError("parameters and simulations need to be numpy arrays.")
            if len(parameters.shape) != 2:
                raise RuntimeError("parameters have to be a 2-dimensional array")
            if len(simulations.shape) != 2:
                raise RuntimeError("simulations have to be a 2-dimensional array")
            if simulations.shape[0] != parameters.shape[0]:
                raise RuntimeError("parameters and simulations need to have the same first dimension")

            # if all checks are passed:
            self.sample_statistics = self.statistics_calc.statistics(
                [simulations[i] for i in range(simulations.shape[0])])
            self.sample_parameters = parameters

            self.logger.info("The statistics will be learned using the provided data and parameters")

        if parameters_val is not None:
            # do all the checks on dimensions:
            if not isinstance(parameters_val, np.ndarray) or not isinstance(simulations_val, np.ndarray):
                raise TypeError("parameters_val and simulations_val need to be numpy arrays.")
            if len(parameters_val.shape) != 2:
                raise RuntimeError("parameters_val have to be a 2-dimensional array")
            if len(simulations_val.shape) != 2:
                raise RuntimeError("simulations_val have to be a 2-dimensional array")
            if simulations_val.shape[0] != parameters_val.shape[0]:
                raise RuntimeError("parameters_val and simulations_val need to have the same first dimension")

            # if all checks are passed:
            self.sample_statistics_val = self.statistics_calc.statistics(
                [simulations_val[i] for i in range(simulations_val.shape[0])])
            self.sample_parameters_val = parameters_val

            self.logger.info("The provided validation data and parameters will be used as a validation set.")

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['backend']
        return state

    @abstractmethod
    def get_statistics(self):
        """
        This should return a statistics object that implements the learned transformation.

        Returns
        -------
        abcpy.statistics.Statistics object
            a statistics object that implements the learned transformation.
        """
        raise NotImplementedError

    def _sample_parameter_statistics(self, rng=np.random.RandomState()):
        """Function that generates (parameter, statistics). It is mapped to the different workers during data
        generation.
        """
        self.sample_from_prior(rng=rng)
        parameter = self.get_parameters()
        y_sim = self.simulate(self.n_samples_per_param, rng=rng)
        if y_sim is not None:
            statistics = self.statistics_calc.statistics(y_sim)
        return parameter, statistics


class StatisticsLearningWithLosses(StatisticsLearning, metaclass=ABCMeta):
    """This abstract base class subclasses the above and includes a utility method to plot losses.
    """

    def plot_losses(self, which_losses="both"):
        """
        Plot losses vs training epochs after the NN have been trained.

        Parameters
        ----------
        which_losses: string, optional
            Specifies which set of losses to display (between training and test loss).
            Can be 'train', 'test' or 'both'. Notice that the test loss could be unavailable (in case no test set was
            used for training), in which case the test loss is not shown even if requested. Defaults to 'both'.

        Returns
        -------

        """

        if which_losses not in ["both", "train", "test"]:
            raise NotImplementedError("'which_losses' should be 'both', 'train' or 'test'")

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
        if which_losses in ["both", "train"]:
            ax.plot(np.arange(len(self.train_losses)) + 1, self.train_losses, label="Train loss", color="C0")
        if which_losses in ["both", "test"]:
            if self.test_losses is not None:
                if len(self.test_losses) != len(self.train_losses):
                    raise RuntimeError("Length of train and test losses list should be the same.")
                ax.plot(np.arange(len(self.train_losses)) + 1, self.test_losses, label="Test loss", color="C1")
            else:
                self.logger.warning("You requested to plot test losses, but these are unavailable (probably due to no "
                                    "test set been used during NN training.")

        ax.set_xlabel("Training epoch")
        ax.set_ylabel("Loss")
        ax.legend()

        return fig, ax


class Semiautomatic(StatisticsLearning, GraphTools):
    """This class implements the semi automatic summary statistics learning technique described in Fearnhead and
    Prangle [1].

    [1] Fearnhead P., Prangle D. 2012. Constructing summary statistics for approximate
    Bayesian computation: semi-automatic approximate Bayesian computation. J. Roy. Stat. Soc. B 74:419–474.
    """

    def __init__(self, model, statistics_calc, backend, n_samples=1000, n_samples_per_param=1, parameters=None,
                 simulations=None, seed=None):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_calc: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class, applied before learning the transformation.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed. These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        """
        # the sampling is performed by the init of the parent class
        super(Semiautomatic, self).__init__(model, statistics_calc, backend,
                                            n_samples, n_samples_per_param=n_samples_per_param, parameters=parameters,
                                            simulations=simulations, seed=seed)

        self.logger.info('Learning of the transformation...')

        self.coefficients_learnt = np.zeros(shape=(self.sample_parameters.shape[1], self.sample_statistics.shape[1]))
        regr = linear_model.LinearRegression(fit_intercept=True)
        for ind in range(self.sample_parameters.shape[1]):
            regr.fit(self.sample_statistics, self.sample_parameters[:, ind])
            self.coefficients_learnt[ind, :] = regr.coef_

        self.logger.info("Finished learning the transformation.")

    def get_statistics(self):
        """
        Returns an abcpy.statistics.LinearTransformation Statistics implementing the learned transformation.

        Returns
        -------
        abcpy.statistics.LinearTransformation object
            a statistics object that implements the learned transformation.
        """
        return LinearTransformation(np.transpose(self.coefficients_learnt), previous_statistics=self.statistics_calc)


class StatisticsLearningNN(StatisticsLearningWithLosses, GraphTools):
    """This is the base class for all the statistics learning techniques involving neural networks. In most cases, you
    should not instantiate this directly. The actual classes instantiate this with the right arguments.

    In order to use this technique, Pytorch is required to handle the neural networks. However, the user does not need
    to be fluent in Pytorch as some default neural networks are instantiated if the user does not provide them
    (experienced users can of course provide the neural networks they would like to use). GPUs can be used to
    train the neural networks if required.
    """

    def __init__(self, model, statistics_calc, backend, training_routine, distance_learning, embedding_net=None,
                 n_samples=1000, n_samples_val=0, n_samples_per_param=1, parameters=None, simulations=None,
                 parameters_val=None, simulations_val=None, seed=None, cuda=None, scale_samples=True, quantile=0.1,
                 use_tqdm=True, **training_routine_kwargs):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_calc: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class, applied before learning the transformation.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        training_routine: function
            training routine to train the network. It has to take as first and second arguments the matrix of
            simulations and the corresponding targets (or the similarity matrix if `distance_learning` is True). It also
            needs to have as keyword parameters embedding_net and cuda.
        distance_learning: boolean
            this has to be True if the statistics learning technique is based on distance learning, in which case the
            __init__ computes the similarity matrix.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output 
            (after being transformed by `statistics_calc`), alternatively, a list
            with integer numbers denoting the width of the hidden layers, from which a fully connected network with
            that structure is created, having the input and output size corresponding to size of model output
            (after being transformed by `statistics_calc`) and
            number of parameters. In case this is None, a fully connected neural network with three hidden layers is
            used; the width of the hidden layers is given by
            ``[int(input_size * 1.5), int(input_size * 0.75 + output_size * 3), int(output_size * 5)]``,
            where `input_size` is the size of the data after being transformed by `statistics_calc`, while `output_size`
            is the number of parameters in the model. For further details check
            :func:`abcpy.NN_utilities.networks.createDefaultNN`
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. 
             These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set. Default
            value is None.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            the network will be wrapped by :class:`abcpy.NN_utilities.networks.ScalerAndNet`; this automatically
            takes care of transforming the data with the scaler before applying the neural network.
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        quantile: float, optional
            quantile used to define the similarity set if distance_learning is True. Default to 0.1.
        use_tqdm : boolean, optional
            Whether using tqdm or not to display progress. Defaults to True.
        training_routine_kwargs:
            additional kwargs to be passed to the underlying training routine.
        """
        self.logger = logging.getLogger(__name__)
        self.scale_samples = scale_samples

        # Define device
        if not has_torch:
            raise ImportError(
                "Pytorch is required to instantiate an element of the {} class, in order to handle "
                "neural networks. Please install it. ".format(self.__class__.__name__))

        # set random seed for torch as well:
        if seed is not None:
            torch.manual_seed(seed)

        if cuda is None:
            cuda = torch.cuda.is_available()
        elif cuda and not torch.cuda.is_available():
            # if the user requested to use GPU but no GPU is there
            cuda = False
            self.logger.warning(
                "You requested to use GPU but no GPU is available! The computation will proceed on CPU.")

        self.device = "cuda" if cuda and torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            self.logger.debug("We are using GPU to train the network.")
        else:
            self.logger.debug("We are using CPU to train the network.")

        # this handles generation of the data (or its formatting in case the data is provided to the Semiautomatic
        # class)
        super(StatisticsLearningNN, self).__init__(model, statistics_calc, backend, n_samples, n_samples_val,
                                                   n_samples_per_param, parameters, simulations, seed=seed,
                                                   parameters_val=parameters_val, simulations_val=simulations_val)

        # we have a validation set if it has the following attribute with size larger than 0
        has_val_set = hasattr(self, "sample_parameters_val") and len(self.sample_parameters_val) > 0

        self.logger.info('Learning of the transformation...')
        # Define Data
        target, simulations = self.sample_parameters, self.sample_statistics
        if has_val_set:
            target_val, simulations_val = self.sample_parameters_val, self.sample_statistics_val
        else:
            target_val, simulations_val = None, None

        if distance_learning:
            self.logger.debug("Computing similarity matrix...")
            # define the similarity set
            similarity_set = compute_similarity_matrix(target, quantile)
            if has_val_set:
                similarity_set_val = compute_similarity_matrix(target_val, quantile)
            else:
                similarity_set_val = None
            self.logger.debug("Done")

        # set up the scaler and transform the data:
        if self.scale_samples:
            self.scaler = MinMaxScaler().fit(simulations)
            simulations = self.scaler.transform(simulations)
            if has_val_set:
                simulations_val = self.scaler.transform(simulations_val)

        # now setup the default neural network or not

        if isinstance(embedding_net, torch.nn.Module):
            self.embedding_net = embedding_net
            self.logger.debug('We use the provided neural network')

        elif isinstance(embedding_net, list) or embedding_net is None:
            # therefore we need to generate the neural network given the list. The following function returns a class
            # of NN with given input size, output size and hidden sizes; then, need () to instantiate the network
            self.embedding_net = createDefaultNN(input_size=simulations.shape[1], output_size=target.shape[1],
                                                 hidden_sizes=embedding_net)()
            self.logger.debug('We generate a default neural network')
        else:
            raise RuntimeError("'embedding_net' needs to be either a torch.nn.Module, or a list, or None.")

        if cuda:
            self.embedding_net.cuda()

        self.logger.debug('We now run the training routine')

        if distance_learning:
            self.embedding_net, self.train_losses, self.test_losses = training_routine(
                simulations, similarity_set, embedding_net=self.embedding_net, cuda=cuda, samples_val=simulations_val,
                use_tqdm=use_tqdm, similarity_set_val=similarity_set_val, **training_routine_kwargs)
        else:
            self.embedding_net, self.train_losses, self.test_losses = training_routine(
                simulations, target, embedding_net=self.embedding_net, cuda=cuda, samples_val=simulations_val,
                target_val=target_val, use_tqdm=use_tqdm, **training_routine_kwargs)

        self.logger.info("Finished learning the transformation.")

        self.embedding_net.cpu()  # move back the net to CPU.

    def get_statistics(self):
        """
        Returns a :class:`abcpy.statistics.NeuralEmbedding` Statistics implementing the learned transformation.

        If a scaler was used, the `net` attribute of the returned object is of the class
        :class:`abcpy.NN_utilities.networks.ScalerAndNet`, which is a nn.Module object wrapping the scaler and the
        learned neural network and applies the scaler before the data is fed through the neural network.

        Returns
        -------
        abcpy.statistics.NeuralEmbedding object
            a statistics object that implements the learned transformation.
        """
        if self.scale_samples:
            return NeuralEmbedding(net=ScalerAndNet(self.embedding_net, self.scaler),
                                   previous_statistics=self.statistics_calc)
        else:
            return NeuralEmbedding(net=self.embedding_net, previous_statistics=self.statistics_calc)


# the following three classes subclass the base class StatisticsLearningNN with different training routines

class SemiautomaticNN(StatisticsLearningNN):
    """This class implements the semi automatic summary statistics learning technique as described in
     Jiang et al. 2017 [1].

     In order to use this technique, Pytorch is required to handle the neural networks. However, the user does not need
     to be fluent in Pytorch as some default neural networks are instantiated if the user does not provide them
     (experienced users can of course provide the neural networks they would like to use). GPUs can be used to
     train the neural networks if required.

     [1] Jiang, B., Wu, T.Y., Zheng, C. and Wong, W.H., 2017. Learning summary statistic for approximate Bayesian
     computation via deep neural network. Statistica Sinica, pp.1595-1618.
    """

    def __init__(self, model, statistics_calc, backend, embedding_net=None, n_samples=1000, n_samples_val=0,
                 n_samples_per_param=1, parameters=None, simulations=None, parameters_val=None, simulations_val=None,
                 early_stopping=False, epochs_early_stopping_interval=1, start_epoch_early_stopping=10,
                 seed=None, cuda=None, scale_samples=True, batch_size=16, n_epochs=200, load_all_data_GPU=False,
                 lr=1e-3, optimizer=None, scheduler=None, start_epoch_training=0, use_tqdm=True,
                 optimizer_kwargs={}, scheduler_kwargs={}, loader_kwargs={}):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_calc: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class, applied before learning the transformation.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output
            (after being transformed by `statistics_calc`), alternatively, a list
            with integer numbers denoting the width of the hidden layers, from which a fully connected network with
            that structure is created, having the input and output size corresponding to size of model output
            (after being transformed by `statistics_calc`) and
            number of parameters. In case this is None, a fully connected neural network with three hidden layers is
            used; the width of the hidden layers is given by
            ``[int(input_size * 1.5), int(input_size * 0.75 + output_size * 3), int(output_size * 5)]``,
            where `input_size` is the size of the data after being transformed by `statistics_calc`, while `output_size`
            is the number of parameters in the model. For further details check
            :func:`abcpy.NN_utilities.networks.createDefaultNN`
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set.
             These are transformed by the `statistics_calc` statistics before the learning step is done.
            Default value is None.
        early_stopping: boolean, optional
            If True, the validation set (which needs to be either provided through the arguments `parameters_val` and
            `simulations_val` or generated by setting `n_samples_val` to a value larger than 0) is used to early stop
            the training of the neural network as soon as the loss on the validation set starts to increase. Default
            value is False.
        epochs_early_stopping_interval: integer, optional
            The frequency at which the validation error is compared in order to decide whether to early stop the
            training or not. Namely, if `epochs_early_stopping_interval=10`, early stopping can happen only at epochs
            multiple of 10. Default value is 1.
        start_epoch_early_stopping: integer, optional
            The epoch after which early stopping can happen; in fact, as soon as training starts, there may be a 
            transient period in which the loss increases. Default value is 10.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            the network will be wrapped by :class:`abcpy.NN_utilities.networks.ScalerAndNet`; this automatically
            takes care of transforming the data with the scaler before applying the neural network.
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        batch_size: integer, optional
            the batch size used for training the neural network. Default is 16
        n_epochs: integer, optional
            the number of epochs used for training the neural network. Default is 200
        load_all_data_GPU: boolean, optional
            If True and if we a GPU is used, the whole dataset is loaded on the GPU before training begins; this may
            speed up training as it avoid transfer between CPU and GPU, but it is not guaranteed to do. Note that if the
            dataset is not small enough, setting this to True causes things to crash if the dataset is too large.
            Default to False, you should not rely too much on this.
        lr: float, optional
            The learning rate to be used in the iterative training scheme of the neural network. Default to 1e-3.
        optimizer: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`. Default to `Adam`. Additional parameters may be
            passed through the `optimizer_kwargs` parameter.
        scheduler: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs. By default, no scheduler is
            used. Additional parameters may be passed through the `scheduler_kwargs` parameter.
        start_epoch_training: integer, optional
            If a scheduler is provided, for the first `start_epoch_training` epochs the scheduler is applied to modify
            the learning rate without training the network. From then on, the training proceeds normally, applying both
            the scheduler and the optimizer at each epoch. Default to 0.
        use_tqdm : boolean, optional
            Whether using tqdm or not to display progress. Defaults to True.
        optimizer_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer.
        scheduler_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the scheduler.
        loader_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the loader (that handles loading the samples from the
            dataset during the training phase).
        """
        super(SemiautomaticNN, self).__init__(model, statistics_calc, backend, FP_nn_training, distance_learning=False,
                                              embedding_net=embedding_net, n_samples=n_samples,
                                              n_samples_val=n_samples_val, n_samples_per_param=n_samples_per_param,
                                              parameters=parameters, simulations=simulations,
                                              parameters_val=parameters_val, simulations_val=simulations_val,
                                              early_stopping=early_stopping,
                                              epochs_early_stopping_interval=epochs_early_stopping_interval,
                                              start_epoch_early_stopping=start_epoch_early_stopping,
                                              seed=seed, cuda=cuda, scale_samples=scale_samples, batch_size=batch_size,
                                              n_epochs=n_epochs, load_all_data_GPU=load_all_data_GPU, lr=lr,
                                              optimizer=optimizer, scheduler=scheduler,
                                              start_epoch_training=start_epoch_training, use_tqdm=use_tqdm,
                                              optimizer_kwargs=optimizer_kwargs,
                                              scheduler_kwargs=scheduler_kwargs, loader_kwargs=loader_kwargs)


class TripletDistanceLearning(StatisticsLearningNN):
    """This class implements the statistics learning technique by using the triplet loss [1] for distance learning as
     described in Pacchiardi et al. 2021 [2].

     In order to use this technique, Pytorch is required to handle the neural networks. However, the user does not need
     to be fluent in Pytorch as some default neural networks are instantiated if the user does not provide them
     (experienced users can of course provide the neural networks they would like to use). GPUs can be used to
     train the neural networks if required.

     [1] Schroff, F., Kalenichenko, D. and Philbin, J., 2015. Facenet: A unified embedding for face recognition and
     clustering. In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 815-823).

     [2] Pacchiardi, L., Kunzli, P., Schöngens, M., Chopard, B., and Dutta, R., 2021. Distance-learning for
     approximate bayesian computation to model a volcanic eruption. Sankhya B, 83(1), 288-317.
    """

    def __init__(self, model, statistics_calc, backend, embedding_net=None, n_samples=1000, n_samples_val=0,
                 n_samples_per_param=1, parameters=None, simulations=None, parameters_val=None, simulations_val=None,
                 early_stopping=False, epochs_early_stopping_interval=1, start_epoch_early_stopping=10, seed=None,
                 cuda=None, scale_samples=True,
                 quantile=0.1, batch_size=16, n_epochs=200, load_all_data_GPU=False, margin=1., lr=None, optimizer=None,
                 scheduler=None, start_epoch_training=0, use_tqdm=True, optimizer_kwargs={}, scheduler_kwargs={},
                 loader_kwargs={}):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_calc: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class, applied before learning the transformation.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output 
            (after being transformed by `statistics_calc`), alternatively, a list
            with integer numbers denoting the width of the hidden layers, from which a fully connected network with
            that structure is created, having the input and output size corresponding to size of model output
            (after being transformed by `statistics_calc`) and
            number of parameters. In case this is None, a fully connected neural network with three hidden layers is
            used; the width of the hidden layers is given by
            ``[int(input_size * 1.5), int(input_size * 0.75 + output_size * 3), int(output_size * 5)]``,
            where `input_size` is the size of the data after being transformed by `statistics_calc`, while `output_size`
            is the number of parameters in the model. For further details check
            :func:`abcpy.NN_utilities.networks.createDefaultNN`
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set.
             These are transformed by the `statistics_calc` statistics before the learning step is done. 
            Default value is None.
        early_stopping: boolean, optional
            If True, the validation set (which needs to be either provided through the arguments `parameters_val` and
            `simulations_val` or generated by setting `n_samples_val` to a value larger than 0) is used to early stop
            the training of the neural network as soon as the loss on the validation set starts to increase. Default
            value is False.
        epochs_early_stopping_interval: integer, optional
            The frequency at which the validation error is compared in order to decide whether to early stop the
            training or not. Namely, if `epochs_early_stopping_interval=10`, early stopping can happen only at epochs
            multiple of 10. Default value is 1.
        start_epoch_early_stopping: integer, optional
            The epoch after which early stopping can happen; in fact, as soon as training starts, there may be a 
            transient period in which the loss increases. Default value is 10.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            the network will be wrapped by :class:`abcpy.NN_utilities.networks.ScalerAndNet`; this automatically
            takes care of transforming the data with the scaler before applying the neural network.
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        quantile: float, optional
            quantile used to define the similarity set if distance_learning is True. Default to 0.1.
        batch_size: integer, optional
            the batch size used for training the neural network. Default is 16
        n_epochs: integer, optional
            the number of epochs used for training the neural network. Default is 200
        load_all_data_GPU: boolean, optional
            If True and if we a GPU is used, the whole dataset is loaded on the GPU before training begins; this may
            speed up training as it avoid transfer between CPU and GPU, but it is not guaranteed to do. Note that if the
            dataset is not small enough, setting this to True causes things to crash if the dataset is too large.
            Default to False, you should not rely too much on this.
        margin: float, optional
            margin defining the triplet loss. The larger it is, the further away dissimilar samples are pushed with
            respect to similar ones. Default to 1.
        lr: float, optional
            The learning rate to be used in the iterative training scheme of the neural network. Default to 1e-3.
        optimizer: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`. Default to `Adam`. Additional parameters may be
            passed through the `optimizer_kwargs` parameter.
        scheduler: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs. By default, no scheduler is
            used. Additional parameters may be passed through the `scheduler_kwargs` parameter.
        start_epoch_training: integer, optional
            If a scheduler is provided, for the first `start_epoch_training` epochs the scheduler is applied to modify
            the learning rate without training the network. From then on, the training proceeds normally, applying both
            the scheduler and the optimizer at each epoch. Default to 0.
        use_tqdm : boolean, optional
            Whether using tqdm or not to display progress. Defaults to True.
        optimizer_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer.
        scheduler_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the scheduler.
        loader_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the loader (that handles loading the samples from the
            dataset during the training phase).
        """

        super(TripletDistanceLearning, self).__init__(model, statistics_calc, backend, triplet_training,
                                                      distance_learning=True, embedding_net=embedding_net,
                                                      n_samples=n_samples, n_samples_val=n_samples_val,
                                                      n_samples_per_param=n_samples_per_param,
                                                      parameters=parameters, simulations=simulations,
                                                      parameters_val=parameters_val, simulations_val=simulations_val,
                                                      early_stopping=early_stopping,
                                                      epochs_early_stopping_interval=epochs_early_stopping_interval,
                                                      start_epoch_early_stopping=start_epoch_early_stopping,
                                                      seed=seed, cuda=cuda, scale_samples=scale_samples,
                                                      quantile=quantile, batch_size=batch_size,
                                                      n_epochs=n_epochs, load_all_data_GPU=load_all_data_GPU,
                                                      margin=margin, lr=lr, optimizer=optimizer, scheduler=scheduler,
                                                      use_tqdm=use_tqdm,
                                                      start_epoch_training=start_epoch_training,
                                                      optimizer_kwargs=optimizer_kwargs,
                                                      scheduler_kwargs=scheduler_kwargs, loader_kwargs=loader_kwargs)


class ContrastiveDistanceLearning(StatisticsLearningNN):
    """This class implements the statistics learning technique by using the contrastive loss [1] for distance learning
     as described in Pacchiardi et al. 2021 [2].

     In order to use this technique, Pytorch is required to handle the neural networks. However, the user does not need
     to be fluent in Pytorch as some default neural networks are instantiated if the user does not provide them
     (experienced users can of course provide the neural networks they would like to use). GPUs can be used to
     train the neural networks if required.

     [1] Hadsell, R., Chopra, S. and LeCun, Y., 2006, June. Dimensionality reduction by learning an invariant mapping.
     In 2006 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR'06) (Vol. 2,
     pp. 1735-1742). IEEE.

     [2] Pacchiardi, L., Kunzli, P., Schöngens, M., Chopard, B., and Dutta, R., 2021. Distance-learning for
     approximate bayesian computation to model a volcanic eruption. Sankhya B, 83(1), 288-317.
    """

    def __init__(self, model, statistics_calc, backend, embedding_net=None, n_samples=1000, n_samples_val=0,
                 n_samples_per_param=1, parameters=None, simulations=None, parameters_val=None, simulations_val=None,
                 early_stopping=False, epochs_early_stopping_interval=1, start_epoch_early_stopping=10, seed=None,
                 cuda=None, scale_samples=True, quantile=0.1, batch_size=16, n_epochs=200, positive_weight=None,
                 load_all_data_GPU=False, margin=1., lr=None, optimizer=None, scheduler=None,
                 start_epoch_training=0, use_tqdm=True, optimizer_kwargs={}, scheduler_kwargs={}, loader_kwargs={}):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_calc: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class, applied before learning the transformation.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output 
            (after being transformed by `statistics_calc`), alternatively, a list
            with integer numbers denoting the width of the hidden layers, from which a fully connected network with
            that structure is created, having the input and output size corresponding to size of model output
            (after being transformed by `statistics_calc`) and
            number of parameters. In case this is None, a fully connected neural network with three hidden layers is
            used; the width of the hidden layers is given by
            ``[int(input_size * 1.5), int(input_size * 0.75 + output_size * 3), int(output_size * 5)]``,
            where `input_size` is the size of the data after being transformed by `statistics_calc`, while `output_size`
            is the number of parameters in the model. For further details check
            :func:`abcpy.NN_utilities.networks.createDefaultNN`
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed. These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set.
             These are transformed by the `statistics_calc` statistics before the learning step is done. 
            Default value is None.
        early_stopping: boolean, optional
            If True, the validation set (which needs to be either provided through the arguments `parameters_val` and
            `simulations_val` or generated by setting `n_samples_val` to a value larger than 0) is used to early stop
            the training of the neural network as soon as the loss on the validation set starts to increase. Default
            value is False.
        epochs_early_stopping_interval: integer, optional
            The frequency at which the validation error is compared in order to decide whether to early stop the
            training or not. Namely, if `epochs_early_stopping_interval=10`, early stopping can happen only at epochs
            multiple of 10. Default value is 1.
        start_epoch_early_stopping: integer, optional
            The epoch after which early stopping can happen; in fact, as soon as training starts, there may be a 
            transient period in which the loss increases. Default value is 10.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            the network will be wrapped by :class:`abcpy.NN_utilities.networks.ScalerAndNet`; this automatically
            takes care of transforming the data with the scaler before applying the neural network.
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        quantile: float, optional
            quantile used to define the similarity set if distance_learning is True. Default to 0.1.
        batch_size: integer, optional
            the batch size used for training the neural network. Default is 16
        n_epochs: integer, optional
            the number of epochs used for training the neural network. Default is 200
        positive_weight: float, optional
            The contrastive loss samples pairs of elements at random, and if the majority of samples are labelled as
            dissimilar, the probability of considering similar pairs is small. Then, you can set this value to a number
            between 0 and 1 in order to sample positive pairs with that probability during training.
        load_all_data_GPU: boolean, optional
            If True and if we a GPU is used, the whole dataset is loaded on the GPU before training begins; this may
            speed up training as it avoid transfer between CPU and GPU, but it is not guaranteed to do. Note that if the
            dataset is not small enough, setting this to True causes things to crash if the dataset is too large.
            Default to False, you should not rely too much on this.
        margin: float, optional
            margin defining the contrastive loss. The larger it is, the further away dissimilar samples are pushed with
            respect to similar ones. Default to 1.
        lr: float, optional
            The learning rate to be used in the iterative training scheme of the neural network. Default to 1e-3.
        optimizer: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`. Default to `Adam`. Additional parameters may be
            passed through the `optimizer_kwargs` parameter.
        scheduler: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs. By default, no scheduler is
            used. Additional parameters may be passed through the `scheduler_kwargs` parameter.
        start_epoch_training: integer, optional
            If a scheduler is provided, for the first `start_epoch_training` epochs the scheduler is applied to modify
            the learning rate without training the network. From then on, the training proceeds normally, applying both
            the scheduler and the optimizer at each epoch. Default to 0.
        use_tqdm : boolean, optional
            Whether using tqdm or not to display progress. Defaults to True.
        optimizer_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer.
        scheduler_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the scheduler.
        loader_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the loader (that handles loading the samples from the
            dataset during the training phase).
        """

        super(ContrastiveDistanceLearning, self).__init__(model, statistics_calc, backend, contrastive_training,
                                                          distance_learning=True, embedding_net=embedding_net,
                                                          n_samples=n_samples, n_samples_val=n_samples_val,
                                                          n_samples_per_param=n_samples_per_param,
                                                          parameters=parameters, simulations=simulations,
                                                          parameters_val=parameters_val,
                                                          simulations_val=simulations_val,
                                                          early_stopping=early_stopping,
                                                          epochs_early_stopping_interval=epochs_early_stopping_interval,
                                                          start_epoch_early_stopping=start_epoch_early_stopping,
                                                          seed=seed, cuda=cuda, scale_samples=scale_samples,
                                                          quantile=quantile, batch_size=batch_size, n_epochs=n_epochs,
                                                          positive_weight=positive_weight,
                                                          load_all_data_GPU=load_all_data_GPU, margin=margin, lr=lr,
                                                          optimizer=optimizer, scheduler=scheduler,
                                                          start_epoch_training=start_epoch_training,
                                                          use_tqdm=use_tqdm,
                                                          optimizer_kwargs=optimizer_kwargs,
                                                          scheduler_kwargs=scheduler_kwargs,
                                                          loader_kwargs=loader_kwargs)


class ExponentialFamilyScoreMatching(StatisticsLearningWithLosses, GraphTools):
    """This class implements the statistics learning technique using exponential family as described in Pacchiardi et
    al. 2020 [1]. Specifically, the idea is to fit an exponential family to a set of parameter-simulation pairs from
    the model, with two neural networks representing the summary statistics and the natural parameters of the
    exponential family. Once the neural networks have been fit, the one representing summary statistics is can be used
    in ABC.

    In order to fit the exponential family (which has an intractable normalization constant), the class relies on
    Score Matching [2] or on Sliced Score Matching [3], which is a faster stochastic version of the former.

    As Score Matching and its sliced version work on an unbounded simulation space, in case the simulations from the
    model are unbounded, they need to be transformed to an unbounded space. This class takes care of this step, provided
    that the user specifies the simulation bounds in the `lower_bound_simulations` and `upper_bound_simulations`
    arguments.

    In order to use this technique, Pytorch is required to handle the neural networks. However, the user does not need
    to be fluent in Pytorch as some default neural networks are instantiated if the user does not provide them
    (experienced users can of course provide the neural networks they would like to use). GPUs can be used to
    train the neural networks if required.

    [1] Pacchiardi, L., and Dutta, R., 2020. Score Matched Conditional Exponential Families for
    Likelihood-Free Inference. arXiv preprint arXiv:2012.10903.

    [2] Hyvärinen, A., and Dayan, P., 2005. Estimation of non-normalized statistical models by score matching.
    Journal of Machine Learning Research, 6(4).

    [3] Song, Y., Garg, S., Shi, J. and Ermon, S., 2019. Sliced score matching: A scalable approach to
    density and score estimation. arXiv preprint arXiv:1905.07088, 2019
    """

    def __init__(self, model, statistics_calc, backend, simulations_net=None, parameters_net=None,
                 embedding_dimension=None,
                 n_samples=1000, n_samples_val=0, parameters=None, simulations=None,
                 parameters_val=None, simulations_val=None,
                 lower_bound_simulations=None, upper_bound_simulations=None,
                 sliced=True, noise_type='radermacher', variance_reduction=False,
                 n_epochs=100, batch_size=16,
                 scale_samples=True, scale_parameters=False,
                 early_stopping=False, epochs_early_stopping_interval=1, start_epoch_early_stopping=10,
                 cuda=None, load_all_data_GPU=False, seed=None,
                 nonlinearity_simulations=None, nonlinearity_parameters=None,
                 batch_norm=True, batch_norm_momentum=0.1, batch_norm_update_before_test=False,
                 lr_simulations=1e-3, lr_parameters=1e-3, lam=0.0,
                 optimizer_simulations=None, optimizer_parameters=None,
                 scheduler_simulations=None, scheduler_parameters=None, start_epoch_training=0,
                 optimizer_simulations_kwargs={}, optimizer_parameters_kwargs={}, scheduler_simulations_kwargs={},
                 scheduler_parameters_kwargs={},
                 use_tqdm=True):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_calc: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class, applied before learning the transformation.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        simulations_net: torch.nn object or list, optional
            The neural network which transforms the simulations to the summary statistics of the exponential family. 
            At the end of the training routine, the output of `simulations_net` (except for the last component)
            will be the learned summary statistics.  
            It can be a torch.nn object with input size corresponding to size of model output 
            (after being transformed by `statistics_calc`) or, alternatively, a list
            with integer numbers denoting the width of the hidden layers, from which a fully connected network with
            that structure is created, having the input size corresponding to size of model output
            (after being transformed by `statistics_calc`) and the output size determined by 
            `embedding_dimension` (see below). Importantly, the output size of `simulations_net` needs to be equal to 
            the output size of `parameters_net` increased by one, as the two are used together in the code. If both nets
            are left to their default values, this is done automatically.   
            In case this is None, a fully connected neural network with three 
            hidden layers is used; the width of the hidden layers is given by
            ``[int(input_size * 1.5), int(input_size * 0.75 + output_size * 3), int(output_size * 5)]``,
            where `input_size` is the size of the data after being transformed by `statistics_calc`, while
            `output_size` is determined by `embedding_dimension`. For further details check
            :func:`abcpy.NN_utilities.networks.createDefaultNN`. By default, this is None.
        parameters_net: torch.nn object or list, optional
            The neural network which maps the parameters to the natural parametrization form of the exponential family. 
            It can be a torch.nn object with input size corresponding to the number of parameters 
            or, alternatively, a list
            with integer numbers denoting the width of the hidden layers, from which a fully connected network with
            that structure is created, having the input size corresponding to the number of parameters
            and the output size determined by 
            `embedding_dimension` (see below). Importantly, the output size of `parameters_net` needs to be equal to 
            the output size of `simulations_net` decreased by one, as the two are used together in the code. 
            If both nets are left to their default values, this is done automatically.   
            In case this is None, a fully connected neural network with three 
            hidden layers is used; the width of the hidden layers is given by
            ``[int(input_size * 1.5), int(input_size * 0.75 + output_size * 3), int(output_size * 5)]``,
            where `input_size` is the number of parameters, while `output_size` is determined by `embedding_dimension`.
            For further details check
            :func:`abcpy.NN_utilities.networks.createDefaultNN`. By default, this is None.
        embedding_dimension: integer, optional 
            Size of the learned summary statistics if `simulations_net` is None or a list. 
            Specifically, in these cases 
            `simulations_net` is automatically created having output size `embedding_dimension + 1`, of which all but 
            the latter components will represent the learned summaries (the latter instead is a learned base measure). 
            If also `parameters_net` is None or a list, it will be automatically created with output size equal to
            `embedding_dimension`. By default `embedding_dimension` is None, in which case it is fixed to the number 
            of parameters in the model.   
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. These are transformed by the 
            `statistics_calc` statistics before the learning step is done. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set. Default
            value is None.
        lower_bound_simulations: np.ndarray, optional
            Array of the same length of the simulations on which the statistics will be learned (therefore, after
            `statistics_calc` has been applied). It contains the lower bounds of the simulations, with each entry
            being either None or a number. It works together with `upper_bound_simulations` to determine the
            nonlinear transformation mapping the bounded space to an unbounded one: if both upper and lower
            bounds for a given entry are None, no transformation is applied to that entry. If both of them are numbers,
            a transformation mapping a compact domain to an unbounded one is applied. If instead the lower bound is a
            number and the upper one is None, a transformation for lower bounded variables is applied. More details on
            the transformations can be found at :class:`abcpy.transformers.BoundedVarTransformer`. By default,
            `lower_bound_simulations` is None, in which case all variables are assumed to not be lower bounded.
        upper_bound_simulations: np.ndarray, optional
            Array of the same length of the simulations on which the statistics will be learned (therefore, after
            `statistics_calc` has been applied). It contains the upper bounds of the simulations, with each entry
            being either None or a number. It works together with `lower_bound_simulations` to determine the
            nonlinear transformation mapping the bounded space to an unbounded one: if both upper and lower
            bounds for a given entry are None, no transformation is applied to that entry. If both of them are numbers,
            a transformation mapping a compact domain to an unbounded one is applied. If instead the lower bound is a
            number and the upper one is None, a transformation for lower bounded variables is applied. More details on
            the transformations can be found at :class:`abcpy.transformers.BoundedVarTransformer`. By default,
            `upper_bound_simulations` is None, in which case all variables are assumed to not be upper bounded.
        sliced: boolean, optional
            If True, the exponential family is fit with the sliced Score Matching approach, which is a faster
            (stochastic) version of Score Matching. If False, the full Score Matching approach is used. Default is True.
        noise_type: basestring, optional
            Denotes the noise type used in the sliced Score Matching version. It can be 'radermacher', 'gaussian' or
            'sphere', with 'radermacher' being the default one. Ignored if `sliced=False`.
        variance_reduction: boolean, optional
            If True, use the variance reduction version of Sliced Score Matching (when that is used), which replaces a
            term with its exact expectation over the noise distribution. Cannot be used when `noise=sphere`.
            Default is False, ignored if `sliced=False`.
        n_epochs: integer, optional
            the number of epochs used for training the neural network. Default is 100
        batch_size: integer, optional
            the batch size used for training the neural network. Default is 16
        scale_samples: boolean, optional
            If True, the simulations are scaled to the (0,1) range before the transformation is learned (i.e., before
            being fed to the neural network). This happens after the simulations have been transformed with
            `statistics_calc` and after the (optional) nonlinear transformation governed by `lower_bound_simulations`
            and `upper_bound_simulations` is applied. This relies on a wrapping of `sklearn.preprocessing.MinMaxScaler`.
            The validation set will also be rescaled in the same fashion.
            When calling the `get_statistics` and the `get_simulations_network` methods,
            the network will be wrapped by :class:`abcpy.NN_utilities.networks.ScalerAndNet`; this automatically
            takes care of transforming the data with the scaler before applying the neural network.
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        scale_parameters: boolean, optional
            If True, the parameters are scaled to the (0,1) range before the natural parameters transformation
            is learned (i.e., before being fed to the neural network).
            This relies on a wrapping of `sklearn.preprocessing.MinMaxScaler`.
            The validation set will also be rescaled in the same fashion.
            When calling the `get_statistics` and the `get_parameters_network` methods,
            the network will be wrapped by :class:`abcpy.NN_utilities.networks.ScalerAndNet`; this automatically
            takes care of transforming the data with the scaler before applying the neural network.
            For parameter, the scaler is not as critical as for simulations, as parameters usually have smaller ranges.
            If however the different parameters differ by orderd of magnitude, using a scaler is recommended.
            Default value is False.
        early_stopping: boolean, optional
            If True, the validation set (which needs to be either provided through the arguments `parameters_val` and
            `simulations_val` or generated by setting `n_samples_val` to a value larger than 0) is used to early stop
            the training of the neural network as soon as the loss on the validation set starts to increase. Default
            value is False.
        epochs_early_stopping_interval: integer, optional
            The frequency at which the validation error is compared in order to decide whether to early stop the
            training or not. Namely, if `epochs_early_stopping_interval=10`, early stopping can happen only at epochs
            multiple of 10. Default value is 1.
        start_epoch_early_stopping: integer, optional
            The epoch after which early stopping can happen; in fact, as soon as training starts, there may be a 
            transient period in which the loss increases. Default value is 10.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        load_all_data_GPU: boolean, optional
            If True and if we a GPU is used, the whole dataset is loaded on the GPU before training begins; this may
            speed up training as it avoid transfer between CPU and GPU, but it is not guaranteed to do. Note that if the
            dataset is not small enough, setting this to True causes things to crash if the dataset is too large.
            Default to False, you should not rely too much on this.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        nonlinearity_simulations: torch.nn class, optional
            If the neural networks for the simulations is built automatically (ie when `simulations_net` is either a
            list or None), then this is used nonlinearity. Default is `torch.nn.Softplus`. This is because the Score
            Matching routine (when `sliced=False`) needs the output of the simulations net to have a non-zero second
            derivative with respect to data, which does not happen when using the common ReLU nonlinearity.
        nonlinearity_parameters: torch.nn class, optional
            If the neural networks for the simulations is built automatically (ie when `parameters_net` is either a
            list or None), then this is used nonlinearity. Default is `torch.nn.ReLU`.
        batch_norm: boolean, optional
            If True, a batch normalization layer is put on top of the parameters net when that is built automatically.
            This improves the performance of the method as it reduces the degeneracy of the
            (summary statistics) * (natural parameters) product. Default is True.
        batch_norm_momentum: float, optional
            Momentum value with which the batch estimates in the batch norm layer are updated at each batch; see
            `torch.nn.BatchNorm1d` for more information. Default is 0.1. Ignored if `batch_norm` is False, or if
            an actual `parameters_net` is provided.
        batch_norm_update_before_test: boolean, optional
            When using batch norm layer on the test set, the resulting test loss evaluation can be noisy as the
            batch norm estimates change during the train phase. To reduce this issue, it is enough to perform a simple
            forward pass of the full train set (without backprop or loss evaulation) before the testing phase is
            started. Set `batch_norm_update_before_test=True` to do that. Default is False.
            Ignored if `batch_norm` is False, if an actual `parameters_net` is provided, as well as if no test set
            is present.
        lr_simulations: float, optional
            The learning rate to be used in the iterative training scheme for the simulations neural network. 
            Default to 1e-3.
        lr_parameters: float, optional
            The learning rate to be used in the iterative training scheme for the parameters neural network. 
            Default to 1e-3.
        lam: float, optional
            If the full Score Matching approach is used (ie `sliced=False`) this denotes the amount of
            second derivative regularization added to the Score Matching loss in the way proposed in Kingma & LeCun
            (2010). Defaul is 0, corresponding to no regularization.
        optimizer_simulations: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`, to be used for the simulations network. 
            Default to `Adam`. Additional parameters may be passed through the `optimizer_simulations_kwargs` argument.
        optimizer_parameters: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`, to be used for the parameters network. 
            Default to `Adam`. Additional parameters may be passed through the `optimizer_parameters_kwargs` argument.
        scheduler_simulations: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs for the simulations net. 
            By default, a :class:`torch.optim.lr_scheduler.ExponentialLR` scheduler with `gamma=0.99` is used.
            Additional arguments may be passed through the `scheduler_simulations_kwargs` parameter.
        scheduler_parameters: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs for the parameters net. 
            By default, a :class:`torch.optim.lr_scheduler.ExponentialLR` scheduler with `gamma=0.99` is used.
            Additional arguments may be passed through the `scheduler_parameters_kwargs` parameter.
        start_epoch_training: integer, optional
            If schedulers is used, for the first `start_epoch_training` epochs the scheduler is applied to modify
            the learning rate without training the network. From then on, the training proceeds normally, applying both
            the scheduler and the optimizer at each epoch. Default to 0.
        optimizer_simulations_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer used for the simulations network.
        optimizer_parameters_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer used for the parameters network.
        scheduler_simulations_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the simulations scheduler.
        scheduler_parameters_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the parameters scheduler.
        use_tqdm : boolean, optional
            Whether using tqdm or not to display progress. Defaults to True.
        """
        self.logger = logging.getLogger(__name__)
        self.scale_samples = scale_samples
        self.scale_parameters = scale_parameters
        self.sliced = sliced

        if lower_bound_simulations is not None and not hasattr(lower_bound_simulations, "shape"):
            raise RuntimeError("Provided lower bounds need to be a numpy array.")
        if upper_bound_simulations is not None and not hasattr(upper_bound_simulations, "shape"):
            raise RuntimeError("Provided upper bounds need to be a numpy array.")
        if upper_bound_simulations is not None and lower_bound_simulations is not None and \
                lower_bound_simulations.shape != upper_bound_simulations.shape:
            raise RuntimeError("Provided lower and upper bounds need to have same shape.")

        # Define device
        if not has_torch:
            raise ImportError(
                "Pytorch is required to instantiate an element of the {} class, in order to handle "
                "neural networks. Please install it. ".format(self.__class__.__name__))

        # set random seed for torch as well:
        if seed is not None:
            torch.manual_seed(seed)

        if cuda is None:
            cuda = torch.cuda.is_available()
        elif cuda and not torch.cuda.is_available():
            # if the user requested to use GPU but no GPU is there
            cuda = False
            self.logger.warning(
                "You requested to use GPU but no GPU is available! The computation will proceed on CPU.")

        self.device = "cuda" if cuda and torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            self.logger.debug("We are using GPU to train the network.")
        else:
            self.logger.debug("We are using CPU to train the network.")

        # this handles generation of the data (or its formatting in case the data is provided to the Semiautomatic
        # class)
        super(ExponentialFamilyScoreMatching, self).__init__(model, statistics_calc, backend, n_samples, n_samples_val,
                                                             1, parameters, simulations, seed=seed,
                                                             parameters_val=parameters_val, simulations_val=simulations_val)

        # we have a validation set if it has the following attribute with size larger than 0
        self.has_val_set = hasattr(self, "sample_parameters_val") and len(self.sample_parameters_val) > 0

        self.logger.info('Learning of the transformation...')
        # Define Data
        parameters, simulations = self.sample_parameters, self.sample_statistics
        if self.has_val_set:
            parameters_val, simulations_val = self.sample_parameters_val, self.sample_statistics_val
        else:
            parameters_val, simulations_val = None, None

        # define the scaler for the simulations by transforming them to a bounded domain (if needed, according to how
        # the bounds are passed) and then rescaling to the [0,1] interval.
        if lower_bound_simulations is None and upper_bound_simulations is None and not scale_samples:
            # in this case we do not use any scaler for the simulations
            self.has_scaler_for_simulations = False
        else:
            self.has_scaler_for_simulations = True

            if lower_bound_simulations is None:
                lower_bound_simulations = np.array([None] * simulations.shape[1])
            if upper_bound_simulations is None:
                upper_bound_simulations = np.array([None] * simulations.shape[1])
            # if both bounds are None this scaler will just behave as a MinMaxScaler. It may be slightly efficient to
            # use that, but it does not matter for now.
            self.scaler_simulations = BoundedVarScaler(lower_bound_simulations, upper_bound_simulations,
                                                       rescale_transformed_vars=self.scale_samples).fit(simulations)
            simulations = self.scaler_simulations.transform(simulations)
            if self.has_val_set:
                simulations_val = self.scaler_simulations.transform(simulations_val)

        # now scale the parameters
        if self.scale_parameters:
            self.scaler_parameters = MinMaxScaler().fit(parameters)
            parameters = self.scaler_parameters.transform(parameters)
            if self.has_val_set:
                parameters_val = self.scaler_parameters.transform(parameters_val)

        # torch.tensor(scaler.transform(samples.reshape(-1, samples.shape[-1])).astype("float32"),
        #              requires_grad=requires_grad).reshape(samples.shape)

        # transform to torch tensors:
        simulations = torch.tensor(simulations.astype("float32"), requires_grad=True)
        parameters = torch.tensor(parameters.astype("float32"), requires_grad=False)
        if self.has_val_set:
            simulations_val = torch.tensor(simulations_val.astype("float32"), requires_grad=True)
            parameters_val = torch.tensor(parameters_val.astype("float32"), requires_grad=False)

        # now setup the default neural network or not

        if embedding_dimension is None:
            embedding_dimension = parameters.shape[1]

        if isinstance(simulations_net, torch.nn.Module):
            self.simulations_net = simulations_net
            self.logger.debug('We use the provided neural network for the summary statistics')

        elif isinstance(simulations_net, list) or simulations_net is None:
            # therefore we need to generate the neural network given the list. The following function returns a class
            # of NN with given input size, output size and hidden sizes; then, need () to instantiate the network
            self.simulations_net = createDefaultNNWithDerivatives(
                input_size=simulations.shape[1], output_size=embedding_dimension + 1, hidden_sizes=simulations_net,
                nonlinearity=torch.nn.Softplus if nonlinearity_simulations is None else nonlinearity_simulations)()
            self.logger.debug('We generate a default neural network for the summary statistics')
        else:
            raise RuntimeError("'simulations_net' needs to be either a torch.nn.Module, or a list, or None.")

        if isinstance(parameters_net, torch.nn.Module):
            self.parameters_net = parameters_net
            self.logger.debug('We use the provided neural network for the parameters')

        elif isinstance(parameters_net, list) or parameters_net is None:
            # therefore we need to generate the neural network given the list. The following function returns a class
            # of NN with given input size, output size and hidden sizes; then, need () to instantiate the network
            self.parameters_net = createDefaultNN(
                input_size=parameters.shape[1], output_size=embedding_dimension, hidden_sizes=parameters_net,
                nonlinearity=torch.nn.ReLU() if nonlinearity_parameters is None else nonlinearity_parameters(),
                batch_norm_last_layer=batch_norm, batch_norm_last_layer_momentum=batch_norm_momentum)()
            self.logger.debug('We generate a default neural network for the parameters')
        else:
            raise RuntimeError("'parameters_net' needs to be either a torch.nn.Module, or a list, or None.")

        if cuda:
            self.simulations_net.cuda()
            self.parameters_net.cuda()

        self.logger.debug('We now run the training routine')
        self.train_losses, self.test_losses = self._train(simulations, parameters, simulations_val, parameters_val,
                                                          n_epochs=n_epochs, use_tqdm=use_tqdm,
                                                          early_stopping=early_stopping,
                                                          load_all_data_GPU=load_all_data_GPU,
                                                          lr_simulations=lr_simulations, lr_parameters=lr_parameters,
                                                          batch_size=batch_size,
                                                          epochs_test_interval=epochs_early_stopping_interval,
                                                          epochs_before_early_stopping=start_epoch_early_stopping,
                                                          batch_norm_update_before_test=batch_norm_update_before_test,
                                                          noise_type=noise_type, variance_reduction=variance_reduction,
                                                          optimizer_simulations=optimizer_simulations,
                                                          optimizer_parameters=optimizer_parameters,
                                                          scheduler_simulations=scheduler_simulations,
                                                          scheduler_parameters=scheduler_parameters,
                                                          optimizer_simulations_kwargs=optimizer_simulations_kwargs,
                                                          optimizer_parameters_kwargs=optimizer_parameters_kwargs,
                                                          scheduler_simulations_kwargs=scheduler_simulations_kwargs,
                                                          scheduler_parameters_kwargs=scheduler_parameters_kwargs,
                                                          lam=lam, start_epoch_training=start_epoch_training)
        self.logger.info("Finished learning the transformation.")

        # move back the nets to CPU.
        self.simulations_net.cpu()
        self.parameters_net.cpu()

    def get_statistics(self, rescale_statistics=True):
        """
        Returns a :class:`abcpy.statistics.NeuralEmbedding` Statistics implementing the learned transformation.

        If a scaler was used, the `net` attribute of the returned object is of the class
        :class:`abcpy.NN_utilities.networks.ScalerAndNet`, which is a nn.Module object wrapping the scaler and the
        learned neural network and applies the scaler before the data is fed through the neural network.

        Additionally, as the learned summary statistics is given by the output of the simulations network excluding
        the last component, we wrap the neural network in the :class:`abcpy.NN_utilities.networks.DiscardLastOutputNet`,
        which automatically takes care of discarding the last output anytime the summary statistics are required.

        Finally, notice that the summary statistics learned with the Exponential Family are only defined up to a
        linear transformation. As such, it may happen that they have very different magnitude. For this reason, we
        provide an option by which the summary statistics are rescale by their standard deviation on the training
        (or test, whenever that was used) set. That is handled automatically by the
        :class:`abcpy.statistics.NeuralEmbedding` class.

        Parameters
        ----------
        rescale_statistics : boolean, optional
            If this is set to True (default), then the returned statistics will be standardized, such that the
            different components of the statistics have the same scale. The standardization works by dividing each
            statistic by the standard deviation achieved on a reference set of simulations. Here, the used set is
            either the validation set used in training (if available) or the training set. If False, no
            standardization is used. Defaults to True.

        Returns
        -------
        :class:`abcpy.statistics.NeuralEmbedding`
            a statistics object that implements the learned transformation.
        """
        if self.has_scaler_for_simulations:
            net = ScalerAndNet(net=DiscardLastOutputNet(self.simulations_net), scaler=self.scaler_simulations)
        else:
            net = DiscardLastOutputNet(self.simulations_net)

        if rescale_statistics:
            # We need a hacky way here. In fact sample_statistics is the one you obtain after the first
            # statistics_calc is applied; if you initialize Neural embedding with the statistics_calc directly,
            # that is applied again, which is not correct.
            # Then we first instantiate the NeuralEmbedding without statistics_calc, and then add it later. In this way
            # the standard deviation is computed correctly, but the behavior of the Statistics in new data will also be
            # correct.
            statistics_calc_new = NeuralEmbedding(net=net, reference_simulations=self.sample_statistics_val
            if self.has_val_set else self.sample_statistics)
            statistics_calc_new.previous_statistics = self.statistics_calc
        else:
            statistics_calc_new = NeuralEmbedding(net=net, previous_statistics=self.statistics_calc)
        return statistics_calc_new

    def get_simulations_network(self):
        """
        Returns the learned neural network for the simulations, representing the learned summary statistics;
        if a scaler was used, the neural net is of the class
        :class:`abcpy.NN_utilities.networks.ScalerAndNet`, which is a nn.Module object wrapping the scaler and the
        learned neural network and automatically applies the scaler before the data is fed through the neural network.
        The original neural network is contained in the `net` attribute of that.

        Returns
        -------
        torch.nn object
            the learned simulations neural network
        """
        return ScalerAndNet(self.simulations_net,
                            self.scaler_simulations) if self.has_scaler_for_simulations else self.simulations_net

    def get_parameters_network(self):
        """
        Returns the learned neural network for the parameters, representing the learned natural parameters in the
        exponential family; if a scaler was used, the neural net is of the class
        :class:`abcpy.NN_utilities.networks.ScalerAndNet`, which is a nn.Module object wrapping the scaler and the
        learned neural network and automatically applies the scaler before the data is fed through the neural network.
        The original neural network is contained in the `net` attribute of that.

        Returns
        -------
        torch.nn object
            the learned parameters neural network
        """
        return ScalerAndNet(self.parameters_net, self.scaler_parameters) if self.scale_parameters else \
            self.parameters_net

    def get_simulations_scaler(self):
        """
        Returns the scaler used for transforming the simulations before feeding them through the neural network.
        Specifically, it can be a :class:`abcpy.transformers.BoundedVarScaler` if the simulations are transformed from
        a bounded to an unbounded domain with a nonlinear transformation, or a
        :class:`sklearn.preprocessing.MinMaxScaler` if the simulations were rescaled to (0,1) without non linear
        transformation. It returns `None` if no scaler was used. The :class:`abcpy.transformers.BoundedVarScaler`
        conforms to the same API as standard sklearn scalers, so it can be used in the same fashion.

        Returns
        -------
        abcpy.transformers.BoundedVarScaler, sklearn.preprocessing.MinMaxScaler or None
            the scaler applied to simulations before the neural network (if present).
        """
        return self.scaler_simulations if self.has_scaler_for_simulations else None

    def get_parameters_scaler(self):
        """
        Returns the scaler used for transforming the parameters before feeding them through the neural network.
        It is an instance of :class:`sklearn.preprocessing.MinMaxScaler`, which rescales the parameters to (0,1).
        It returns `None` if no scaler was used.

        Returns
        -------
        sklearn.preprocessing.MinMaxScaler or None
            the scaler applied to parameters before the neural network (if present).
        """
        return self.scaler_parameters if self.scale_parameters else None

    def _train(self, samples_matrix, theta_vect,
               samples_matrix_test=None, theta_vect_test=None, epochs_test_interval=10,
               epochs_before_early_stopping=100,
               early_stopping=False,
               n_epochs=100, batch_size=None, lr_simulations=0.001, lr_parameters=0.001,
               load_all_data_GPU=False,
               batch_norm_update_before_test=False,
               noise_type='radermacher', variance_reduction=False,
               optimizer_simulations=None, optimizer_parameters=None,
               scheduler_simulations=None, scheduler_parameters=None,
               optimizer_simulations_kwargs={}, optimizer_parameters_kwargs={},
               scheduler_simulations_kwargs={}, scheduler_parameters_kwargs={},
               start_epoch_training=0,
               lam=0.0, use_tqdm=False):
        """This assumes samples matrix to be a 2d tensor with size (n_theta, size_sample) and theta_vect a 2d tensor with
        size (n_theta, p).
        """
        if self.sliced:
            batch_steps = lambda samples, etas: self._single_sliced_score_matching(samples, etas, noise_type=noise_type,
                                                                                   variance_reduction=variance_reduction)
        else:
            batch_steps = lambda samples, etas: self._batch_Fisher_div_with_c_x(samples, etas, lam=lam)

        if load_all_data_GPU:
            # we move all data to the gpu; it needs to be small enough
            samples_matrix = samples_matrix.to(self.device)
            if samples_matrix_test is not None:
                samples_matrix_test = samples_matrix_test.to(self.device)
            theta_vect = theta_vect.to(self.device)
            if theta_vect_test is not None:
                theta_vect_test = theta_vect_test.to(self.device)

        compute_test_loss = False
        if theta_vect_test is not None and samples_matrix_test is not None:
            test_loss_list = []
            compute_test_loss = True
            n_theta_test = theta_vect_test.shape[0]

        if optimizer_simulations is None:
            optimizer_simulations = Adam(self.simulations_net.parameters(), lr=lr_simulations,
                                         **optimizer_simulations_kwargs)
        else:
            optimizer_simulations = optimizer_simulations(self.simulations_net.parameters(), lr=lr_simulations,
                                                          **optimizer_simulations_kwargs)

        if optimizer_parameters is None:
            optimizer_parameters = Adam(self.parameters_net.parameters(), lr=lr_parameters,
                                        **optimizer_parameters_kwargs)
        else:
            optimizer_parameters = optimizer_parameters(self.parameters_net.parameters(), lr=lr_parameters,
                                                        **optimizer_parameters_kwargs)

        if batch_size is None:  # in this case use full batch
            batch_size = theta_vect.shape[0]

        n_theta = theta_vect.shape[0]

        loss_list = []

        # define now the LR schedulers:
        enable_scheduler_simulations = True
        enable_scheduler_parameters = True

        if scheduler_simulations is False:
            enable_scheduler_simulations = False
        else:
            if scheduler_simulations is None:
                # default scheduler
                scheduler_simulations = lr_scheduler.ExponentialLR
                if len(scheduler_simulations_kwargs) == 0:  # no arguments provided
                    scheduler_simulations_kwargs = dict(gamma=0.99)

            # instantiate the scheduler
            scheduler_simulations = scheduler_simulations(optimizer_simulations, **scheduler_simulations_kwargs)

        if scheduler_parameters is False:
            enable_scheduler_parameters = False
        else:
            if scheduler_parameters is None:
                # default scheduler
                scheduler_parameters = lr_scheduler.ExponentialLR
                if len(scheduler_parameters_kwargs) == 0:  # no arguments provided
                    scheduler_parameters_kwargs = dict(gamma=0.99)

            # instantiate the scheduler
            scheduler_parameters = scheduler_parameters(optimizer_parameters, **scheduler_parameters_kwargs)

        # initialize the state_dict variables:
        net_state_dict = None
        net_state_dict_theta = None

        for epoch in range(0, start_epoch_training):
            if enable_scheduler_simulations:
                scheduler_simulations.step()
            if enable_scheduler_parameters:
                scheduler_parameters.step()

        for epoch in tqdm(range(start_epoch_training, n_epochs), disable=not use_tqdm):
            # print("epoch", epoch)
            # set nets to train mode (needed as there may be a batchnorm layer there):
            self.simulations_net.train()
            self.parameters_net.train()

            indeces = self.rng.permutation(n_theta)  # this may be a bottleneck computationally?
            batch_index = 0
            total_train_loss_epoch = 0

            # loop over batches
            while batch_size * batch_index < n_theta:
                # print(batch_index)
                optimizer_simulations.zero_grad()
                optimizer_parameters.zero_grad()

                # by writing in this way, if we go above the number of elements in the vector, you don't care
                batch_indeces = indeces[batch_size * batch_index:batch_size * (batch_index + 1)]

                thetas_batch = theta_vect[batch_indeces].to(self.device)

                # compute the transformed parameter values for the batch:
                etas = self.parameters_net(thetas_batch)

                samples_batch = samples_matrix[batch_indeces].to(self.device)
                # now call the batch routine that takes care of forward step of simulations as well
                batch_loss = batch_steps(samples_batch, etas)

                total_train_loss_epoch += batch_loss.item()

                # set requires_grad to False to save computation
                if lr_simulations == 0:
                    set_requires_grad(self.simulations_net, False)
                if lr_parameters == 0:
                    set_requires_grad(self.parameters_net, False)

                batch_loss.backward()

                # reset it
                if lr_simulations == 0:
                    set_requires_grad(self.simulations_net, True)
                if lr_parameters == 0:
                    set_requires_grad(self.parameters_net, True)

                optimizer_simulations.step()
                optimizer_parameters.step()

                batch_index += 1

            loss_list.append(total_train_loss_epoch / (batch_index + 1))

            # at each epoch we compute the test loss; we need to use batches as well here, otherwise it may not fit
            # to GPU memory
            if compute_test_loss:
                # first, we do forward pass of all the training data in order to update the batchnorm running means
                # (if a batch norm layer is there):
                if batch_norm_update_before_test:
                    with torch.no_grad():
                        batch_index = 0
                        while batch_size * batch_index < n_theta:
                            # the batchnorm is usually after the net; then, it is enough to feedforward the data there:
                            thetas_batch = theta_vect[batch_size * batch_index:batch_size * (batch_index + 1)].to(
                                self.device)
                            _ = self.parameters_net(thetas_batch)
                            batch_index += 1

                self.simulations_net.eval()
                self.parameters_net.eval()

                batch_index = 0
                total_test_loss_epoch = 0
                while batch_size * batch_index < n_theta_test:
                    # no need to shuffle the test data:
                    thetas_batch = theta_vect_test[batch_size * batch_index:batch_size * (batch_index + 1)].to(
                        self.device)
                    samples_batch = samples_matrix_test[batch_size * batch_index:batch_size * (batch_index + 1)].to(
                        self.device)

                    # compute the transformed parameter values for the batch:
                    etas_test = self.parameters_net(thetas_batch)

                    total_test_loss_epoch += batch_steps(samples_batch, etas_test).item()

                    batch_index += 1

                test_loss_list.append(total_test_loss_epoch / (batch_index + 1))

                # the test loss on last step is larger than the training_dataset_index before, stop training
                if early_stopping and (epoch + 1) % epochs_test_interval == 0:
                    # after `epochs_before_early_stopping` epochs, we can stop only if we saved a state_dict before
                    # (ie if at least epochs_test_interval epochs have passed).
                    if epoch + 1 > epochs_before_early_stopping and net_state_dict is not None:
                        if test_loss_list[-1] > test_loss_list[- 1 - epochs_test_interval]:
                            self.logger.info("Training has been early stopped at epoch {}.".format(epoch + 1))
                            # reload the previous state dict:
                            self.simulations_net.load_state_dict(net_state_dict)
                            self.parameters_net.load_state_dict(net_state_dict_theta)
                            break  # stop training
                    # if we did not stop: update the state dict
                    net_state_dict = self.simulations_net.state_dict()
                    net_state_dict_theta = self.parameters_net.state_dict()

            if enable_scheduler_simulations:
                scheduler_simulations.step()
            if enable_scheduler_parameters:
                scheduler_parameters.step()

        # after training, return to eval mode:
        self.simulations_net.eval()
        self.parameters_net.eval()

        if compute_test_loss:
            return loss_list, test_loss_list
        else:
            return loss_list, None

    def _batch_Fisher_div_with_c_x(self, samples, etas, lam=0):
        # do the forward pass at once here:
        if hasattr(self.simulations_net, "forward_and_derivatives"):
            transformed_samples, f, s = self.simulations_net.forward_and_derivatives(samples)
        else:
            transformed_samples = self.simulations_net(samples)
            f, s = jacobian_second_order(samples, transformed_samples, diffable=True)

        f = f.reshape(-1, f.shape[1], f.shape[2])
        s = s.reshape(-1, s.shape[1], s.shape[2])

        return Fisher_divergence_loss_with_c_x(f, s, etas, lam=lam) / (samples.shape[0])

    def _single_sliced_score_matching(self, samples, etas, noise=None, detach=False, noise_type='radermacher',
                                      variance_reduction=False):
        """Can either receive noise as an input or generate it. etas have been pre-transformed by
        parameters net
        This was modified from:
        https://github.com/ermongroup/sliced_score_matching/blob/master/losses/sliced_sm.py
        This function takes care of generating the projection samples and computing the loss by taking the grad.

        Here, only one projection is used for each sample; however the projection changes at each epoch.
        """
        etas = etas.view(-1, etas.shape[-1])
        etas = torch.cat((etas, torch.ones(etas.shape[0], 1).to(etas)), dim=1)  # append a 1
        reshaped_samples = samples.view(-1, samples.shape[-1])
        reshaped_samples.requires_grad_(True)

        if noise is None:
            vectors = torch.randn_like(reshaped_samples).to(reshaped_samples)
            if noise_type == 'radermacher':
                vectors = vectors.sign()
            elif noise_type == 'sphere':
                if variance_reduction:
                    raise RuntimeError("Noise of type 'sphere' can't be used with variance reduction.")
                else:
                    vectors = vectors / torch.norm(vectors, dim=-1, keepdim=True) * np.sqrt(vectors.shape[-1])
            elif noise_type == 'gaussian':
                pass
            else:
                raise RuntimeError("Noise type not implemented")
        else:
            vectors = noise

        transformed_samples = self.simulations_net(reshaped_samples)
        logp = torch.bmm(etas.unsqueeze(1), transformed_samples.unsqueeze(2))  # way to do batch dot products
        logp = logp.sum()
        grad1 = autograd.grad(logp, reshaped_samples, create_graph=True)[0]
        gradv = torch.sum(grad1 * vectors)
        if variance_reduction:
            loss1 = torch.norm(grad1, dim=-1) ** 2 * 0.5  # this is the only difference
        else:
            loss1 = torch.sum(grad1 * vectors, dim=-1) ** 2 * 0.5
        if detach:
            loss1 = loss1.detach()
        grad2 = autograd.grad(gradv, reshaped_samples, create_graph=True)[0]
        loss2 = torch.sum(vectors * grad2, dim=-1)
        if detach:
            loss2 = loss2.detach()

        loss = (loss1 + loss2).mean()
        return loss
