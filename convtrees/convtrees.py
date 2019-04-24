import math

import mnist
import numpy
import pandas
import scipy.signal
from matplotlib import pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn import pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.cluster import KMeans

from spherecluster import SphericalKMeans



def random_kernels(N=20, K=3):
    r = numpy.random.random(N*K*K)
    k = r.reshape(-1, K, K)
    return k

def random_locations(width, height, codebook, n_locations=10, n_kernels=1):
    # where to sample
    xs = numpy.random.randint(0, width, n_locations)
    ys = numpy.random.randint(0, height, n_locations)

    # which kernels to use
    k_idx = numpy.random.randint(0, len(codebook), n_locations*n_kernels)
    return xs, ys, k_idx 

def random_convs(img, codebook, kernels, xs, ys, K):
    
    features = numpy.zeros(shape=(len(kernels),))

    # TODO: vectorize
    for i, (k, x, y) in enumerate(zip(kernels, xs, ys)):
        kernel = codebook[k]

        xmax = min(img.shape[0],x+K)
        ymax = min(img.shape[1],y+K)

        loc = img[x:xmax, y:ymax]
        conv = scipy.signal.convolve2d(loc, kernel, mode='full')
        features[i] = numpy.sum(conv)

    return numpy.stack(features)        

def sample_patches(imgs, K=3, n_patches=10):
    N = len(imgs) * n_patches    
    shape = imgs[0].shape

    xs = numpy.random.randint(0, shape[0]-K, N)
    ys = numpy.random.randint(0, shape[1]-K, N)

    # TODO: vectorize
    out = []
    for i, x, y in zip(range(len(imgs)), xs, ys):
        xmax = x+K
        ymax = y+K
        patch = imgs[i, x:xmax, y:ymax]
        out.append(patch)

    return numpy.stack(out)


def kmeans_codebook(patches, k=30):
    shape = patches[0].shape

    x = patches.reshape(-1, shape[0]*shape[1])
    # normalize
    #x = x / ( 1e-6 + x.sum(axis=1, keepdims=True) )

    est = SphericalKMeans(k)
    #est = KMeans(n_clusters=k)
    est.fit(x)

    codebook = est.cluster_centers_.reshape(-1, shape[0], shape[1])
    return codebook

def plot_codebook(codebook):
    shape = codebook[0].shape

    n_rows = 5
    cols, rows = math.ceil(len(codebook)/n_rows), n_rows
    print('nn', cols, rows, cols*rows)


    fig, axs = plt.subplots(rows, cols, figsize=(4*3,4))

    fig.patch.set_facecolor('grey')
    for ax in axs.flatten():
        ax.set_visible(False)

    for ax, kernel in zip(axs.flatten(), codebook):
        print('c', kernel)
        ax.set_visible(True)
        ax.imshow(kernel, cmap='gray')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    fig.tight_layout()

    return fig

def evaluate_mnist():

    train_x, train_y = mnist.train_images(), mnist.train_labels()
    test_x, test_y  = mnist.test_images(), mnist.test_labels()

    K=3
    codebook_size = 50
    locations = 100
    kernels = codebook_size//5

    random_codebook = random_kernels(K=K, N=codebook_size)
    #print('rr code', codebook.shape)
    print('Creating codebook')
    pp = sample_patches(train_x, K=K)
    codebook = kmeans_codebook(pp, k=codebook_size)
    print('kmeans code', codebook.shape)

    fig = plot_codebook(codebook)
    fig.savefig('codebook.png', facecolor=fig.get_facecolor())

    input_shape = (28, 28)

    input_area = numpy.array(input_shape).prod()
    sample_area = K*K*locations
    coverage = sample_area / input_area 
    # TODO: could calculate effective sampled area
    print('Coverage: {:d}% {:d}px/{:d}px'.format(int(coverage*100), input_area, sample_area))

    xs, ys, ks = random_locations(28, 28, codebook, n_locations=locations, n_kernels=kernels)

    def transform(imgs):
        f = [ random_convs(i, codebook, ks, xs, ys, K=K) for i in imgs ]
        f = numpy.array(f)
        return f

    print('Precomputing features')
    train_x = transform(train_x)
    test_x = transform(test_x)

    clf = RandomForestClassifier(n_estimators=100, min_samples_leaf=1e-6)
    params = {
        'n_estimators': [ 1, 10, 100],
        'min_samples_leaf': [1e-5],
        #'min_samples_leaf': numpy.logspace(-7, -4, 10),
        #'n_estimators': numpy.linspace(30, 100, 4).astype(int),
    }

    #ff = FunctionTransformer(func=transform, validate=True)

    #clf = pipeline.make_pipeline(ff, clf)

    #print('p\n', params)

    clf = GridSearchCV(clf, params, cv=3, scoring='accuracy', return_train_score=True,
                        verbose=2, n_jobs=-1)

    print(train_x.shape, train_x.shape[0])

    #train_x = train_x.reshape(-1, 28*28)
    #test_x = test_x.reshape(-1, 28*28)
    #train_x = train_x[:1000]
    #train_y = train_y[:1000]

    print("Train model")
    clf.fit(train_x, train_y)
    expected = test_y.tolist()

    print("Compute predictions")
    predicted = clf.predict(test_x)
    print("Accuracy: ", accuracy_score(expected, predicted))

    df = pandas.DataFrame(clf.cv_results_)
    df.to_csv('results.csv')
    print('CV results\n', df[['param_min_samples_leaf', 'param_n_estimators', 'mean_train_score', 'mean_test_score']])


if __name__ == '__main__':

    mnist.temporary_dir = lambda: './data'
    evaluate_mnist()

