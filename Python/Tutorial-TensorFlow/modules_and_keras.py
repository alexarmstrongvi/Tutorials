################################################################################
# Keras
################################################################################
print(f"\n===== Running {__file__} =====\n")

from typing import List, Tuple
import tensorflow as tf
from tensorflow import keras
import numpy as np

################################################################################
# Tensorflow Modules (tf.Module)
################################################################################
class MyModule(tf.Module):
    def __init__(self, name=None):
        super().__init__(name=name)
        
    def __call__(self, x):
        return x
    
my_module = MyModule(name='my_module')

# Attributes
# my_module.name
# my_module.name_scope
# my_module.submodules
# my_module.trainable_variables
# my_module.variables

# Methods
# my_module.with_name_scope()

################################################################################
# Layer API (tf.keras.layers)
################################################################################
class MyLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    #def build(self):
    
    def call(self, x):
        return x

my_layer = MyLayer()

# Attributes added from Module
# my_layer.dtype                   # e.g. float32
# my_layer.dtype_policy            # e.g. <Policy "float32">
# my_layer.variable_dtype          # e.g. float32
# my_layer.compute_dtype           # e.g. float32

# my_layer.built                   # e.g. False
# my_layer.dynamic                 # e.g. False
# my_layer.stateful                # e.g. False
# my_layer.supports_masking        # e.g. False
# my_layer.trainable               # e.g. True

# my_layer.inbound_nodes           # e.g. []
# my_layer.weights                 # e.g. []
# my_layer.trainable_weights       # e.g. []
# my_layer.non_trainable_weights   # e.g. []
# my_layer.non_trainable_variables # e.g. []
# my_layer.metrics                 # e.g. []
# my_layer.updates                 # e.g. []
# my_layer.outbound_nodes          # e.g. []
# my_layer.losses                  # e.g. []

# References
# my_layer.activity_regularizer    # e.g. None
# my_layer.input_spec              # e.g. None

# Methods
# my_layer.add_loss()
# my_layer.add_metric()
# my_layer.add_update()
# my_layer.add_variable()
# my_layer.add_weight()
# my_layer.apply()
# my_layer.build()
# my_layer.call()
# my_layer.compute_mask()
# my_layer.compute_output_shape()
# my_layer.compute_output_signature()
# my_layer.count_params()
# my_layer.from_config()
# my_layer.get_config()
# my_layer.get_input_at()
# my_layer.get_input_mask_at()
# my_layer.get_input_shape_at()
# my_layer.get_losses_for()
# my_layer.get_output_at()
# my_layer.get_output_mask_at()
# my_layer.get_output_shape_at()
# my_layer.get_updates_for()
# my_layer.get_weights()
# my_layer.set_weights()

################################################################################
# Models (tf.keras.Model)
################################################################################
#tf.keras.Model(inputs=tf.keras.Input(...), outputs=...) or 
loss_and_metrics = Tuple[float, List[float]]
class MyLayer(keras.layers.Layer):
    def __init__(self):
        super().__init__()
        self.constant  = tf.constant(3.14, dtype=tf.float32s)
        self.variable  = tf.Variable(1.0, trainable=False, dtype=tf.float32)
        self.weight1   = tf.Variable(1.0, dtype=tf.float32)
        self.weight2   = self.add_weight(shape=(3,3), initializer=tf.random_uniform_initializer())

    def build(self, input_shape: tf.TensorShape) -> None:
        self.weight3 = tf.add_weight(shape=(2,), initializer=tf.ones_initializer())
        pass

    def call(self, inputs: tf.Tensor, training: bool, *args, **kwargs) -> tf.Tensor:
        # self.add_loss()
        return inputs

    # def get_config(self):
    #     return {}

    # @property
    # def weights(self):
    #     pass

    # @property
    # def non_trainable_weights(self):
    #     pass

    # @property
    # def trainable_weights(self):
    #     pass

class MyModel(tf.keras.Model):
    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.my_layer

    def compile(optimizer, loss, metrics):
        pass

    def fit(
        inputs, 
        targets, 
        epochs, 
        batch_size,
        validation_data,
    ) -> tf.keras.callbacks.History:
        super().fit()
        pass

    def train_step():
        pass

    def test_step():
        pass

    def build():
        pass

    def call():
        pass

    def evaluate(inputs, targets, batch_size) -> loss_and_metrics:
        pass

    def predict(inputs, batch_size) -> tf.Tensor:
        pass


my_model = MyModel(name='my_model')

# Attributes added from Layer
# my_model.run_eagerly          # e.g. False
# my_model.stop_training        # e.g. False

# my_model.layers               # e.g. []
# my_model.metrics_names        # e.g. []
# my_model.state_updates        # e.g. []

