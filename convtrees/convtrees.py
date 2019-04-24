import mnist
import numpy
import pandas
import scipy.signal

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import FunctionTransformer
from sklearn import pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

mnist.temporary_dir = lambda: './data'

def random_kernels(N=20, K=3):
    r = numpy.random.random(N*K*K)
    k = r.reshape(-1, K, K)
    return k

def random_locations(width, height, codebook, N=10):
    # where to sample
    xs = numpy.random.randint(0, width, N)
    ys = numpy.random.randint(0, height, N)

    # which kernels to use
    k_idx = numpy.random.randint(0, len(codebook), N)
    return xs, ys, k_idx 

def random_convs(img, codebook, kernels, xs, ys, K):
    
    features = numpy.zeros(shape=(len(kernels),))

    for i, (k, x, y) in enumerate(zip(kernels, xs, ys)):
        kernel = codebook[k]

        xmax = min(img.shape[0],x+K)
        ymax = min(img.shape[1],y+K)

        loc = img[x:xmax, y:ymax]
        conv = scipy.signal.convolve2d(loc, kernel, mode='full')
        features[i] = numpy.sum(conv)

    return numpy.stack(features)        


def evaluate_mnist():

    K=3
    codebook = random_kernels(K=K, N=30)
    xs, ys, ks = random_locations(28, 28, codebook, N=100)

    def transform(imgs):
        print('ii', imgs.shape)
        f = [ random_convs(i.reshape(28, 28), codebook, ks, xs, ys, K=K) for i in imgs ]
        f = numpy.array(f)
        print('f', f.shape)
        return f

    train_x, train_y = mnist.train_images(), mnist.train_labels()
    test_x, test_y  = mnist.test_images(), mnist.test_labels()


    clf = RandomForestClassifier(n_estimators=100, min_samples_leaf=1e-6)
    params = {
        'n_estimators': [1, 10, 100],
        #'min_samples_leaf': numpy.logspace(-7, -4, 10),
        #'n_estimators': numpy.linspace(30, 100, 3).astype(int),
    }

    ff = FunctionTransformer(func=transform, validate=True)

    clf = pipeline.make_pipeline(ff, clf)

    #print('p\n', params)

    #clf = GridSearchCV(clf, params, cv=3, scoring='accuracy', return_train_score=True,
    #                    verbose=2, n_jobs=-1)

    print(train_x.shape, train_x.shape[0])

    train_x = train_x.reshape(-1, 28*28)
    test_x = test_x.reshape(-1, 28*28)
    #train_x = train_x[:1000]
    #train_y = train_y[:1000]

    print("Train model")
    clf.fit(train_x, train_y)
    expected = test_y.tolist()

    print("Compute predictions")
    predicted = clf.predict(test_x)
    print("Accuracy: ", accuracy_score(expected, predicted))

    df = pandas.DataFrame(clf.cv_results_)
    print('CV results\n', df[['param_min_samples_leaf', 'mean_train_score', 'mean_test_score']])
    df.to_csv('results.csv')



if __name__ == '__main__':
    evaluate_mnist()

