
import numpy as np
import tensorflow as tf
from keras.datasets import mnist
import keras

#mnist_arduino
def init_model(dim0):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Input,Conv2D, Dense, MaxPooling2D, Softmax, Activation, BatchNormalization, Flatten, Dropout, DepthwiseConv2D
    from tensorflow.keras.layers import MaxPool2D, AvgPool2D, AveragePooling2D, GlobalAveragePooling2D,ZeroPadding2D,Input,Embedding,PReLU,Reshape

    model = Sequential()
    model.add(Conv2D(dim0, (3,3), padding = 'valid',strides = (2, 2), input_shape = (28, 28, 1), name='ftr0'));model.add(BatchNormalization(name="bn0"));model.add(Activation('relu', name="relu0")); 
    model.add(Conv2D(dim0*3, (3,3), padding = 'valid',strides = (2, 2), name='ftr1'));model.add(BatchNormalization(name="bn1"));model.add(Activation('relu',name="relu1")); 
    model.add(Conv2D(dim0*6, (3,3), padding = 'valid',strides = (2, 2), name='ftr2'));model.add(BatchNormalization());model.add(Activation('relu')); 
    
    model.add(GlobalAveragePooling2D(name='GAP'))
    model.add(Dense(10, name="fc1"))
    model.add(Activation('softmax', name="sm"))
    return model


def train_mnist():
    (x_train,y_train), (x_test,y_test) = mnist.load_data() 
    num_classes = 10

    x_train = x_train.reshape(x_train.shape[0],x_train.shape[1],x_train.shape[2],1)/255
    x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],x_test.shape[2],1)/255

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)


    model = init_model(dim0=1)  
    model.summary()

    EPOCHS = 20
    model.compile(optimizer='adam', loss = "categorical_crossentropy", metrics = ["categorical_accuracy"]) 
    H = model.fit(x_train, y_train, batch_size=64, epochs= EPOCHS,  verbose= 1, validation_data = (x_test, y_test), shuffle=True) 

    h5_file = "mnist_arduino_custom.h5"
    model.save(h5_file)

def generate_test_file(data):

    for y in range(28):
        for x in range(28):
            print("%3d,"%(int(data[y,x,0]*255)), end="")
        print("")

def main():

    train_mnist()

    #data = x_test[1]

    # FIXME: export the model using TinyMaix

    #  python3 h5_to_tflite.py h5/mnist_valid.h5 tflite/mnist_valid_f.tflite 0
    #  python3 tflite2tmdl.py tflite/mnist_valid_f.tflite tmdl/mnist_valid_f.tmdl fp32 1 28,28,1 10"

if __name__ == '__main__':
    main()