# References
# my_model.compiled_loss        # e.g. None
# my_model.compiled_metrics     # e.g. None
# my_model.distribute_strategy  # e.g. <tensorflow.python.distribute.distribute_lib._DefaultDistributionStrategy object at 0x7fa481a70b80>
# my_model.history              # e.g. None
# my_model.input_names          # e.g. None
# my_model.inputs               # e.g. None
# my_model.optimizer            # e.g. None
# my_model.output_names         # e.g. None
# my_model.outputs              # e.g. None
# my_model.predict_function     # e.g. None
# my_model.test_function        # e.g. None
# my_model.train_function       # e.g. None

# Methods
# my_model.compile()
# my_model.evaluate()
# my_model.evaluate_generator()
# my_model.fit()
# my_model.fit_generator()
# my_model.get_layer()
# my_model.load_weights()
# my_model.make_predict_function()
# my_model.make_test_function()
# my_model.make_train_function()
# my_model.predict()
# my_model.predict_generator()
# my_model.predict_on_batch()
# my_model.predict_step()
# my_model.reset_metrics()
# my_model.reset_states()
# my_model.save()
# my_model.save_weights()
# my_model.summary()
# my_model.test_on_batch()
# my_model.test_step()
# my_model.to_json()
# my_model.to_yaml()
# my_model.train_on_batch()
# my_model.train_step()

# Sequential Models
# tf.keras.Sequential


################################################################################
# Built-in Layers (tf.keras.layers)
################################################################################

# Dense NN
# tf.keras.layers.Dense()
# tf.keras.layers.Dropout()

# Convolutional NN
# tf.keras.layers.Conv2D()
# tf.keras.layers.AveragePooling2D()
# tf.keras.layers.MaxPool2D()
# tf.keras.layers.Flatten()

# Unsorted
# tf.keras.layers.AbstractRNNCell()
# tf.keras.layers.Activation()
# tf.keras.layers.ActivityRegularization()
# tf.keras.layers.Add()
# tf.keras.layers.AdditiveAttention()
# tf.keras.layers.AlphaDropout()
# tf.keras.layers.Attention()
# tf.keras.layers.Average()
# tf.keras.layers.AveragePooling1D()
# tf.keras.layers.AveragePooling3D()
# tf.keras.layers.AvgPool1D()
# tf.keras.layers.AvgPool2D()
# tf.keras.layers.AvgPool3D()
# tf.keras.layers.BatchNormalization()
# tf.keras.layers.Bidirectional()
# tf.keras.layers.Concatenate()
# tf.keras.layers.Conv1D()
# tf.keras.layers.Conv1DTranspose()
# tf.keras.layers.Conv2DTranspose()
# tf.keras.layers.Conv3D()
# tf.keras.layers.Conv3DTranspose()
# tf.keras.layers.ConvLSTM2D()
# tf.keras.layers.Convolution1D()
# tf.keras.layers.Convolution1DTranspose()
# tf.keras.layers.Convolution2D()
# tf.keras.layers.Convolution2DTranspose()
# tf.keras.layers.Convolution3D()
# tf.keras.layers.Convolution3DTranspose()
# tf.keras.layers.Cropping1D()
# tf.keras.layers.Cropping2D()
# tf.keras.layers.Cropping3D()
# tf.keras.layers.DenseFeatures()
# tf.keras.layers.DepthwiseConv2D()
# tf.keras.layers.Dot()
# tf.keras.layers.ELU()
# tf.keras.layers.Embedding()
# tf.keras.layers.GRU()
# tf.keras.layers.GRUCell()
# tf.keras.layers.GaussianDropout()
# tf.keras.layers.GaussianNoise()
# tf.keras.layers.GlobalAveragePooling1D()
# tf.keras.layers.GlobalAveragePooling2D()
# tf.keras.layers.GlobalAveragePooling3D()
# tf.keras.layers.GlobalAvgPool1D()
# tf.keras.layers.GlobalAvgPool2D()
# tf.keras.layers.GlobalAvgPool3D()
# tf.keras.layers.GlobalMaxPool1D()
# tf.keras.layers.GlobalMaxPool2D()
# tf.keras.layers.GlobalMaxPool3D()
# tf.keras.layers.GlobalMaxPooling1D()
# tf.keras.layers.GlobalMaxPooling2D()
# tf.keras.layers.GlobalMaxPooling3D()
# tf.keras.layers.InputLayer()
# tf.keras.layers.InputSpec()
# tf.keras.layers.LSTM()
# tf.keras.layers.LSTMCell()
# tf.keras.layers.Lambda()
# tf.keras.layers.Layer()
# tf.keras.layers.LayerNormalization()
# tf.keras.layers.LeakyReLU()
# tf.keras.layers.LocallyConnected1D()
# tf.keras.layers.LocallyConnected2D()
# tf.keras.layers.Masking()
# tf.keras.layers.MaxPool1D()
# tf.keras.layers.MaxPool3D()
# tf.keras.layers.MaxPooling1D()
# tf.keras.layers.MaxPooling2D()
# tf.keras.layers.MaxPooling3D()
# tf.keras.layers.Maximum()
# tf.keras.layers.Minimum()
# tf.keras.layers.MultiHeadAttention()
# tf.keras.layers.Multiply()
# tf.keras.layers.PReLU()
# tf.keras.layers.Permute()
# tf.keras.layers.RNN()
# tf.keras.layers.ReLU()
# tf.keras.layers.RepeatVector()
# tf.keras.layers.Reshape()
# tf.keras.layers.SeparableConv1D()
# tf.keras.layers.SeparableConv2D()
# tf.keras.layers.SeparableConvolution1D()
# tf.keras.layers.SeparableConvolution2D()
# tf.keras.layers.SimpleRNN()
# tf.keras.layers.SimpleRNNCell()
# tf.keras.layers.Softmax()
# tf.keras.layers.SpatialDropout1D()
# tf.keras.layers.SpatialDropout2D()
# tf.keras.layers.SpatialDropout3D()
# tf.keras.layers.StackedRNNCells()
# tf.keras.layers.Subtract()
# tf.keras.layers.ThresholdedReLU()
# tf.keras.layers.TimeDistributed()
# tf.keras.layers.UpSampling1D()
# tf.keras.layers.UpSampling2D()
# tf.keras.layers.UpSampling3D()
# tf.keras.layers.Wrapper()
# tf.keras.layers.ZeroPadding1D()
# tf.keras.layers.ZeroPadding2D()
# tf.keras.layers.ZeroPadding3D()

