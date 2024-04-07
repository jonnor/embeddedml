
import os
import subprocess

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


def train_mnist(h5_file):
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

    model.save(h5_file)

def generate_test_file(data):

    for y in range(28):
        for x in range(28):
            print("%3d,"%(int(data[y,x,0]*255)), end="")
        print("")

def generate_tinymaix_model(h5_file,
        input_shape : tuple[int],
        output_shape : tuple[int],
        tools_dir,
        python_bin='python',
        precision='fp32',
        quantize=False,
        output_dequantize=False,
    ):

    # Convert .h5 to .tflite file
    assert h5_file.endswith('.h5'), 'Keras model HDF5 file must end with .h5'
    tflite_file = h5_file.replace('.h5', '.tflite')

    args = [
        python_bin,
        os.path.join(tools_dir, 'h5_to_tflite.py'),
        h5_file,
        tflite_file,
    ]
    if quantize:
        raise NotImplementedError()
    else:
        args += [ '0' ] 

    cmd = ' '.join(args)
    print('RUN', cmd)
    out = subprocess.check_output(args).decode('utf-8')

    # check that outputs have been created
    assert os.path.exists(tflite_file), tflite_file
    
    def format_shape(t : tuple[int]):
        return ','.join(str(i) for i in t)


    # Convert .tflite file to TinyMaix 
    tmld_file = tflite_file.replace('.tflite', '.tmdl')
    header_file = tmld_file.replace('.tmdl', '.h')
    args = [
        python_bin,
        os.path.join(tools_dir, 'tflite2tmdl.py'),
        tflite_file,
        tmld_file,
        precision,
        str(1 if output_dequantize else 0),
        format_shape(input_shape),
        format_shape(output_shape),
        #endian, #"<" or ">"
    ]
    cmd = ' '.join(args)
    print('RUN', cmd)
    subprocess.check_output(args).decode('utf-8')

    # check that outputs have been created
    assert os.path.exists(tmld_file), tmld_file
    assert os.path.exists(header_file), header_file


def main():

    h5_file = "mnist_arduino_custom.h5"
    #train_mnist(h5_file)

    #data = x_test[1]

    # Export the model using TinyMaix
    tinymaix_tools_dir = './TinyMaix/tools'
    generate_tinymaix_model(h5_file,
        input_shape=(28,28,1),
        output_shape=(1,),
        tools_dir=tinymaix_tools_dir\
    )



    #  python3 h5_to_tflite.py h5/mnist_valid.h5 tflite/mnist_valid_f.tflite 0
    #  python3 tflite2tmdl.py tflite/mnist_valid_f.tflite tmdl/mnist_valid_f.tmdl fp32 1 28,28,1 10"

if __name__ == '__main__':
    main()
