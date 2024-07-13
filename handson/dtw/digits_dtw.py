
import math
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
            'command': int(digit),
            'speaker': speaker,
            'sample': sample,
            'file': os.path.join('recordings', name),
        })
    
    out = pandas.DataFrame.from_records(records)
    return out

def load_mini_speech_commands(path):
    
    ignored = set(['README.md'])
    records = []
    classes = [ p for p in os.listdir(path) if not p in ignored ]
    for c in classes:
        for name in os.listdir(os.path.join(path, c)):
            if not name.endswith('.wav'):
                print('ignore', name)
                continue
            speaker, _, sample = os.path.splitext(name)[0].split('_')

            records.append({
                'command': c,
                'speaker': speaker,
                'sample': sample,
                'file': os.path.join(c, name),
            })

    out = pandas.DataFrame.from_records(records)
    return out


def compute_features(filenames : pandas.Series, directory : str,
        mean_normalize=True, variance_normalization=True, drop_zero=True, lifter=0,
    ):

    def compute_one(f):
        p = os.path.join(directory, f)
        audio, sr = librosa.load(p, sr=8000)
        #print('duration', len(audio)/sr)
        assert sr == 8000
        hop_length = 256
        n_fft = hop_length * 2
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13,
            n_fft=n_fft, hop_length=hop_length, lifter=lifter)
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
    
def plot_features(X, dataset, class_column='command'):

    n_samples = 10

    from matplotlib import pyplot as plt
    import librosa.display

    for class_name in dataset[class_column].unique():
        selected = dataset[dataset[class_column]==class_name].sample(n_samples)
        print(selected.index)
        Xs = X[selected.index]

        height = n_samples * 3.0
        width = 3.0 * 3
        fig, axs = plt.subplots(n_samples, figsize=(width, height))
        for ax, x, (idx, sample) in zip(axs, Xs, selected.iterrows()):
            img = librosa.display.specshow(x.T,
                    ax=ax,
                    x_axis='time', 
                    sr=8000, hop_length=256,
            )
            print(sample)
            ax.set_title(sample['file'])

        fig.tight_layout()
        fig.savefig(f'features_{class_name}.png')
        #fig.show()



from scikeras.wrappers import KerasClassifier

def build_cnn(meta):
    # meta is a special argument from scikeras
    n_features_in_ = meta["n_features_in_"]
    input_shape = meta["X_shape_"][1:]
    n_classes = meta["n_classes_"]

    from keras import layers, models

    print('input', input_shape, meta["X_shape_"])
  
    filters_start = 16
    dropout = 0.25
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Reshape((input_shape[0], input_shape[1], 1)),
        layers.Conv2D(filters_start, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(filters_start*2, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(dropout),
        layers.Flatten(),
        layers.Dense(32, activation='relu'),
        layers.Dropout(dropout),
        layers.Dense(n_classes),
        layers.Activation("softmax"),
    ])

    print(model.summary())

    return model

def build_rnn(meta):
    # meta is a special argument from scikeras
    n_features_in_ = meta["n_features_in_"]
    input_shape = meta["X_shape_"][1:]
    n_classes = meta["n_classes_"]

    from keras import layers, models

    gru_units = 16
    dropout = 0.25
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.TimeDistributed(layers.Dense(8)),
        layers.GRU(gru_units, return_sequences=False),
        layers.Dense(32, activation='relu'),
        layers.Dropout(dropout),
        layers.Dense(n_classes),
        layers.Activation("softmax"),
    ])

    print(model.summary())

    return model

def main():

    path = 'free-spoken-digit-dataset'   
    path = 'mini_speech_commands'

    if 'free' in path:
        dataset = load_digits_dataset(path)
    elif 'mini' in path:
        dataset = load_mini_speech_commands(path)

    # XXX: scaling from 1k to 2k sample took time from 15 seconds per fold to 50 seconds per fold with KNN
    dataset = dataset.sample(n=len(dataset), random_state=1).reset_index()

    print(dataset)
    print('groups', dataset.speaker.nunique())

    print('classes', dataset.command.value_counts().sort_index())

    recordings_dir = path

    features = compute_features(dataset.file, recordings_dir,
        mean_normalize=True, variance_normalization=True, drop_zero=True,
    )

    shapes = [ f.shape[1] for f in features ]
    print('feature-dims',
        min(shapes), max(shapes), numpy.quantile(shapes, 0.10), numpy.quantile(shapes, 0.90)
    )

    from tslearn.neighbors import KNeighborsTimeSeriesClassifier


    from sklearn.model_selection import cross_validate
    from sklearn.model_selection import GroupShuffleSplit

    length = math.ceil(numpy.quantile(shapes, 0.90))
    n_features = features.iloc[0].shape[0]

    # standardize sequences to a fixed length
    xx = []
    for i, f in enumerate(features):
        x = numpy.zeros(shape=(length, n_features))
        ff = f.T[0:length, :]
        x[0:len(ff), :] = ff

        xx.append(x)
        #xx.append(numpy.ravel(x))

    X = numpy.stack(xx)

    #plot_features(X, dataset)

    #return # XXX:
    
    # TODO: set metric to be Z-normalized Euclidean?
    clf = KNeighborsTimeSeriesClassifier(n_neighbors=1,
        metric="dtw",
        metric_params=dict(global_constraint="sakoe_chiba", sakoe_chiba_radius=1),
        n_jobs=None,
    )
    
    from sklearn.ensemble import RandomForestClassifier
    #clf = RandomForestClassifier(n_estimators=100)


    from scikeras.wrappers import KerasClassifier
    clf = KerasClassifier(
        build_cnn,
        loss="sparse_categorical_crossentropy",
        epochs=200,
        fit__validation_split=0.2,
        optimizer='adam',
        optimizer__learning_rate=0.001,
        batch_size=128,
        metrics=['accuracy'],
        #hidden_layer_dim=100,
    )

    splitter = GroupShuffleSplit(n_splits=3, test_size=0.2)
    res = cross_validate(clf, X, dataset.command,
            cv=splitter, groups=dataset.speaker,
            verbose=2, return_train_score=True
    )
    res = pandas.DataFrame.from_records(res)

    print(res)
    print(res.test_score.mean())

if __name__ == '__main__':
    main()

