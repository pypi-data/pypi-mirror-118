"""
Deep Feature-Based Models
"""

import warnings
from copy import deepcopy

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Layer, Input, subtract
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import clone_model
import tensorflow.keras.backend as K

from adapt.utils import (GradientHandler,
                         check_arrays,
                         check_one_array,
                         check_network,
                         get_default_encoder,
                         get_default_task,
                         get_default_discriminator)

EPS = K.epsilon()

def accuracy(y_true, y_pred):
    """
    Custom accuracy function which can handle
    probas vector in both binary and multi classification
    
    Parameters
    ----------
    y_true : Tensor
        True tensor.
        
    y_pred : Tensor
        Predicted tensor.
        
    Returns
    -------
    Boolean Tensor
    """
    # TODO: accuracy can't handle 1D ys.
    multi_columns_t = K.cast(K.greater(K.shape(y_true)[1], 1),
                           "float32")
    binary_t = K.reshape(K.sum(K.cast(K.greater(y_true, 0.5),
                                    "float32"), axis=-1), (-1,))
    multi_t = K.reshape(K.cast(K.argmax(y_true, axis=-1),
                             "float32"), (-1,))
    y_true = ((1 - multi_columns_t) * binary_t +
              multi_columns_t * multi_t)
    
    multi_columns_p = K.cast(K.greater(K.shape(y_pred)[1], 1),
                           "float32")
    binary_p = K.reshape(K.sum(K.cast(K.greater(y_pred, 0.5),
                                    "float32"), axis=-1), (-1,))
    multi_p = K.reshape(K.cast(K.argmax(y_pred, axis=-1),
                             "float32"), (-1,))
    y_pred = ((1 - multi_columns_p) * binary_p +
              multi_columns_p * multi_p)        
    return tf.keras.metrics.get("acc")(y_true, y_pred)


class UpdateLambda(Callback):
    """
    Callback updating the lambda trade-off
    of a LambdaFactor layer according to the
    following formula:
    
    lambda = 2 / (1 + exp(-gamma * p)) - 1
    
    With p incresing from 0 to 1 during the
    training process
    
    Parameters
    ----------
    gamma : float (default=10.)
        gamma factor

    lambda_name : string (default="lambda_layer")
        Name of the LambdaLayer instance to
        update.
    """
    def __init__(self, gamma=10., lambda_name="g_handler"):
        self.gamma = gamma
        self.lambda_name = lambda_name
        self.steps = 0.
       
    def on_train_batch_begin(self, batch, logs=None):
        progress = self.steps / self.total_steps
        self.model.get_layer(self.lambda_name).lambda_.assign(
            -K.cast(2. / (1. + K.exp(-self.gamma * progress)) - 1., "float32")
        )
        self.steps += 1.
        
    def set_params(self, params):
        self.total_steps = (params["epochs"] * params["steps"])


