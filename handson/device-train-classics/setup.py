# setup.py
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "elastic_net_multiclass",
        ["logreg.cpp"],
        include_dirs=[
            pybind11.get_include(),
        ],
        language='c++',
        cxx_std=11,
    ),
]

setup(
    name="elastic_net_multiclass",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Embedded Elastic Net Multi-class Logistic Regression",
    long_description="A lightweight implementation of Elastic Net Multi-class Logistic Regression optimized for embedded systems",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pybind11",
    ],
)
