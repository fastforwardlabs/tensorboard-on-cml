import tensorflow as tf
import datetime
import matplotlib.pyplot as plt


# Load the MNIST digits dataset from Keras
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Plot sample images
fig = plt.figure()
for i in range(9):
    plt.subplot(3, 3, i + 1)
    plt.tight_layout()
    plt.imshow(x_train[i], cmap="gray")
    plt.title(f"Label: {y_train[i]}")
    plt.xticks([])
    plt.yticks([])

# Function to create simple Keras model using Sequential API
def create_model():
    return tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(
                512,
                activation="relu",
                kernel_regularizer=tf.keras.regularizers.l2(l2=0.0001),
            ),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )


# Create and fit a model by specifying the `tf.keras.callbacks.Tensorboard` Callback to ensure
# logs are stored to capture information about the training run
model = create_model()
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(
    x=x_train,
    y=y_train,
    epochs=40,
    validation_data=(x_test, y_test),
    callbacks=[tensorboard_callback],
)