class BaseDeepFeature:
    """
    Base for Deep features-based methods.
    
    This object is used as basis for deep DA methods.
    The object takes three networks : ``encoder``, ``task`` and
    ``discriminator``. A deep DA object can be created as
    a ``BaseDeepFeature`` child by implementing the
    ``create_model`` and ``get_loss`` methods.
    
    Parameters
    ----------
    encoder : tensorflow Model (default=None)
        Encoder netwok. If ``None``, a shallow network with 10
        neurons and ReLU activation is used as encoder network.
        
    task : tensorflow Model (default=None)
        Task netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as task network.
        
    discriminator : tensorflow Model (default=None)
        Discriminator netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as discriminator
        network. Note that the output shape of the discriminator should
        be ``(None, 1)`` and a ``sigmoid`` activation should be used.

    loss : string or tensorflow loss (default="mse")
        Loss function used for the task.
        
    metrics : dict or list of string or tensorflow metrics (default=None)
        Metrics given to the model. If a list is provided,
        metrics are used on both ``task`` and ``discriminator``
        outputs. To give seperated metrics, please provide a
        dict of metrics list with ``"task"`` and ``"disc"`` as keys.
        
    optimizer : string or tensorflow optimizer (default=None)
        Optimizer of the model. If ``None``, the
        optimizer is set to tf.keras.optimizers.Adam(0.001)
        
    copy : boolean (default=True)
        Whether to make a copy of ``encoder``, ``task`` and
        ``discriminator`` or not.
        
    random_state : int (default=None)
        Seed of random generator.
    
    Attributes
    ----------
    encoder_ : tensorflow Model
        encoder network.
        
    task_ : tensorflow Model
        task network.
        
    discriminator_ : tensorflow Model
        discriminator network.
    
    model_ : tensorflow Model
        Fitted model: the union of ``encoder_``,
        ``task_`` and ``discriminator_`` networks.
        
    history_ : dict
        history of the losses and metrics across the epochs.
        If ``yt`` is given in ``fit`` method, target metrics
        and losses are recorded too.
        
    See also
    --------
    DANN
    ADDA
    DeepCORAL
    """
    def __init__(self, 
                 encoder=None,
                 task=None,
                 discriminator=None,
                 loss="mse",
                 metrics=None,
                 optimizer=None,
                 copy=True,
                 random_state=None):
                
        np.random.seed(random_state)
        tf.random.set_seed(random_state)
        
        if encoder is None:
            encoder = get_default_encoder()
        if task is None:
            task = get_default_task()
        if discriminator is None:
            discriminator = get_default_discriminator()
        
        if not isinstance(metrics, (list, dict, type(None))):
            raise ValueError("`metrics` argument should be an instance "
                             "of dict or list")
        
        if isinstance(metrics, dict):
            metrics_disc = metrics.get("disc")
            metrics_task = metrics.get("task")
        else:
            metrics_disc = metrics
            metrics_task = metrics
        if metrics_disc is None:
            metrics_disc = []
        if metrics_task is None:
            metrics_task = []
        
        if optimizer is None:
            optimizer = Adam(0.001)
        
        self.encoder_ = check_network(encoder,
                                      copy=copy,
                                      display_name="encoder",
                                      compile_=False)
        self.task_ = check_network(task,
                                   copy=copy,
                                   display_name="task",
                                   compile_=False)
        self.discriminator_ = check_network(discriminator,
                                            copy=copy,
                                            display_name="discriminator",
                                            compile_=False)
        self.loss = loss
        self.metrics = metrics
        self.loss_ = tf.keras.losses.get(loss)
        self.metrics_disc_ = []
        self.metrics_task_ = []
        for m in metrics_disc:
            if ((isinstance(m, str) and "acc" in m) or 
                (hasattr(m, "__name__") and "acc" in m.__name__) or
                (hasattr(m, "__class__") and "Acc" in m.__class__.__name__)):
                self.metrics_disc_.append(accuracy)
            else:
                self.metrics_disc_.append(tf.keras.metrics.get(m))
        for m in metrics_task:
            if ((isinstance(m, str) and "acc" in m) or 
                (hasattr(m, "__name__") and "acc" in m.__name__) or
                (hasattr(m, "__class__") and "Acc" in m.__class__.__name__)):
                self.metrics_task_.append(accuracy)
            else:
                self.metrics_task_.append(tf.keras.metrics.get(m))
        self.optimizer = optimizer
        self.copy = copy
        self.random_state = random_state
        

    def _build(self, shape_Xs, shape_ys,
                    shape_Xt, shape_yt):
        
        # Call predict to avoid strange behaviour with
        # Sequential model whith unspecified input_shape
        zeros_enc_ = self.encoder_.predict(np.zeros((1,) + shape_Xt));
        self.task_.predict(zeros_enc_);
        self.discriminator_.predict(zeros_enc_);
                
        inputs_Xs = Input(shape_Xs)
        inputs_ys = Input(shape_ys)
        inputs_Xt = Input(shape_Xt)
                
        if shape_yt is None:
            inputs_yt = None
            inputs = [inputs_Xs, inputs_ys, inputs_Xt]
        else:
            inputs_yt = Input(shape_yt)
            inputs = [inputs_Xs, inputs_ys,
                      inputs_Xt, inputs_yt]
        
        outputs = self.create_model(inputs_Xs=inputs_Xs,
                                    inputs_Xt=inputs_Xt)
        
        self.model_ = Model(inputs, outputs)
        
        loss = self.get_loss(inputs_ys=inputs_ys,
                              **outputs)
        metrics = self.get_metrics(inputs_ys=inputs_ys,
                                    inputs_yt=inputs_yt,
                                    **outputs)
        
        self.model_.add_loss(loss)
        for k in metrics:            
            self.model_.add_metric(tf.reduce_mean(metrics[k]),
                                   name=k, aggregation="mean")
        
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        self.model_.compile(optimizer=self.optimizer)
        self.history_ = {}
        return self
    
    
    def _fit(self, Xs, ys, Xt, yt=None, **fit_params):
        
        np.random.seed(self.random_state)
        tf.random.set_seed(self.random_state)
        
        Xs, ys, Xt, yt = check_arrays(Xs, ys, Xt, yt)
               
        shape_Xs = Xs.shape[1:]
        shape_Xt = Xt.shape[1:]
        shape_ys = ys.shape[1:]
        if yt is None:
            shape_yt = None
        else:
            shape_yt = yt.shape[1:]
            
        max_size = max(len(Xs), len(Xt))
        
        Xs = np.resize(Xs, (max_size,) + shape_Xs)
        ys = np.resize(ys, (max_size,) + shape_ys)
        Xt = np.resize(Xt, (max_size,) + shape_Xt)
        if yt is not None:
            yt = np.resize(yt, (max_size,) + shape_yt)
        
        if not hasattr(self, "model_"):
            self._build(shape_Xs, shape_ys,
                       shape_Xt, shape_yt)
        
        if yt is None:
            hist = self.model_.fit([Xs, ys, Xt],
                                   **fit_params)
        else:
            hist = self.model_.fit([Xs, ys, Xt, yt],
                                   **fit_params)

        for k, v in hist.history.items():
            self.history_[k] = self.history_.get(k, []) + v
        return self
    
    
    def _get_metric_names(self):
        names_task = []
        for metric, i in zip(self.metrics_task_,
                             range(len(self.metrics_task_))):
            if hasattr(metric, "__name__"):
                name = metric.__name__
            elif hasattr(metric, "__class__"):
                name = metric.__class__.__name__
            else:
                name = str(i)
            if "_" in name: 
                short_name = ""
                for s in name.split("_"):
                    if len(s) > 0:
                        short_name += s[0]
            else:
                short_name = name[:3]
            
            names_task.append("task_" + short_name)
            
        names_disc = []
        for metric, i in zip(self.metrics_disc_,
                             range(len(self.metrics_disc_))):
            if hasattr(metric, "__name__"):
                name = metric.__name__
            elif hasattr(metric, "__class__"):
                name = metric.__class__.__name__
            else:
                name = str(i)
            if "_" in name: 
                short_name = ""
                for s in name.split("_"):
                    if len(s) > 0:
                        short_name += s[0]
            else:
                short_name = name[:3]
            names_disc.append("disc_" + short_name)
        return names_task, names_disc


    def create_model(self, inputs_Xs, inputs_Xt):
        """
        Create model. 
        
        Give the model architecture from the Xs, Xt
        inputs to the outputs.
        
        Parameters
        ----------
        inputs_Xs : InputLayer
            Input layer for Xs entries.
            
        inputs_Xt : InputLayer
            Input layer for Xt entries.
        
        Returns
        -------
        outputs : dict of tf Tensors
            Outputs tensors of the model
            (used to compute the loss).
        """
        pass

    
    def get_loss(self, inputs_ys, **ouputs):
        """
        Get loss.
        
        Parameters
        ----------
        inputs_ys : InputLayer
            Input layer for ys entries.
        
        outputs : dict of tf Tensors
            Model outputs tensors.
        
        Returns
        -------
        loss : tf Tensor
            Model loss
        """
        pass
   

    def get_metrics(self, inputs_ys, inputs_yt, **outputs):
        """
        Get Metrics.
        
        Parameters
        ----------
        inputs_ys : InputLayer
            Input layer for ys entries.
            
        inputs_yt : InputLayer
            Input layer for yt entries.
        
        outputs : dict of tf Tensors
            Model outputs tensors.
        
        Returns
        -------
        metrics : dict of tf Tensors
            Model metrics. dict keys give the
            name of the metric and dict values
            give the corresponding Tensor.
        """
        return {}


    def fit(self, Xs, ys, Xt, yt=None, **fit_params):
        """
        Fit Model. Note that ``fit`` does not reset
        the model but extend the training.

        Parameters
        ----------
        Xs : numpy array
            Source input data.

        ys : numpy array
            Source output data.

        Xt : numpy array
            Target input data.
            
        yt : numpy array (default=None)
            Target output data. `yt` is only used
            for validation metrics.

        fit_params : key, value arguments
            Arguments given to the fit method of the model
            (epochs, batch_size, callbacks...).

        Returns
        -------
        self : returns an instance of self
        """
        return self._fit(Xs, ys, Xt, yt, **fit_params)


    def predict(self, X):
        """
        Return predictions of the task network on the encoded features.
        
        Parameters
        ----------
        X : array
            input data
            
        Returns
        -------
        y_pred : array
            predictions of task network
        """
        X = check_one_array(X)
        return self.task_.predict(self.predict_features(X))
    
    
    def predict_features(self, X):
        """
        Return the encoded features of X.
        
        Parameters
        ----------
        X : array
            input data
            
        Returns
        -------
        X_enc : array
            predictions of encoder network
        """
        X = check_one_array(X)
        return self.encoder_.predict(X)
    
    
    def predict_disc(self, X):
        """
        Return predictions of the discriminator on the encoded features.
        
        Parameters
        ----------
        X : array
            input data
            
        Returns
        -------
        y_disc : array
            predictions of discriminator network
        """
        X = check_one_array(X)
        return self.discriminator_.predict(self.predict_features(X))




