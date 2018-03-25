
#include "pdf.c"

#include <stdio.h>
#include <stdlib.h>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;



PYBIND11_MODULE(naivebayes, m) {
    m.doc() = "NaiveBayes classifiers for embedded devices";

    m.def("pdf", pdf);
    m.def("pdf_floatfixed", pdf_floatfixed);
    m.def("pdf_fast", pdf_fast);
    m.def("pdf_fixed", pdf_fixed);
}

