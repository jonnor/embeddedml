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

def plot_codebook(codebook):
    shape = codebook[0].shape

    n_rows = 5
    cols, rows = math.ceil(len(codebook)/n_rows), n_rows

    fig, axs = plt.subplots(rows, cols, figsize=(4*3,4))

    fig.patch.set_facecolor('grey')
    for ax in axs.flatten():
        ax.set_visible(False)

    for ax, kernel in zip(axs.flatten(), codebook):
        ax.set_visible(True)
        ax.imshow(kernel, cmap='gray')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    fig.tight_layout()

    return fig


def random_kernels(N=20, K=3):
    r = numpy.random.random(N*K*K)
    k = r.reshape(-1, K, K)
    return k

def convolve(img, codebook, kernels, ls, xs, ys, K):
    
    features = numpy.zeros(shape=(len(kernels),))

    # TODO: vectorize over images
    for i, (l, k, x, y) in enumerate(zip(ls, kernels, xs, ys)):
        #print('ii', i//5, k, codebook.shape)
        kernel = codebook[l, k]
        #kernel = numpy.zeros(shape=(K,K))

        xmax = min(img.shape[0],x+K)
        ymax = min(img.shape[1],y+K)

        loc = img[x:xmax, y:ymax]
        conv = scipy.signal.convolve2d(loc, kernel, mode='full')
        features[i] = numpy.sum(conv)

    return numpy.stack(features)        

def locations_random_full(shape, N, K=None):
    xs = numpy.random.randint(0, shape[0], N)
    ys = numpy.random.randint(0, shape[0], N)
    return xs, ys

def locations_random_valid(shape, N, K=3):
    xs = numpy.random.randint(0, shape[0]-K, N)
    ys = numpy.random.randint(0, shape[1]-K, N)
    return xs, ys


def sample_patches(imgs, locations, K, n_patches=100):
    N = len(imgs) * n_patches    

    xs, ys = locations
    assert len(xs) == len(ys)
    out = numpy.zeros(shape=(len(xs), n_patches, K, K))

    img_range = numpy.array(range(0, len(imgs)))
    for l, (x, y) in enumerate(zip(xs, ys)):
        subset = numpy.random.choice(img_range, size=n_patches)
        patch = imgs[subset, x:x+K, y:y+K]
        out[l] = patch

    return out

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



def evaluate_mnist():

    train_x, train_y = mnist.train_images(), mnist.train_labels()
    test_x, test_y  = mnist.test_images(), mnist.test_labels()

    K=3
    codebook_size = 30
    n_locations = 30
    n_kernels = 30
    input_shape = (28, 28)

    #random_codebook = random_kernels(K=K, N=codebook_size)
    #print('rr code', codebook.shape)
    print('Creating codebook')

    locations = locations_random_valid(input_shape, N=n_locations, K=K)
    assert len(locations[0]) == n_locations, (len(locations[0]), n_locations)
    
    loc_patches = sample_patches(train_x, locations, K=K, n_patches=1000)
    all_patches = loc_patches.reshape(-1, K, K)

    print('pp', loc_patches.shape, all_patches.shape)

    codebook = kmeans_codebook(all_patches, k=codebook_size)
    print('kmeans global codebook', codebook.shape)

    loc_codebooks = numpy.array([ kmeans_codebook(p, k=codebook_size) for p in loc_patches ])
    print('loc codebooks', loc_codebooks.shape)

    fig = plot_codebook(codebook)
    fig.savefig('codebook.png', facecolor=fig.get_facecolor())


    input_area = numpy.array(input_shape).prod()
    sample_area = K*K*n_locations
    coverage = sample_area / input_area
    print('cc', sample_area, input_area)
    # TODO: could calculate effective sampled area
    print('Coverage: {:d}% {:d}px/{:d}px'.format(int(coverage*100), sample_area, input_area))

    xs, ys = locations
    xs = numpy.repeat(xs, n_kernels)
    ys = numpy.repeat(ys, n_kernels)
    ls = list(range(n_locations))
    ls = numpy.repeat(ls, n_kernels)

    ks = numpy.random.randint(0, codebook_size, len(xs))

    assert len(ks) == len(xs), (len(ks), len(xs))
    assert len(ls) == len(xs), (len(ls), len(xs))

#    ks = numpy.flatten([ numpy.random.randint(0, len(cc), size=n_kernels) for cc in loc_codebooks ])


    def transform(imgs):
        f = [ convolve(i, loc_codebooks, ks, ls, xs, ys, K=K) for i in imgs ]
        f = numpy.array(f)
        return f

    print('Precomputing features')
    train_x = transform(train_x)
    test_x = transform(test_x)
    print('Feat', train_x.shape)

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