class DANN(BaseDeepFeature):
    """
    DANN: Discriminative Adversarial Neural Network
    
    DANN is a feature-based domain adaptation method.
    
    The goal of DANN is to find a new representation of the input features
    in which source and target data could not be distinguished by any
    **discriminator** network. This new representation is learned by an
    **encoder** network in an adversarial fashion. A **task** network is
    learned on the encoded space in parallel to the **encoder** and 
    **discriminator** networks.
    
    The three network paremeters are optimized according to the
    following objectives:
    
    .. math::
    
        \min_{\phi, F} & \; \mathcal{L}_{task}(F(\phi(X_S)), y_S) -
        \lambda \\left(
        \log(1 - D(\phi(X_S))) + \log(D(\phi(X_T))) \\right) \\\\
        \max_{D} & \; \log(1 - D(\phi(X_S))) + \log(D(\phi(X_T)))
        
    Where:
    
    - :math:`(X_S, y_S), (X_T)` are respectively the labeled source data
      and the unlabeled target data.
    - :math:`\phi, F, D` are respectively the **encoder**, the **task**
      and the **discriminator** networks
    - :math:`\lambda` is the trade-off parameter.
    
    The adversarial training is done through a **reversal gradient layer**
    placed between the **encoder** and the **discriminator** networks.
    This layer inverses the gradient sign in backpropagation, thus the
    two networks are optimized according to two opposite objective functions.
    
    The method has been originally introduced for **unsupervised**
    classification DA but it could be widen to other task in
    **supervised** DA straightforwardly.
    
    .. figure:: ../_static/images/dann.png
        :align: center
        
        DANN architecture (source: [1])
    
    Parameters
    ----------
    encoder : tensorflow Model (default=None)
        Encoder netwok. If ``None``, a shallow network with 10
        neurons and ReLU activation is used as encoder network.
        
    task : tensorflow Model (default=None)
        Task netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as task network.
        
    discriminator : tensorflow Model (default=None)
        Discriminator netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as discriminator
        network. Note that the output shape of the discriminator should
        be ``(None, 1)`` and a ``sigmoid`` activation should be used.
        
    lambda_ : float or None (default=0.1)
        Trade-off parameter.
        If ``None``, ``lambda_`` increases gradually
        according to the following formula:
        ``lambda_`` = 2/(1 + exp(-``gamma`` * p)) - 1.
        With p growing from 0 to 1 during training.
        
    gamma : float (default=10.0)
        Increase rate parameter.
        Give the increase rate of the trade-off parameter if
        ``lambda_`` is set to ``None``.

    loss : string or tensorflow loss (default="mse")
        Loss function used for the task.
        
    metrics : dict or list of string or tensorflow metrics (default=None)
        Metrics given to the model. If a list is provided,
        metrics are used on both ``task`` and ``discriminator``
        outputs. To give seperated metrics, please provide a
        dict of metrics list with ``"task"`` and ``"disc"`` as keys.
        
    optimizer : string or tensorflow optimizer (default=None)
        Optimizer of the model. If ``None``, the
        optimizer is set to tf.keras.optimizers.Adam(0.001)
        
    copy : boolean (default=True)
        Whether to make a copy of ``encoder``, ``task`` and
        ``discriminator`` or not.
        
    random_state : int (default=None)
        Seed of random generator.
    
    Attributes
    ----------
    encoder_ : tensorflow Model
        encoder network.
        
    task_ : tensorflow Model
        task network.
        
    discriminator_ : tensorflow Model
        discriminator network.
    
    model_ : tensorflow Model
        Fitted model: the union of ``encoder_``,
        ``task_`` and ``discriminator_`` networks.
        
    history_ : dict
        history of the losses and metrics across the epochs.
        If ``yt`` is given in ``fit`` method, target metrics
        and losses are recorded too.
        
    Examples
    --------
    >>> import numpy as np
    >>> from adapt.feature_based import DANN
    >>> np.random.seed(0)
    >>> Xs = np.concatenate((np.random.random((100, 1)),
    ...                      np.zeros((100, 1))), 1)
    >>> Xt = np.concatenate((np.random.random((100, 1)),
    ...                      np.ones((100, 1))), 1)
    >>> ys = 0.2 * Xs[:, 0]
    >>> yt = 0.2 * Xt[:, 0]
    >>> model = DANN(lambda_=0., random_state=0)
    >>> model.fit(Xs, ys, Xt, yt, epochs=100, verbose=0)
    >>> model.history_["task_t"][-1]
    0.0240...
    >>> model = DANN(lambda_=0.1, random_state=0)
    >>> model.fit(Xs, ys, Xt, yt, epochs=100, verbose=0)
    >>> model.history_["task_t"][-1]
    0.0022...
    
    See also
    --------
    ADDA
    DeepCORAL
        
    References
    ----------
    .. [1] `[1] <http://jmlr.org/papers/volume17/15-239/15-239.pdf>`_ Y. Ganin, \
E. Ustinova, H. Ajakan, P. Germain, H. Larochelle, F. Laviolette, M. Marchand, \
and V. Lempitsky. "Domain-adversarial training of neural networks". In JMLR, 2016.
    """
    def __init__(self, 
                 encoder=None,
                 task=None,
                 discriminator=None,
                 lambda_=0.1,
                 gamma=10.,
                 loss="mse",
                 metrics=None,
                 optimizer=None,
                 copy=True,
                 random_state=None):
        
        self.lambda_ = lambda_
        if self.lambda_ is None:
            self.lambda_init_ = 0.
        else:
            self.lambda_init_ = self.lambda_
        self.gamma = gamma        
        super().__init__(encoder, task, discriminator,
                         loss, metrics, optimizer, copy,
                         random_state)

        
    def fit(self, Xs, ys, Xt, yt=None, **fit_params):  
        Xs, ys, Xt, yt = check_arrays(Xs, ys, Xt, yt)
        
        # Define callback for incresing lambda_, if model_ is
        # already built, do not reinitialized lambda_
        if self.lambda_ is None and not hasattr(self, "model_"):
            callback = UpdateLambda(gamma=self.gamma)
            if "callbacks" in fit_params:
                fit_params["callbacks"].append(callback)
            else:
                fit_params["callbacks"] = [callback]

        self._fit(Xs, ys, Xt, yt, **fit_params)
        return self
    
    
    def create_model(self, inputs_Xs, inputs_Xt):

        encoded_src = self.encoder_(inputs_Xs)
        encoded_tgt = self.encoder_(inputs_Xt)
        task_src = self.task_(encoded_src)
        task_tgt = self.task_(encoded_tgt)
        
        flip = GradientHandler(-self.lambda_init_)
        
        disc_src = flip(encoded_src)
        disc_src = self.discriminator_(disc_src)
        disc_tgt = flip(encoded_tgt)
        disc_tgt = self.discriminator_(disc_tgt)
        
        outputs = dict(task_src=task_src,
                       task_tgt=task_tgt,
                       disc_src=disc_src,
                       disc_tgt=disc_tgt)
        return outputs


    def get_loss(self, inputs_ys,
                  task_src, task_tgt,
                  disc_src, disc_tgt):
        
        loss_task = self.loss_(inputs_ys, task_src)
        loss_disc = (-K.log(1-disc_src + EPS)
                     -K.log(disc_tgt + EPS))
        
        loss = K.mean(loss_task) + K.mean(loss_disc)
        return loss
    
    
    def get_metrics(self, inputs_ys, inputs_yt,
                     task_src, task_tgt,
                     disc_src, disc_tgt):
        metrics = {}
        
        task_s = self.loss_(inputs_ys, task_src)
        disc = (-K.log(1-disc_src + EPS)
                -K.log(disc_tgt + EPS))
        
        metrics["task_s"] = K.mean(task_s)
        metrics["disc"] = K.mean(disc)
        if inputs_yt is not None:
            task_t = self.loss_(inputs_yt, task_tgt)
            metrics["task_t"] = K.mean(task_t)
        
        names_task, names_disc = self._get_metric_names()
        
        for metric, name in zip(self.metrics_task_, names_task):
            metrics[name + "_s"] = metric(inputs_ys, task_src)
            if inputs_yt is not None:
                metrics[name + "_t"] = metric(inputs_yt, task_tgt)
                
        for metric, name in zip(self.metrics_disc_, names_disc):
            pred = K.concatenate((disc_src, disc_tgt), axis=0)
            true = K.concatenate((K.zeros_like(disc_src),
                                  K.ones_like(disc_tgt)), axis=0)
            metrics[name] = metric(true, pred)
        return metrics


