
#include "pdf.c"
#include "naivebayes.c"

#include <stdio.h>
#include <stdlib.h>

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
        // FIXME: check data is n_classes*n_features*2
        const int n_items = n_classes*n_features;
        summaries = (BayesSummary *)malloc(sizeof(BayesSummary)*n_items);

        // FIXME: construct summaries from data
    
        model.n_features = n_features;
        model.n_classes = n_classes;
        model.summaries = summaries;
    }
    ~Classifier() {
        free(summaries);
    }

    int32_t predict(std::vector<float> values) {
        const int32_t p = bayes_predict(&model, &values[0], values.size());
        return p;
    }
};


PYBIND11_MODULE(naivebayes, m) {
    m.doc() = "NaiveBayes classifiers for embedded devices";

    m.def("pdf", pdf);
    m.def("pdf_floatfixed", pdf_floatfixed);
    m.def("pdf_fast", pdf_fast);
    m.def("pdf_fixed", pdf_fixed);

    py::class_<Classifier>(m, "Classifier")
        .def(py::init<std::vector<float>, int, int>())
        .def("predict", &Classifier::predict);
}

