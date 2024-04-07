
import numpy
import nnom
from keras.applications import MobileNet
import keras

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import load_model, save_model
import tensorflow as tf

save_dir = 'keras_mnist_trained_model.h5'

def build_model(width=96, height=96, classes=521, channels=1, alpha=0.25):

    model = MobileNet(
        input_shape=(width, height, channels),
        alpha=alpha,
        depth_multiplier=1,
        dropout=0.001,
        include_top=True,
        weights=None,
        pooling=None,
        classes=classes,
        classifier_activation="softmax",
    )

    return model

def train(model, x_train, y_train, x_test, y_test, batch_size=64, epochs=50):
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=2,
              validation_data=(x_test, y_test),
              shuffle=False)

    return history

def generate_c_model(x_test, y_test, save_dir, out_path = "weights.h"):
    # -------- generate weights.h (NNoM model) ----------
    # get the best model
    model = load_model(save_dir)

    # only use 1000 for test
    x_test = x_test[:1000]
    y_test = y_test[:1000]
    # generate binary dataset for NNoM validation, 0~1 -> 0~127, q7
    nnom.generate_test_bin(x_test*127, y_test, name='test_data.bin')

    # evaluate in Keras (for comparision)
    scores = nnom.evaluate_model(model, x_test, y_test)

    # generate NNoM model, x_test is the calibration dataset used in quantisation process
    nnom.generate_model(model, x_test, format='hwc', per_channel_quant=False, name=out_path)


def main():

    print('Keras version', keras.__version__)

    epochs = 10
    num_classes = 10
    train_samples = None # can be used to limit

    # The data, split between train and test sets:
    (x_train, y_train), (x_test_original, y_test_original) = cifar10.load_data()

    # convert to grayscale

    x_test = x_test_original
    y_test = y_test_original
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # Convert class vectors to binary class matrices.
    y_train = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes)

    # reshape to 4 d becaue we build for 4d?
    #x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
    #x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
    print('x_train shape:', x_train.shape)

    # quantize the range to q7
    x_test = x_test.astype('float32')/255
    x_train = x_train.astype('float32')/255
    print("data range", x_test.min(), x_test.max())

    # XXX: make training faster
    if train_samples is not None:
        x_train = x_train[:train_samples]
        y_train = y_train[:train_samples]

    #build model
    s = x_test.shape[1:]
    model = build_model(width=s[0], height=s[1], classes=num_classes, channels=3)

    model.summary()

    # train model
    history = train(model, x_train, y_train, x_test.copy(), y_test.copy(), epochs=epochs)

    save_model(model, save_dir)
    del model
    tf.keras.backend.clear_session()

    # convert
    generate_c_model(x_test, y_test, save_dir)


if __name__ == "__main__":
    main()



