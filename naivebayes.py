import numpy
numpy.seterr(all='raise')

import embayesc

def prob_ref(x, mean, std):
    exponent = (- ((x - mean)**2 / (2 * std**2)))
    sigma_max = 100
    if exponent < -sigma_max:
        exponent = -sigma_max
    return (numpy.exp(exponent) / (numpy.sqrt(2 * numpy.pi) * std))

class Gaussian(object):
    def __init__(self):
        pass

    def fit(self, X, y):
        separated = [[x for x, t in zip(X, y) if t == c] for c in numpy.unique(y)]
        self.model = numpy.array([numpy.c_[numpy.mean(i, axis=0), numpy.std(i, axis=0)] for i in separated])
        return self

    def _prob(self, x, mean, std):
        return numpy.log(prob_ref(x, mean, std))

    def predict_log_proba(self, X):            
        def class_probability(summaries, x):
            probs = [self._prob(i, *s) for s, i in zip(summaries, x)]
            sss = numpy.sum(probs)
            return sss
                
        return [[ class_probability(s, x) for s in self.model] for x in X]

    def predict(self, X):
        n_classes, n_features, _ = self.model.shape
        model = list(numpy.ravel(self.model))
        self.classifier = embayesc.Classifier(model, n_classes, n_features)

        cp = [ self.classifier.predict(x) for x in X ]
        pp = numpy.argmax(self.predict_log_proba(X), axis=1)
        #print('predictions', cp, '\n', pp)
        return pp

    def score(self, X, y):
        return sum(self.predict(X) == y) / len(y)

    def output_c(self, name):
        return 'TODO'