class ADDA(BaseDeepFeature):
    """
    ADDA: Adversarial Discriminative Domain Adaptation

    ADDA is a feature-based domain adaptation method.
    
    The purpose of ADDA is to build a new feature representation
    in which source and target data could not be distinguished by
    any **discriminator** network. This feature representation is
    built with two **encoder** networks:
    
    - a **source encoder** trained to provide good features in order
      to learn the task on the source domain. The task is learned
      through a **task** network trained with the **source encoder**.
    - a **target encoder** trained to fool a **discriminator** network
      which tries to classify source and target data in the encoded space.
      The **target encoder** and the **discriminator** are trained
      in an adversarial fashion in the same way as GAN.
      
    The parameters of the four networks are optimized in a two stage
    algorithm where **source encoder** and **task** networks are first
    fitted according to the following optimization problem:
    
    .. math::
    
        \min_{\phi_S, F} \mathcal{L}_{task}(F(\phi_S(X_S)), y_S)
    
    In the second stage, **target encoder** and **discriminator**
    networks are fitted according to:
    
    .. math::
    
        \min_{\phi_T} & \; - \log(D(\phi_T(X_T)))) \\\\
        \min_{D} & \; - \log(D(\phi_S(X_S))) - \log(1 - D(\phi_T(X_T)))
    
    Where:
    
    - :math:`(X_S, y_S), (X_T)` are respectively the labeled source data
      and the unlabeled target data.
    - :math:`\phi_S, \phi_T, F, D` are respectively the **source encoder**,
      the **target encoder**, the **task** and the **discriminator** networks.
    
    The method has been originally introduced for **unsupervised**
    classification DA but it could be widen to other task in **supervised**
    DA straightforwardly.
    
    .. figure:: ../_static/images/adda.png
        :align: center
        
        Overview of the ADDA approach (source: [1])
    
    Parameters
    ----------
    encoder : tensorflow Model (default=None)
        Encoder netwok. If ``None``, a shallow network with 10
        neurons and ReLU activation is used as encoder network.
        
    task : tensorflow Model (default=None)
        Task netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as task network.
        
    discriminator : tensorflow Model (default=None)
        Discriminator netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as discriminator
        network. Note that the output shape of the discriminator should
        be ``(None, 1)`` and a ``sigmoid`` activation should be used.
        
    encoder_src : tensorflow Model (default=None)
        Source encoder netwok. A source encoder network can be
        given in the case of heterogenous features between
        source and target domains. If ``None``, a copy of the
        ``encoder`` network is used as source encoder.
        
    is_pretrained : boolean (default=False)
        Specify if the encoder is already pretrained on source or not

    loss : string or tensorflow loss (default="mse")
        Loss function used for the task.
        
    metrics : dict or list of string or tensorflow metrics (default=None)
        Metrics given to the model. If a list is provided,
        metrics are used on both ``task`` and ``discriminator``
        outputs. To give seperated metrics, please provide a
        dict of metrics list with ``"task"`` and ``"disc"`` as keys.
        
    optimizer : string or tensorflow optimizer (default=None)
        Optimizer of the model. If ``None``, the
        optimizer is set to tf.keras.optimizers.Adam(0.001)
        
    optimizer_src : string or tensorflow optimizer (default=None)
        Optimizer of the source model. If ``None``, the source
        optimizer is a copy of ``optimizer``.
        
    copy : boolean (default=True)
        Whether to make a copy of ``encoder``, ``task`` and
        ``discriminator`` or not.
        
    random_state : int (default=None)
        Seed of random generator.
    
    Attributes
    ----------
    encoder_ : tensorflow Model
        encoder network.
        
    task_ : tensorflow Model
        task network.
        
    discriminator_ : tensorflow Model
        discriminator network.
    
    model_ : tensorflow Model
        Fitted model: the union of ``encoder_``,
        and ``discriminator_`` networks.
        
    model_src_ : tensorflow Model
        Fitted source model: the union of ``encoder_src_``
        and ``task_`` networks.
        
    history_ : dict
        history of the losses and metrics across the epochs.
        If ``yt`` is given in ``fit`` method, target metrics
        and losses are recorded too.
        
    history_src_ : dict
        Source model history of the losses and metrics
        across the epochs. If ``yt`` is given in ``fit``
        method, target metrics and losses are recorded too.
        
    is_pretrained_ : boolean
        Specify if the encoder is already pretrained on
        source or not. If True, the ``fit`` method will
        only performs the second stage of ADDA.
        
    Examples
    --------
    >>> import numpy as np
    >>> from adapt.feature_based import ADDA
    >>> np.random.seed(0)
    >>> Xs = np.concatenate((np.random.random((100, 1)),
    ...                      np.zeros((100, 1))), 1)
    >>> Xt = np.concatenate((np.random.random((100, 1)),
    ...                      np.ones((100, 1))), 1)
    >>> ys = 0.2 * Xs[:, 0]
    >>> yt = 0.2 * Xt[:, 0]
    >>> model = ADDA(random_state=0)
    >>> model.fit(Xs, ys, Xt, yt, epochs=100, verbose=0)
    >>> model.history_src_["task_t"][-1]
    0.0234...
    >>> model.history_["task_t"][-1]
    0.0009...
    
    See also
    --------
    DANN
    DeepCORAL
        
    References
    ----------
    .. [1] `[1] <https://arxiv.org/pdf/1702.05464.pdf>`_ E. Tzeng, J. Hoffman, \
K. Saenko, and T. Darrell. "Adversarial discriminative domain adaptation". \
In CVPR, 2017.
    """
    def __init__(self, 
                 encoder=None,
                 task=None,
                 discriminator=None,
                 encoder_src=None,
                 is_pretrained=False,
                 loss="mse",
                 metrics=None,
                 optimizer=None,
                 optimizer_src=None,
                 copy=True,
                 random_state=None):

        super().__init__(encoder, task, discriminator,
                         loss, metrics, optimizer, copy,
                         random_state)
        self.is_pretrained_ = is_pretrained
        
        if optimizer_src is None:
            self.optimizer_src = deepcopy(self.optimizer)
        else:
            self.optimizer_src = optimizer_src
        
        if encoder_src is None:
            self.encoder_src_ = check_network(self.encoder_,
                                              copy=True,
                                              display_name="encoder",
                                              force_copy=True,
                                              compile_=False)
            self.same_encoder_ = True
        else:
            self.encoder_src_ = check_network(encoder_src,
                                              copy=copy,
                                              display_name="encoder_src",
                                              compile_=False)
            self.same_encoder_ = False

        
    def fit_source(self, Xs, ys, Xt=None, yt=None, **fit_params):
        """
        Build and fit source encoder and task networks
        on source data.
        
        This method performs the first stage of ADDA.

        Parameters
        ----------
        Xs : numpy array
            Source input data.

        ys : numpy array
            Source output data.

        Xt : numpy array (default=None)
            Target input data. Target data are only
            used in the fit method of ``model_src_`` as
            validation data.
            
        yt : numpy array (default=None)
            Target output data. Target data are only
            used in the fit method of ``model_src_`` as
            validation data.

        fit_params : key, value arguments
            Arguments given to the fit method of the model
            (epochs, batch_size, callbacks...).

        Returns
        -------
        model_src_ : returns the fitted source model.
        """
        np.random.seed(self.random_state)
        tf.random.set_seed(self.random_state)
                
        # Call predict to avoid strange behaviour with
        # Sequential model whith unspecified input_shape
        zeros_enc_ = self.encoder_src_.predict(np.zeros((1,) + Xs.shape[1:]));
        self.task_.predict(zeros_enc_);
        
        self.model_src_ = Sequential()
        self.model_src_.add(self.encoder_src_)
        self.model_src_.add(self.task_)
        self.model_src_.compile(loss=self.loss_,
                                metrics=self.metrics_task_,
                                optimizer=self.optimizer_src)
        
        if (Xt is not None and yt is not None and 
            not "validation_data" in fit_params):
            hist = self.model_src_.fit(Xs, ys,
                                       validation_data=(Xt, yt),
                                       **fit_params)
            hist.history["task_t"] = hist.history.pop("val_loss")
            for k in hist.history:
                if "val_" in k:
                    hist.history[k.replace("val_", "") + "_t"] = hist.history.pop(k)
        else:
            hist = self.model_src_.fit(Xs, ys, **fit_params)

        hist.history["task_s"] = hist.history.pop("loss")
        
        for k, v in hist.history.items():
            if not hasattr(self, "history_src_"):
                self.history_src_ = {}
            self.history_src_[k] = self.history_src_.get(k, []) + v
        return self.model_src_


    def fit_target(self, Xs_enc, ys, Xt, yt=None, **fit_params):
        """
        Build and fit target encoder and discriminator
        networks on source data.
        
        This method performs the second stage of ADDA.

        Parameters
        ----------
        Xs_enc : numpy array
            Source encoded data.

        ys : numpy array
            Source output data.

        Xt : numpy array
            Target input data.
            
        yt : numpy array (default=None)
            Target output data. `yt` is only used
            for validation metrics.

        fit_params : key, value arguments
            Arguments given to the fit method of the model
            (epochs, batch_size, callbacks...).

        Returns
        -------
        model_ : return the fitted target model.
        """
        self._fit(Xs_enc, ys, Xt, yt, **fit_params)
        return self.model_
        
    
    def fit(self, Xs, ys, Xt, yt=None, fit_params_src=None, **fit_params):
        """
        Perform the two stages of ADDA.
        
        First ``encoder_src_`` and ``task_`` are fitted using
        ``Xs`` and ``ys``. Then ``encoder_`` and ``discriminator_``
        are fitted using ``Xs``, ``Xt`` and ``ys``.
        
        Note that if fit is called again, only the training of
        ``encoder_`` and ``discriminator_`` is extended,
        ``encoder_src_`` and ``task_`` remaining as they are.
        
        Parameters
        ----------
        Xs : numpy array
            Source input data.

        ys : numpy array
            Source output data.

        Xt : numpy array
            Target input data.
            
        yt : numpy array (default=None)
            Target output data. `yt` is only used
            for validation metrics.

        fit_params_src : dict (default=None)
            Arguments given to the fit method of the
            source model (epochs, batch_size, callbacks...).
            If ``None``, fit_params_src is set to fit_params.

        fit_params : key, value arguments
            Arguments given to the fit method of the
            target model (epochs, batch_size, callbacks...).

        Returns
        -------
        self : returns an instance of self
        """
        if fit_params_src is None:
            fit_params_src = fit_params
        
        Xs, ys, Xt, yt = check_arrays(Xs, ys, Xt, yt)
        
        if not self.is_pretrained_:
            self.fit_source(Xs, ys, Xt, yt, **fit_params_src)
            self.is_pretrained_ = True
            if self.same_encoder_:
                # Call predict to set architecture if no
                # input_shape is given
                self.encoder_.predict(np.zeros((1,) + Xt.shape[1:]))
                self.encoder_.set_weights(self.encoder_src_.get_weights())
        
        Xs_enc = self.encoder_src_.predict(Xs)
        
        self.fit_target(Xs_enc, ys, Xt, yt, **fit_params)
        return self
    
    
    def create_model(self, inputs_Xs, inputs_Xt):

        encoded_tgt = self.encoder_(inputs_Xt)
        encoded_tgt_nograd = GradientHandler(0.)(encoded_tgt)
        
        task_tgt = self.task_(encoded_tgt)

        disc_src = self.discriminator_(inputs_Xs)
        disc_tgt = self.discriminator_(encoded_tgt)
        disc_tgt_nograd = self.discriminator_(encoded_tgt_nograd)
        
        outputs = dict(disc_src=disc_src,
                       disc_tgt=disc_tgt,
                       disc_tgt_nograd=disc_tgt_nograd,
                       task_tgt=task_tgt)
        return outputs


    def get_loss(self, inputs_ys, disc_src, disc_tgt,
                  disc_tgt_nograd, task_tgt):
        
        loss_disc = (-K.log(disc_src + EPS)
                     -K.log(1-disc_tgt_nograd + EPS))
        
        # The second term is here to cancel the gradient update on
        # the discriminator
        loss_enc = (-K.log(disc_tgt + EPS)
                    +K.log(disc_tgt_nograd + EPS))
        
        loss = K.mean(loss_disc) + K.mean(loss_enc)
        return loss
    
    
    def get_metrics(self, inputs_ys, inputs_yt,
                     disc_src, disc_tgt,
                     disc_tgt_nograd, task_tgt):
        metrics = {}
        
        disc = (-K.log(disc_src + EPS)
                -K.log(1-disc_tgt_nograd + EPS))
        
        metrics["disc"] = K.mean(disc)
        if inputs_yt is not None:
            task_t = self.loss_(inputs_yt, task_tgt)
            metrics["task_t"] = K.mean(task_t)
        
        names_task, names_disc = self._get_metric_names()
        
        if inputs_yt is not None:
            for metric, name in zip(self.metrics_task_, names_task):
                metrics[name + "_t"] = metric(inputs_yt, task_tgt)
                      
        for metric, name in zip(self.metrics_disc_, names_disc):
            pred = K.concatenate((disc_src, disc_tgt), axis=0)
            true = K.concatenate((K.ones_like(disc_src),
                                  K.zeros_like(disc_tgt)), axis=0)
            metrics[name] = metric(true, pred)
        return metrics
    
    
    def predict_features(self, X, domain="tgt"):
        """
        Return the encoded features of X.
        
        Parameters
        ----------
        X : array
            Input data

        domain: str (default="tgt")
            If domain is ``"tgt"`` or ``"target"``,
            outputs of ``encoder_`` are returned.
            If domain is ``"src"`` or ``"source"``,
            outputs of ``encoder_src_`` are returned.
            
        Returns
        -------
        X_enc : array
            predictions of encoder network
        """
        X = check_one_array(X)
        if domain in ["tgt", "target"]:
            return self.encoder_.predict(X)
        elif domain in ["src", "source"]:
            return self.encoder_src_.predict(X)
        else:
            raise ValueError("`domain `argument "
                             "should be `tgt` or `src`, "
                             "got, %s"%domain)
        
        
    def predict(self, X, domain="tgt"):
        """
        Return predictions of the task network on the encoded features.
        
        Parameters
        ----------
        X : array
            Input data
            
        domain : str (default="tgt")
            If domain is ``"tgt"`` or ``"target"``,
            outputs of ``encoder_`` are used.
            If domain is ``"src"`` or ``"source"``,
            outputs of ``encoder_src_`` are used.
            
        Returns
        -------
        y_pred : array
            predictions of task network
        """
        X = check_one_array(X)
        return self.task_.predict(self.predict_features(X, domain))
    
    
    def predict_disc(self, X, domain="tgt"):
        """
        Return predictions of the discriminator on the encoded features.
        
        Parameters
        ----------
        X : array
            Input data
            
        domain : str (default="tgt")
            If domain is ``"tgt"`` or ``"target"``,
            outputs of ``encoder_`` are used.
            If domain is ``"src"`` or ``"source"``,
            outputs of ``encoder_src_`` are used.
            
        Returns
        -------
        y_disc : array
            predictions of discriminator network
        """
        X = check_one_array(X)
        return self.discriminator_.predict(self.predict_features(X, domain))

    
    
    
