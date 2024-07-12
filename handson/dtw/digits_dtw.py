
import os

import pandas
import librosa
import numpy

def load_digits_dataset(path):

    records = []
    recordings_dir = os.path.join(path, 'recordings')
    for name in os.listdir(recordings_dir):
        digit, speaker, sample = os.path.splitext(name)[0].split('_')

        records.append({
            'digit': int(digit),
            'speaker': speaker,
            'sample': sample,
            'file': name,
        })
    
    out = pandas.DataFrame.from_records(records)
    return out

def compute_features(filenames : pandas.Series, directory : str,
        mean_normalize=True, variance_normalization=True, drop_zero=True,
    ):

    def compute_one(f):
        p = os.path.join(directory, f)
        audio, sr = librosa.load(p, sr=None)
        #print('duration', len(audio)/sr)
        assert sr == 8000
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13, n_fft=256)
        if mean_normalize:
            mean = numpy.mean(mfcc, axis=1, keepdims=True)
            mfcc -= mean + 1e-8

        if variance_normalization:
            stddev = numpy.std(mfcc, axis=1, keepdims=True)
            mfcc /= stddev

        if drop_zero:
            # the zeroth MFCC coefficient is not so useful for speech
            mfcc = mfcc[1:,:]

        return mfcc
    
    return filenames.apply(compute_one)
    

def main():
    
    path = 'free-spoken-digit-dataset'
    dataset = load_digits_dataset(path)

    # XXX: scaling from 1k to 2k sample took time from 15 seconds per fold to 50 seconds per fold with KNN
    dataset = dataset.sample(n=1000, random_state=1)

    print(dataset)
    print('groups', dataset.speaker.nunique())

    print('classes', dataset.digit.value_counts().sort_index())

    recordings_dir = os.path.join(path, 'recordings')
    features = compute_features(dataset.file, recordings_dir)

    shapes = [ f.shape for f in features ]
    print('feature-dims',
        min(shapes), max(shapes), numpy.quantile(shapes, 0.10), numpy.quantile(shapes, 0.90)
    )

    from tslearn.neighbors import KNeighborsTimeSeriesClassifier

    test_groups = dataset.speaker.sample(n=2, random_state=1)
    train_groups = dataset.speaker

    from sklearn.model_selection import cross_validate
    from sklearn.model_selection import GroupShuffleSplit

    length = 10
    n_features = features.iloc[0].shape[0]

    # standardize sequences to a fixed length
    xx = []
    for i, f in enumerate(features):
        x = numpy.zeros(shape=(length, n_features))
        ff = f.T[0:length, :]
        x[0:len(ff), :] = ff
        xx.append(x)
    X = numpy.stack(xx)


    # TODO: set metric to be Z-normalized Euclidean?
    clf = KNeighborsTimeSeriesClassifier(n_neighbors=3,
        metric="dtw",
        metric_params=dict(global_constraint="sakoe_chiba", sakoe_chiba_radius=2),
        n_jobs=None,
    )
    
    splitter = GroupShuffleSplit(n_splits=3, test_size=0.2)
    res = cross_validate(clf, X, dataset.digit,
            cv=splitter, groups=dataset.speaker,
            verbose=2, return_train_score=True
    )
    res = pandas.DataFrame.from_records(res)

    print(res)
    print(res.test_score.mean())

if __name__ == '__main__':
    main()

