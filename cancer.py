
import naivebayes

import numpy
from sklearn.model_selection import train_test_split
from sklearn import metrics, datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

rnd = 11
digits = datasets.load_breast_cancer()
Xtrain, Xtest, ytrain, ytest = train_test_split(digits.data, digits.target, random_state=rnd)
scaler = StandardScaler()
Xtrain = scaler.fit_transform(Xtrain)
Xtest = scaler.transform(Xtest)

print('Loading dataset. {} features', Xtrain.shape[1])

print('Training Gaussian model'.format())
model = naivebayes.Gaussian()
model.fit(Xtrain, ytrain)

# Predict
ypred = model.predict(Xtest)
print('Accuracy on validation set {:.2f}%'.format(metrics.accuracy_score(ypred, ytest)*100))

code = model.output_c('cancer')
filename = 'cancer.h'
with open(filename, 'w') as f:
   f.write(code)
print('Wrote C code to', filename)

port = '/dev/ttyUSB0'
print('Classify on microcontroller via', port)
import serial
device = serial.Serial(port=port, baudrate=115200, timeout=0.1) 

repetitions = 10
Y_pred = []
times = []
for idx,row in enumerate(Xtest):
   # send
   values = [idx, repetitions] + list(row)
   send = ';'.join("{}".format(v) for v in values) + '\n'
   device.write(send.encode('ascii'))
   resp = device.readline()

   # receive
   tok = resp.decode('ascii').strip().split(';')
   retvals = [float(v) for v in tok]
   (request,micros,prediction,reps),values = retvals[:4], retvals[4:]

   assert request == idx
   assert reps == repetitions
   err = numpy.array(values) - row
   assert numpy.sum(err) < 0.05, err # FIXME: why is error so high?

   Y_pred.append(prediction)
   times.append(micros / 1000)
   #print(idx, prediction, reps, micros)

print('Accuracy  {:.2f}%'.format(metrics.accuracy_score(Y_pred, ytest)*100))
print('Confusion matrix')
print(metrics.confusion_matrix(Y_pred, ytest))

avg = numpy.mean(times) / repetitions
stddev = numpy.std(numpy.array(times) / repetitions)
print('Time per classification (ms): {:.2f} avg, {:.2f} stdev'.format(avg, stddev))