class DeepCORAL(BaseDeepFeature):
    """
    DeepCORAL: Deep CORrelation ALignment
    
    DeepCORAL is an extension of CORAL method. It learns a nonlinear
    transformation which aligns correlations of layer activations in
    deep neural networks.
    
    The method consists in training both an **encoder** and a **task**
    network. The **encoder** network maps input features into new
    encoded ones on which the **task** network is trained.
    
    The parameters of the two networks are optimized in order to
    minimize the following loss function:
    
    .. math::
    
        \mathcal{L} = \mathcal{L}_{task} + \\lambda ||C_S - C_T||_F^2
        
    Where:
    
    - :math:`\mathcal{L}_{task}` is the task loss computed with
      source labeled data.
    - :math:`C_S` is the correlation matrix of source data in the
      encoded feature space.
    - :math:`C_T` is the correlation matrix of target data in the
      encoded feature space.
    - :math:`||.||_F` is the Frobenius norm.
    - :math:`\\lambda` is a trade-off parameter.
    
    Thus the **encoder** network learns a new feature representation
    on wich the correlation matrixes of source and target data are
    "close" and where a **task** network is able to learn the task
    with source labeled data.
    
    Notice that DeepCORAL only uses labeled source and unlabeled target
    data. It belongs then to "unsupervised" domain adaptation methods.
    
    .. figure:: ../_static/images/deepcoral.png
        :align: center
        
        DeepCORAL architecture (source: [1])
    
    Parameters
    ----------
    encoder : tensorflow Model (default=None)
        Encoder netwok. If ``None``, a shallow network with 10
        neurons and ReLU activation is used as encoder network.
        
    task : tensorflow Model (default=None)
        Task netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as task network.
        
    lambda_ : float (default=1.)
        Trade-off parameter.

    loss : string or tensorflow loss (default="mse")
        Loss function used for the task.
        
    metrics : dict or list of string or tensorflow metrics (default=None)
        Metrics given to the model. Metrics are used
        on ``task`` outputs.
        
    optimizer : string or tensorflow optimizer (default=None)
        Optimizer of the model. If ``None``, the
        optimizer is set to tf.keras.optimizers.Adam(0.001)
        
    copy : boolean (default=True)
        Whether to make a copy of ``encoder``
        and ``task`` or not.
        
    random_state : int (default=None)
        Seed of random generator.
    
    Attributes
    ----------
    encoder_ : tensorflow Model
        encoder network.
        
    task_ : tensorflow Model
        task network.
    
    model_ : tensorflow Model
        Fitted model: the union of ``encoder_``
        and ``task_`` networks.
        
    history_ : dict
        history of the losses and metrics across the epochs.
        If ``yt`` is given in ``fit`` method, target metrics
        and losses are recorded too.
        
    Examples
    --------
    >>> import numpy as np
    >>> from adapt.feature_based import DeepCORAL
    >>> np.random.seed(0)
    >>> Xs = np.random.multivariate_normal(
    ...      np.array([0, 0]), np.array([[0.001, 0], [0, 1]]), 100)
    >>> Xt = np.random.multivariate_normal(
    ...      np.array([0, 0]), np.array([[0.1, 0.2], [0.2, 0.5]]), 100)
    >>> ys = np.zeros(100)
    >>> yt = np.zeros(100)
    >>> model = DeepCORAL(lambda_=0., random_state=0)
    >>> model.fit(Xs, ys, Xt, yt, epochs=500, batch_size=100, verbose=0)
    >>> model.history_["task_t"][-1]
    1.30188e-05
    >>> model = DeepCORAL(lambda_=1., random_state=0)
    >>> model.fit(Xs, ys, Xt, yt, epochs=500, batch_size=100, verbose=0)
    >>> model.history_["task_t"][-1]
    5.4704474e-06
        
    See also
    --------
    CORAL
    DANN
    ADDA

    References
    ----------
    .. [1] `[1] <https://arxiv.org/pdf/1607.01719.pdf>`_ Sun B. and Saenko K. \
"Deep CORAL: correlation alignment for deep domain adaptation." In ICCV, 2016.
    """
    def __init__(self, 
                 encoder=None,
                 task=None,
                 lambda_=1.,
                 loss="mse",
                 metrics=None,
                 optimizer=None,
                 copy=True,
                 random_state=None):
        
        self.lambda_ = lambda_    
        super().__init__(encoder, task, None,
                         loss, metrics, optimizer, copy,
                         random_state)

        
    def fit(self, Xs, ys, Xt, yt=None, **fit_params):
        self._fit(Xs, ys, Xt, yt, **fit_params)
        return self
    
    
    def create_model(self, inputs_Xs, inputs_Xt):
               
        encoded_src = self.encoder_(inputs_Xs)
        encoded_tgt = self.encoder_(inputs_Xt)
        
        batch_size = K.mean(K.sum(K.ones_like(inputs_Xs), 0))
        dim = len(encoded_src.shape)
        
        if dim != 2:
            raise ValueError("Encoded space should "
                             "be 2 dimensional, got, "
                             "%s"%encoded_src.shape)
            
        task_src = self.task_(encoded_src)
        task_tgt = self.task_(encoded_tgt)
        
        factor_1 = 1 / (batch_size - 1 + EPS)
        factor_2 = 1 / batch_size
        
        sum_src = K.sum(encoded_src, axis=0)
        sum_src_row = K.reshape(sum_src, (1, -1))
        sum_src_col = K.reshape(sum_src, (-1, 1))
        
        cov_src = factor_1 * (
            K.dot(K.transpose(encoded_src), encoded_src) -
            factor_2 * K.dot(sum_src_col, sum_src_row)
        )
        
        sum_tgt = K.sum(encoded_tgt, axis=0)
        sum_tgt_row = K.reshape(sum_tgt, (1, -1))
        sum_tgt_col = K.reshape(sum_tgt, (-1, 1))
        
        cov_tgt = factor_1 * (
            K.dot(K.transpose(encoded_tgt), encoded_tgt) -
            factor_2 * K.dot(sum_tgt_col, sum_tgt_row)
        )
        
        outputs = dict(task_src=task_src,
                       task_tgt=task_tgt,
                       cov_src=cov_src,
                       cov_tgt=cov_tgt)
        return outputs


    def get_loss(self, inputs_ys,
                  task_src, task_tgt,
                  cov_src, cov_tgt):
        
        loss_task = self.loss_(inputs_ys, task_src)
        loss_disc = 0.25 * K.mean(K.square(subtract([cov_src, cov_tgt])))
        loss_disc_lambda = self.lambda_ * loss_disc
        
        loss = K.mean(loss_task) + loss_disc_lambda
        return loss
    
    
    def get_metrics(self, inputs_ys, inputs_yt,
                     task_src, task_tgt,
                     cov_src, cov_tgt):
        metrics = {}
        
        task_s = self.loss_(inputs_ys, task_src)
        disc = 0.25 * K.mean(K.square(subtract([cov_src, cov_tgt])))
        
        metrics["task_s"] = K.mean(task_s)
        metrics["disc"] = self.lambda_ * K.mean(disc)
        if inputs_yt is not None:
            task_t = self.loss_(inputs_yt, task_tgt)
            metrics["task_t"] = K.mean(task_t)
        
        names_task, names_disc = self._get_metric_names()
        
        for metric, name in zip(self.metrics_task_, names_task):
            metrics[name + "_s"] = metric(inputs_ys, task_src)
            if inputs_yt is not None:
                metrics[name + "_t"] = metric(inputs_yt, task_tgt)
        return metrics
    
    
    
