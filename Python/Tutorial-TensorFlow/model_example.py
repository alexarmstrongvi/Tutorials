################################################################################
# Basic Model Training Example
################################################################################
print(f"\n===== Running {__file__} =====\n")

import tensorflow as tf
import numpy as np

(x_train, y_train), (x_test, y_test) = \
    tf.keras.datasets.mnist.load_data()

n_pixels = x_train.shape[1] * x_train.shape[2]

x_train  = x_train.reshape(-1, n_pixels).astype("float32") / 255
x_test   = x_test.reshape(-1, n_pixels).astype("float32") / 255
y_train  = y_train.astype("float32")
y_test   = y_test.astype("float32")

n_val = 10000
x_val   = x_train[-n_val:]
y_val   = y_train[-n_val:]
x_train = x_train[:-n_val]
y_train = y_train[:-n_val]


my_model = tf.keras.Sequential([
    tf.keras.Input(shape=(n_pixels,), name='digits'),
    tf.keras.layers.Dense(units=64, activation='relu',    name='dense_1'),
    tf.keras.layers.Dense(units=64, activation='relu',    name='dense_2'),
    tf.keras.layers.Dense(units=10, activation='softmax', name='predictions')
])


# Compiling
my_model.compile(
    optimizer = tf.optimizers.RMSprop(),
    loss      = tf.losses.SparseCategoricalCrossentropy(),
    metrics   = [
        tf.metrics.SparseCategoricalAccuracy()
    ],
)

# Fitting
history = my_model.fit(
    x_train, y_train,
    batch_size=64,
    epochs=2,
    validation_data=(x_val, y_val)
)

assert(type(history) == tf.keras.callbacks.History)
#print(history.history)

# Evaluating
results = my_model.evaluate(x_test, y_test, batch_size=128)
results

# Predicting
# - DONT USE my_model.predict in most cases as this builds a lot of extra things to run more optimally on large inputs but ends up storing a lot of that in memory until it gets deleted manually
y_pred = my_model(x_test[:3])
print('Prediction shape =',y_pred.shape)
print('Index of max prediction per image :',y_pred.argmax(axis=1))
