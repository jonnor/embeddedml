import numpy
numpy.seterr(all='raise')

import embayesc

def prob_ref(x, mean, std):
    exponent = (- ((x - mean)**2 / (2 * std**2)))
    sigma_max = 100
    if exponent < -sigma_max:
        exponent = -sigma_max
    return (numpy.exp(exponent) / (numpy.sqrt(2 * numpy.pi) * std))

def c_struct_init(vals, convert):
    if convert is None:
      convert = str
    s = ','.join(convert(v) for v in vals)
    return '{ ' + s + ' }'

def c_tofixed(v):
    return "VAL_FROMFLOAT({})".format(v)

def generate_c(model, name='myclassifier'):
    n_classes, n_features, n_attributes = model.shape
    assert n_attributes == 3 # mean+std+stdlog2 

    summaries_data = []
    for class_n, class_summaries in enumerate(model):
        for feature_n, summary in enumerate(class_summaries):
            summaries_data.append(list(summary))

    summaries_name = name + '_summaries'
    summaries = """BayesSummary {name}[{items}] = {{
        {summaries_init}
    }};
    """.format(**{
        'name': summaries_name,
        'items': n_classes*n_features,
        'summaries_init': ',\n  '.join(c_struct_init(d, c_tofixed) for d in summaries_data)
    })

    model = """BayesModel {name} = {{
        {classes},
        {features},
        {summaries},
    }};
    """.format(**{
        'name': name+'_model',
        'classes': n_classes,
        'features': n_features,
        'summaries': summaries_name,
    })

    return '\n\n'.join([summaries, model]) 

class Gaussian(object):
    def __init__(self):
        pass

    def fit(self, X, y):
        separated = [[x for x, t in zip(X, y) if t == c] for c in numpy.unique(y)]
        self.model = numpy.array([numpy.c_[numpy.mean(i, axis=0), numpy.std(i, axis=0), numpy.log2(numpy.std(i, axis=0))] for i in separated])
        return self

    def _prob(self, x, mean, std, stdlog2):
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
        return cp

    def score(self, X, y):
        return sum(self.predict(X) == y) / len(y)

    def output_c(self, name):
        return generate_c(self.model, name)