################################################################################
# Optimizers (tf.optimizers or tf.keras.optimizers)
################################################################################
# Common
# tf.optimizers.SGD()
# tf.optimizers.Adam()
# tf.opimizers.RMSprop()
 
# Others
# tf.opimizers.Adadelta()
# tf.opimizers.Adagrad()
# tf.opimizers.Adamax()
# tf.opimizers.Ftrl()
# tf.opimizers.Nadam()
# tf.opimizers.Optimizer()
    
################################################################################
# Loss and Metric functions (tf.losses, tf.metrics, tf.keras.losses, tf.keras.metrics)
################################################################################
# Classes (Both)
# BinaryCrossentropy
# CategoricalCrossentropy
# CategoricalHinge
# CosineSimilarity
# Hinge
# KLDivergence
# MeanAbsoluteError
# MeanAbsolutePercentageError
# MeanSquaredError
# MeanSquaredLogarithmicError
# Poisson
# SparseCategoricalCrossentropy
# SquaredHing

# Classes (Only Losses)
# tf.losses.Huber()
# tf.losses.LogCosh()
# tf.losses.Loss()
# tf.losses.Reduction()
    
# Classes (Only Metric)
# tf.metrics.AUC()
# tf.metrics.Accuracy()
# tf.metrics.BinaryAccuracy()
# tf.metrics.CategoricalAccuracy()
# tf.metrics.FalseNegatives()
# tf.metrics.FalsePositives()
# tf.metrics.LogCoshError()
# tf.metrics.Mean()
# tf.metrics.MeanIoU()
# tf.metrics.MeanRelativeError()
# tf.metrics.MeanTensor()
# tf.metrics.Metric()
# tf.metrics.Precision()
# tf.metrics.PrecisionAtRecall()
# tf.metrics.Recall()
# tf.metrics.RecallAtPrecision()
# tf.metrics.RootMeanSquaredError()
# tf.metrics.SensitivityAtSpecificity()
# tf.metrics.SparseCategoricalAccuracy()
# tf.metrics.SparseTopKCategoricalAccuracy()
# tf.metrics.SpecificityAtSensitivity()
# tf.metrics.Sum()
# tf.metrics.TopKCategoricalAccuracy()
# tf.metrics.TrueNegatives()
# tf.metrics.TruePositives()
    
# Functions (Both)
# KLD()
# MAE()
# MAPE()
# MSE()
# MSLE()
# binary_crossentropy()
# categorical_crossentropy()
# deserialize()
# get()
# hinge()
# kl_divergence()
# kld()
# kullback_leibler_divergence()
# log_cosh()
# logcosh()
# mae()
# mape()
# mean_absolute_error()
# mean_absolute_percentage_error()
# mean_squared_error()
# mean_squared_logarithmic_error()
# mse()
# msle()
# poisson()
# serialize()
# sparse_categorical_crossentropy()
# squared_hinge()
    
# Functions (Only Losses)
# tf.losses.categorical_hinge()
# tf.losses.cosine_similarity()
# tf.losses.huber()

# Functions (Only Metrics)
# tf.metrics.binary_accuracy()
# tf.metrics.categorical_accuracy()
# tf.metrics.sparse_categorical_accuracy()
# tf.metrics.sparse_top_k_categorical_accuracy()
# tf.metrics.top_k_categorical_accuracy()

################################################################################
# Other Keras Submodules
################################################################################
# tf.keras.activations
# tf.keras.applications
# tf.keras.backend
# tf.keras.callbacks
# tf.keras.constraints
# tf.keras.datasets
# tf.keras.estimator
# tf.keras.experimental
# tf.keras.initializers
# tf.keras.mixed_precision
# tf.keras.models
# tf.keras.preprocessing
# tf.keras.regularizers
# tf.keras.utils
# tf.keras.wrappers
