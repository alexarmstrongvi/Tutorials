################################################################################
# TensorFlow basics
################################################################################
print(f"\n===== Running {__file__} =====\n")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import numpy as np

# Configuration
assert(tf.executing_eagerly() == True)

################################################################################
# Tensors
# - immutable
# - basically a wrapper over numpy arrays
################################################################################
#t = tf.Tensor(1, value_index=0, dtype=tf.int8) # How to use?
t_rank0 = tf.constant(1)
t_rank1 = tf.constant([1,2,3])
t_rank2 = tf.constant([[1,2,3],[4,5,6],[7,8,9]])
assert(tf.is_tensor(t_rank0))

########################################
# Attributes
########################################
assert(t_rank2.ndim == 2)
assert(t_rank2.shape == (3,3)) # get_shape()
assert(t_rank2.dtype == tf.int32)
assert(t_rank2.is_packed == False)
#print(t_rank2.device) # e.g. /job:localhost/replica:0/task:0/device:CPU:0
#print(t_rank2.backing_device)
# t.eval()
# t.ref()
# t.set_shape()
# Graph execution attributes : graph, name, op, value_index, consumers()

# Other properties
assert(tf.size(t_rank2).numpy() == 3*3)

# TensorShape
ts = t_rank2.shape
assert(type(ts) == tf.TensorShape)
#ts.as_list
#ts.dims
#ts.is_fully_defined
#ts.ndims
#ts.num_elements
#ts.rank
# and others...

# Data types (tf.dtypes)
assert(type(tf.float32 == tf.DType))
# tf.int8,   tf.int16,  tf.int32,  tf.int64
# tf.qint8,  tf.qint16, tf.qint32
# tf.quint8, tf.quint16
# tf.uint8,  tf.uint16, tf.uint32, tf.uint64
# tf.bool
# tf.float16, tf.float32, tf.float64; tf.half = tf.float16
# tf.bfloat16
# tf.double
# tf.complex, tf.complex64, tf.complex128
# tf.string

# Other tensor constructors
# tf.convert_to_tensor()
# tf.range()
# tf.linspace()
# tf.eye()
# tf.ones()
# tf.ones_like()
# tf.zeros()
# tf.zeros_like()
# tf.fill()
# tf.identity()
# tf.identity_n()
# tf.constant_initializer()
# tf.ones_initializer()
# tf.zeros_initializer()

# Other Tensor Types
# tf.SparseTensor
# tf.RaggedTensor - variable number of elements along an axis

########################################
# Viewing
########################################

# Indexing (same as numpy except you CANNOT select arbitrary items with array indexing)

########################################
# Modifying
########################################
# Conversions
assert(np.all(np.array(t_rank2) == t_rank2.numpy()))
# tf.as_dtype(), tf.cast()

# Reshaping
# tf.reshape(t, [1,3])
# tf.stack()
# tf.one_hot()

########################################
# Math operations
########################################
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[4, 5], [6, 7]])

# Built-in
z = a + b
z = a - b
z = a * b
z = a / b
z = a @ b

# # Arithmatic
# tf.add, tf.subtract
# tf.multiply, tf.divide, tf.truediv
# tf.pow, tf.square, tf.sqrt, tf.exp

# # Trig
# tf.sin, tf.asin, tf.sinh, tf.asinh
# tf.cos, tf.acos, tf.cosh, tf.acosh
# tf.tan, tf.atan, tf.tanh, tf.atanh, tf.atan2

# # Comparison
# tf.equal, tf.not_equal
# tf.greater, tf.greater_equal
# tf.less, tf.less_equal

# tf.maximum, tf.minimum
# tf.argmax, tf.argmin
# tf.logical_and, tf.logical_notm, tf.logical_or()

# # Linear Algebra (tf.linalg)
# tf.matmul or '@'
# tf.scalar_mul
# tf.eig
# tf.eigvals
# tf.einsum
# tf.norm
# tf.tensordot
# tf.linalg.trace
# tf.linalg.det
# # many others...
# # x = {f for f in dir(tf.linalg) if not f.startswith('_')}
# # x - {f for f in dir(tf) if not f.startswith('_')}

# # Map
# tf.abs
# tf.floor
# tf.round
# tf.negative
# tf.sign
# tf.sigmoid()
# tf.cumsum()

# # Reduce
# tf.reduce_all, tf.reduce_any()
# tf.reduce_max, tf.reduce_min
# tf.reduce_sum(), tf.add_n()
# tf.reduce_mean
# tf.reduce_prod
# tf.reduce_logsumexp

# # Math module (tf.math)
# tf.math.log
# tf.math.mod
# tf.math.ceil
# tf.math.reciprocal()
# tf.math.reduce_std()
# # many others...
# # x = {f for f in dir(tf.math) if not f.startswith('_')}
# # x - {f for f in dir(tf) if not f.startswith('_')}

# Strings (tf.strings)
# tf.as_string
# tf.split
# tf.strings.format
# tf.strings.join
# tf.strings.length
# tf.strings.lower
# tf.strings.ngrams
# tf.strings.reduce_join
# tf.strings.regex_full_match
# tf.strings.regex_replace
# tf.strings.strip
# tf.strings.substr
# tf.strings.to_number
# tf.strings.upper
# and many others...

# Broadcasting (same as numpy)

################################################################################
# Random number generation (tf.random)
################################################################################
#tf.random.create_rng_state
#tf.random.set_seed

#tf.random.shuffle()

# Distributions
#t = tf.random.normal([10])
#tf.random.truncated_normal
#tf.random.stateless_normal
#tf.random.stateless_truncated_normal
#tf.random.stateless_parameterized_truncated_normal
#tf.random_normal_initializer

#tf.random.uniform
#tf.random.stateless_uniform
#tf.random_uniform_initializer

#tf.random.poisson
#tf.random.stateless_poisson

#tf.random.gamma
#tf.random.stateless_gamma

#tf.random.categorical
#tf.random.stateless_categorical

#tf.random.stateless_binomial