class MCD(BaseDeepFeature):
    """
    MCD: Maximum Classifier Discrepancy is a feature-based domain adaptation
    method originally introduced for unsupervised classification DA.
    
    The goal of MCD is to find a new representation of the input features which
    minimizes the discrepancy between the source and target domains 
    
    The discrepancy is estimated through adversarial training of three networks:
    An encoder and two classifiers. These two learn the task on the source domains
    and are used to compute the discrepancy. A reversal layer is placed between
    the encoder and the two classifiers to perform adversarial training.
    
    Parameters
    ----------
    encoder : tensorflow Model (default=None)
        Encoder netwok. If ``None``, a shallow network with 10
        neurons and ReLU activation is used as encoder network.
        
    get_task : tensorflow Model (default=None)
        Task netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as task network.
        
    is_pretrained : boolean (default=False)
        Specify if the `encoder` and `task` networks are already
        pretrained on source or not.

    loss : string or tensorflow loss (default="mse")
        Loss function used for the task.
        
    metrics : dict or list of string or tensorflow metrics (default=None)
        Metrics given to the model. If a list is provided,
        metrics are used on both ``task`` and ``discriminator``
        outputs. To give seperated metrics, please provide a
        dict of metrics list with ``"task"`` and ``"disc"`` as keys.
        
    optimizer : string or tensorflow optimizer (default=None)
        Optimizer of the model. If ``None``, the
        optimizer is set to tf.keras.optimizers.Adam(0.001)
        
    optimizer_src : string or tensorflow optimizer (default=None)
        Optimizer for the pretraining on source. If ``None``,
        ``optimizer_src`` is a copy of ``optimizer``.
        
    copy : boolean (default=True)
        Whether to make a copy of ``encoder``, ``task`` and
        ``discriminator`` or not.
        
    random_state : int (default=None)
        Seed of random generator.
    
    Attributes
    ----------
    encoder_ : tensorflow Model
        encoder network.
        
    task_ : tensorflow Model
        Principal task network.
        
    task_sec_ : tensorflow Model
        Secondary task network.
    
    model_ : tensorflow Model
        Fitted model: the union of ``encoder_``, ``task_``,
        ``task_sec_`` and ``discriminator_`` networks.
        
    model_src_ : tensorflow Model
        Fitted model: the union of ``encoder_``, ``task_``
        and ``task_sec_`` networks.
        
    history_ : dict
        history of the losses and metrics across the epochs.
        If ``yt`` is given in ``fit`` method, target metrics
        and losses are recorded too.
        
    history_src_ : dict
        Source model history of the losses and metrics
        across the epochs. If ``yt`` is given in ``fit``
        method, target metrics and losses are recorded too.
        
    is_pretrained_ : boolean
        Specify if the encoder is already pretrained on
        source or not. If True, the ``fit`` method will
        avoid the pretraining step.
        
    Examples
    --------
    >>> Xs = np.concatenate((np.random.random((100, 1)),
    ...                      np.zeros((100, 1))), 1)
    >>> Xt = np.concatenate((np.random.random((100, 1)),
    ...                      np.ones((100, 1))), 1)
    >>> ys = 0.2 * Xs[:, 0]
    >>> yt = 0.2 * Xt[:, 0]
    >>> model = MCD(random_state=0)
    >>> model.fit(Xs, ys, Xt, yt, epochs=100, verbose=0)
    >>> model.history_src_["task_t"][-1]
    0.0234...
    >>> model.history_["task_t"][-1]
    0.0009...
        
    References
    ----------
    .. [1] `[1] <https://arxiv.org/pdf/1702.05464.pdf>`_ K. Saito, K. Watanabe, \
Y. Ushiku, and T. Harada. "Maximum  classifier  discrepancy  for  unsupervised  \
domain adaptation". In CVPR, 2018.
    """
    def __init__(self, 
                 encoder=None,
                 task=None,
                 is_pretrained=False,
                 lambda_=1.,
                 loss="mse",
                 metrics=None,
                 optimizer=None,
                 optimizer_src=None,
                 copy=True,
                 random_state=None):

        super().__init__(encoder, task, None,
                         loss, metrics, optimizer, copy,
                         random_state)
        self.is_pretrained_ = is_pretrained
        self.lambda_ = lambda_
        
        if optimizer_src is None:
            self.optimizer_src = deepcopy(self.optimizer)
        else:
            self.optimizer_src = optimizer_src
            
        self.task_sec_ = check_network(self.task_, 
                                       copy=True,
                                       display_name="task",
                                       force_copy=True)
        self.task_sec_._name = self.task_sec_._name + "_2"

        
    def fit_source(self, Xs, ys, Xt=None, yt=None, **fit_params):
        np.random.seed(self.random_state)
        tf.random.set_seed(self.random_state)
                
        # Call predict to avoid strange behaviour with
        # Sequential model whith unspecified input_shape
        zeros_enc_ = self.encoder_.predict(np.zeros((1,) + Xs.shape[1:]));
        self.task_.predict(zeros_enc_);
        
        self.model_src_ = Sequential()
        self.model_src_.add(self.encoder_)
        self.model_src_.add(self.task_)
        self.model_src_.compile(loss=self.loss_,
                                metrics=self.metrics_task_,
                                optimizer=self.optimizer_src)
        
        if (Xt is not None and yt is not None and 
            not "validation_data" in fit_params):
            hist = self.model_src_.fit(Xs, ys,
                                       validation_data=(Xt, yt),
                                       **fit_params)
        else:
            hist = self.model_src_.fit(Xs, ys, **fit_params)
        
        for k, v in hist.history.items():
            if not hasattr(self, "history_src_"):
                self.history_src_ = {}
            self.history_src_[k] = self.history_src_.get(k, []) + v            
            
        self.task_sec_.predict(zeros_enc_);
