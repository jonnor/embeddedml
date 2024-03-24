
import numpy
import nnom
import keras.applications

print('Keras version', keras.__version__)

model = keras.applications.MobileNet(
    input_shape=(96, 96, 1),
    alpha=0.25,
    depth_multiplier=1,
    dropout=0.001,
    include_top=True,
    weights=None,
    pooling=None,
    classes=521,
    classifier_activation="softmax",
)

#model.summary()

#print(nnom.__path__)
print(dir(nnom))

out_path = "kws_weights.h"
data = numpy.random.rand(100, 96, 96, 1)
nnom.generate_model(model, data, name=out_path)


print('Wrote C code to', out_path)
