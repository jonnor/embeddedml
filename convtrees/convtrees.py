import mnist
import numpy
import pandas

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

mnist.temporary_dir = lambda: './data'

def evaluate_mnist():

    train_x, train_y = mnist.train_images(), mnist.train_labels()
    test_x, test_y  = mnist.test_images(), mnist.test_labels()


    clf = RandomForestClassifier(n_estimators=100)
    params = {
        'min_samples_leaf': numpy.logspace(-7, -4, 10),
        'n_estimators': numpy.linspace(30, 100, 3).astype(int),
    }

    print('p\n', params)

    clf = GridSearchCV(clf, params, cv=3, scoring='accuracy', return_train_score=True,
                        verbose=2, n_jobs=-1)

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

    df = pandas.DataFrame(clf.cv_results_)
    print('CV results\n', df[['param_min_samples_leaf', 'mean_train_score', 'mean_test_score']])
    df.to_csv('results.csv')

    print("Accuracy: ", accuracy_score(expected, predicted))

if __name__ == '__main__':
    evaluate_mnist()