#         Add a small noise on weights to avoid task and task_sec
#         being identical.
        weights = self.task_.get_weights()
        for i in range(len(weights)):
            weights[i] += (0.01 * weights[i] *
                           np.random.standard_normal(weights[i].shape))
        self.task_sec_.set_weights(weights)
        return self


    def fit_target(self, Xs, ys, Xt, yt=None, **fit_params):
        self._fit(Xs, ys, Xt, yt, **fit_params)
        return self
        
    
    def fit(self, Xs, ys, Xt, yt=None, fit_params_src=None, **fit_params):  
        if fit_params_src is None:
            fit_params_src = fit_params
        
        Xs, ys, Xt, yt = check_arrays(Xs, ys, Xt, yt)
        
        if not self.is_pretrained_:
            self.fit_source(Xs, ys, Xt, yt, **fit_params_src)
            self.is_pretrained_ = True
        
        self.fit_target(Xs, ys, Xt, yt, **fit_params)
        return self
    
    
    def create_model(self, inputs_Xs, inputs_Xt):

        encoded_src = self.encoder_(inputs_Xs)
        encoded_tgt = self.encoder_(inputs_Xt)
        
        task_src = GradientHandler(0., name="gh_0")(encoded_src)
        task_sec_src = GradientHandler(0., name="gh_1")(encoded_src)
        task_src = self.task_(task_src)
        task_sec_src = self.task_sec_(task_sec_src)
        
        task_tgt = GradientHandler(-self.lambda_, name="gh_2")(encoded_tgt)
        task_sec_tgt = GradientHandler(-self.lambda_, name="gh_3")(encoded_tgt)
        task_tgt = self.task_(task_tgt)
        task_sec_tgt = self.task_sec_(task_sec_tgt)
        
        outputs = dict(task_src=task_src,
                       task_tgt=task_tgt,
                       task_sec_src=task_sec_src,
                       task_sec_tgt=task_sec_tgt)
        return outputs


    def get_loss(self, inputs_ys, task_src,
                  task_tgt, task_sec_src, task_sec_tgt):
        
        loss_task = 0.5 * (self.loss_(inputs_ys, task_src) + self.loss_(inputs_ys, task_sec_src))

        loss_disc = K.mean(K.abs(subtract([task_tgt, task_sec_tgt])), axis=-1)
        
        loss = K.mean(loss_task) - K.mean(loss_disc)
        return loss
    
    
    def get_metrics(self, inputs_ys, inputs_yt,
                     task_src, task_tgt,
                     task_sec_src, task_sec_tgt):
        metrics = {}
        
        disc = K.abs(K.mean(subtract([task_tgt, task_sec_tgt]), axis=-1))
        task_s = self.loss_(inputs_ys, task_src)
        
        metrics["task_s"] = K.mean(task_s)
        metrics["disc"] = K.mean(disc)
        if inputs_yt is not None:
            task_t = self.loss_(inputs_yt, task_tgt)
            metrics["task_t"] = K.mean(task_t)
        
        names_task, names_disc = self._get_metric_names()
        
        for metric, name in zip(self.metrics_task_, names_task):
            metrics[name + "_s"] = metric(inputs_ys, task_src)
            if inputs_yt is not None:
                metrics[name + "_t"] = metric(inputs_yt, task_tgt)
                
        for metric, name in zip(self.metrics_disc_, names_disc):
            metrics[name] = metric(task_tgt, task_sec_tgt)
        return metrics
    
    
    
