
#ifndef ARDUINO

#include <stdio.h>
#include <stdlib.h>

#include "embayes.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class Classifier {
private:
    BayesSummary *summaries;
    BayesModel model;

public:
    Classifier(std::vector<float> data, int n_classes, int n_features)
        : summaries(nullptr)
    {
        const int n_attributes = 3;
        // FIXME: check data is n_classes*n_features*n_attributes
        const int n_items = n_classes*n_features;
        summaries = (BayesSummary *)malloc(sizeof(BayesSummary)*n_items);

        model.n_features = n_features;
        model.n_classes = n_classes;
        model.summaries = summaries;

        for (int class_idx = 0; class_idx<n_classes; class_idx++) {
            for (int feature_idx = 0; feature_idx<n_features; feature_idx++) {
                const int32_t summary_idx = class_idx*n_features + feature_idx;
                BayesSummary summary;
                summary.mean = VAL_FROMFLOAT(data[n_attributes*summary_idx + 0]);
                summary.std = VAL_FROMFLOAT(data[n_attributes*summary_idx + 1]);
                summary.stdlog2 = VAL_FROMFLOAT(data[n_attributes*summary_idx + 2]);
                model.summaries[summary_idx] = summary;
            }
        }
    }
    ~Classifier() {
        free(summaries);
    }

    int32_t predict(std::vector<float> floats) {
        std::vector<val_t> values(floats.size());
        for (int i=0; i<(int)floats.size(); i++) {
            values[i] = VAL_FROMFLOAT(floats[i]);
        }

        const int32_t p = embayes_predict(&model, &values[0], values.size());
        return p;
    }
};

float logpdf_float(float x, float mean, float std, float stdlog2) {
   return VAL_TOFLOAT(embayes_logpdf(VAL_FROMFLOAT(x), VAL_FROMFLOAT(mean), VAL_FROMFLOAT(std), VAL_FROMFLOAT(stdlog2)));
}

PYBIND11_MODULE(embayesc, m) {
    m.doc() = "NaiveBayes classifiers for embedded devices";

    // Probability function
    m.def("logpdf", logpdf_float);

    py::class_<Classifier>(m, "Classifier")
        .def(py::init<std::vector<float>, int, int>())
        .def("predict", &Classifier::predict);
}

#endif
