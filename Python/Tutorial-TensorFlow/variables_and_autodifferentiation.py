# Silence warning about recompiling tensorflow to use more optimal CPU instructions
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

################################################################################
# TensorFlow Variables and Autodiff
################################################################################
print(f"\n===== Running {__file__} =====\n")

import tensorflow as tf
import numpy as np

################################################################################
# Variables
# - shared, persistent state your program manipulates
# - same API as tensors with small differences
#     - special functions needed to modify variables as tensor operations create copies
################################################################################
# Uncomment to see where your variables get placed
# tf.debugging.set_log_device_placement(True)
v = tf.Variable(1)
print(v)

# Attributes not found in Tensor
# v.trainable       (e.g. = True)
# v.initializer     (e.g. = None)
# v.constraint      (e.g. = None)
# v.handle          (e.g. = tf.Tensor(<unprintable>, shape=(), dtype=resource))
# v.aggregation     (e.g. = VariableAggregation.NONE)
# v.synchronization (e.g. = VariableSynchronization.AUTO)

# Getters
# v.value()
# v.is_initialized()

# Modifying
# v.assign()
# v.assign_add()
# v.assign_sub()

################################################################################
# Gradients and autodifferentiation
# - GradientTape context records computations that go into each tensor and stores in object
# - GradientTape object can then compute gradient of any tensor target given the source variables with respect to which one wants to differentiate 
# - Variables vs Tensors - variables are automatically "watched" while tensors are not, though this behavior can be overwritten (tape.watch and watch_accessed_variables=False)
# - the point of evalation is set by whatever the variable values were when defining the formula, not whatever values the variables may have been updated to have (something that generally shouldn't happen)
################################################################################
x0 = 2
x = tf.Variable(x0, dtype=tf.float32) # must be float to use with GradientTape
y = tf.constant(x0, dtype=tf.float32)

with tf.GradientTape(persistent=True) as tape:
    tape.watch(y)
    x.assign(1) # effects f'
    f  = x**2 + y**2
    print(f'f[x={x.numpy()},y={y.numpy()}] = {f.numpy()}')
    
    x.assign(100) # no effect as x's value already captured in f
    f2 = f**2
    print(f'f2[f={f.numpy()}] = {f2.numpy()}')
# Assigning new values to x or y will have no impact though it will show in watched_variables
x.assign(1000)
print('\nWatched Variables')
for v in tape.watched_variables():
    print('\t-',v.name, '=', v.value().numpy())
print()

# References to x, y, f, or f2 must be kept to use gradient
g = f
f = tf.constant(1.0) # g must be used instead of f now
# Passing references to unwatched tensors results in return None

# Gradient
df_dx = tape.gradient(target=g,  sources=x).numpy()
df_dy = tape.gradient(target=g,  sources=y).numpy()
print(f'df/dx = 2x = {df_dx}; df/dy = 2y = {df_dy}')
df_dx, df_dy = tape.gradient(target=g,  sources=[x,y])
print('Same :',df_dx.numpy(), df_dy.numpy())

df2_df = tape.gradient(target=f2, sources=g).numpy()
print(f'df2/df = 2f = {df2_df}')
df2_dx = tape.gradient(target=f2, sources=x).numpy()
print(f'df2/dx = df2/df2 * df/dx = 2f * 2x = {df2_df}')

# Multiple targets (i.e. non-scalar targets)
# - Case 1) n_targets > 1 and n_sources = 1
# - Case 2) n_targets = n_sources > 1

# 2nd order gradients

# unconnected_gradients = tf.UnconnectedGradients.ZERO



# Control flow is allowed but not part of the gradient
# tape.reset()
# with tape.stop_recording()

# Jacobian
# tape.jacobian
# tape.batch_jacobian

# Custom gradients
# @tf.custom_gradient