class MDD(BaseDeepFeature):
    """
    MDD: Margin Disparity Discrepancy is a feature-based domain adaptation
    method originally introduced for unsupervised classification DA.
    
    The goal of MDD is to find a new representation of the input features which
    minimizes the disparity discrepancy between the source and target domains 
    
    The discrepancy is estimated through adversarial training of three networks:
    An encoder a task network and a discriminator.
    
    Parameters
    ----------
    encoder : tensorflow Model (default=None)
        Encoder netwok. If ``None``, a shallow network with 10
        neurons and ReLU activation is used as encoder network.
        
    get_task : tensorflow Model (default=None)
        Task netwok. If ``None``, a two layers network with 10
        neurons per layer and ReLU activation is used as task network.
        
    gamma : float (default=4.)
        Margin parameter.

    loss : string or tensorflow loss (default="mse")
        Loss function used for the task.
        
    metrics : dict or list of string or tensorflow metrics (default=None)
        Metrics given to the model. If a list is provided,
        metrics are used on both ``task`` and ``discriminator``
        outputs. To give seperated metrics, please provide a
        dict of metrics list with ``"task"`` and ``"disc"`` as keys.
        
    optimizer : string or tensorflow optimizer (default=None)
        Optimizer of the model. If ``None``, the
        optimizer is set to tf.keras.optimizers.Adam(0.001)
        
    copy : boolean (default=True)
        Whether to make a copy of ``encoder``, ``task`` and
        ``discriminator`` or not.
        
    random_state : int (default=None)
        Seed of random generator.
    
    Attributes
    ----------
    encoder_ : tensorflow Model
        encoder network.
        
    task_ : tensorflow Model
        Principal task network.
        
    task_adv_ : tensorflow Model
        Adversarial task network.
    
    model_ : tensorflow Model
        Fitted model: the union of ``encoder_``, ``task_``,
        and ``discriminator_`` networks.
        
    history_ : dict
        history of the losses and metrics across the epochs.
        If ``yt`` is given in ``fit`` method, target metrics
        and losses are recorded too.
        
    Examples
    --------
    >>> Xs = np.concatenate((np.random.random((100, 1)),
    ...                      np.zeros((100, 1))), 1)
    >>> Xt = np.concatenate((np.random.random((100, 1)),
    ...                      np.ones((100, 1))), 1)
    >>> ys = 0.2 * Xs[:, 0]
    >>> yt = 0.2 * Xt[:, 0]
    >>> model = MDD(random_state=0)
    >>> model.fit(Xs, ys, Xt, yt, epochs=100, verbose=0)
    >>> model.history_["task_t"][-1]
    0.0009...
        
    References
    ----------
    .. [1] `[1] <https://arxiv.org/pdf/1702.05464.pdf>`_ Y. Zhang, \
T. Liu, M. Long, and M. Jordan. "Bridging theory and algorithm for \
domain adaptation". ICML, 2019.
    """
    def __init__(self, 
                 encoder=None,
                 task=None,
                 is_pretrained=False,
                 lambda_=1.,
                 gamma=4.,
                 loss="mse",
                 metrics=None,
                 optimizer=None,
                 optimizer_src=None,
                 copy=True,
                 random_state=None):

        super().__init__(encoder, task, None,
                         loss, metrics, optimizer, copy,
                         random_state)
        self.lambda_ = lambda_
        self.gamma = gamma
        
        if optimizer_src is None:
            self.optimizer_src = deepcopy(self.optimizer)
        else:
            self.optimizer_src = optimizer_src

        self.discriminator_ = check_network(self.task_, 
                                       copy=True,
                                       display_name="task",
                                       force_copy=True)
        self.discriminator_._name = self.discriminator_._name + "_2"
        
        if hasattr(self.loss_, "__name__"):
            self.loss_name_ = self.loss_.__name__
        elif hasattr(self.loss_, "__class__"):
            self.loss_name_ = self.loss_.__class__.__name__
        else:
            self.loss_name_ = ""

      
    def create_model(self, inputs_Xs, inputs_Xt):

        encoded_src = self.encoder_(inputs_Xs)
        encoded_tgt = self.encoder_(inputs_Xt)

        task_src = self.task_(encoded_src)
        task_tgt = self.task_(encoded_tgt)
        
        task_src_nograd = GradientHandler(0., name="gh_2")(task_src)
        task_tgt_nograd = GradientHandler(0., name="gh_3")(task_tgt)
        
        # TODO, add condition for bce and cce     
#         if self.loss_name_ in ["categorical_crossentropy",
#                                "CategoricalCrossentropy"]:

        disc_src = GradientHandler(-self.lambda_, name="gh_0")(encoded_src)
        disc_tgt = GradientHandler(-self.lambda_, name="gh_1")(encoded_tgt)
        disc_src = self.discriminator_(disc_src)
        disc_tgt = self.discriminator_(disc_tgt)

        outputs = dict(task_src=task_src,
                       task_tgt=task_tgt,
                       task_src_nograd=task_src_nograd,
                       task_tgt_nograd=task_tgt_nograd,
                       disc_src=disc_src,
                       disc_tgt=disc_tgt)
        return outputs


    def get_loss(self, inputs_ys, task_src,
                 task_src_nograd, task_tgt_nograd,
                 task_tgt, disc_src, disc_tgt):
        
        task_loss = self.loss_(inputs_ys, task_src)
        
        disc_loss_src = self.loss_(task_src_nograd, disc_src)
        disc_loss_tgt = self.loss_(task_tgt_nograd, disc_tgt)
        
        disc_loss = disc_loss_tgt - self.gamma * disc_loss_src
        
        loss = K.mean(task_loss) - K.mean(disc_loss)
        return loss


    def get_metrics(self, inputs_ys, inputs_yt,
                    task_src, task_tgt,
                    task_src_nograd, task_tgt_nograd,
                    disc_src, disc_tgt):
        metrics = {}
        
        task_s = self.loss_(inputs_ys, task_src)
        disc = (self.loss_(task_tgt_nograd, disc_tgt) -
                self.gamma * self.loss_(task_src_nograd, disc_src))
        
        metrics["task_s"] = K.mean(task_s)
        metrics["disc"] = K.mean(disc)
        if inputs_yt is not None:
            task_t = self.loss_(inputs_yt, task_tgt)
            metrics["task_t"] = K.mean(task_t)
        
        names_task, names_disc = self._get_metric_names()
        
        for metric, name in zip(self.metrics_task_, names_task):
            metrics[name + "_s"] = metric(inputs_ys, task_src)
            if inputs_yt is not None:
                metrics[name + "_t"] = metric(inputs_yt, task_tgt)
                
        for metric, name in zip(self.metrics_disc_, names_disc):
            metrics[name] = (metric(task_tgt_nograd, disc_tgt) -
                self.gamma * metric(task_src_nograd, disc_src))
        return metrics
