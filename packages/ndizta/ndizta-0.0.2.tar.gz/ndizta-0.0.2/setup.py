#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2021 by Saswata Nandi
:license: MIT, see LICENSE for more details.
"""
import os
import sys
from pathlib import Path

from setuptools import setup, find_packages
from setuptools.command.install import install

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir

# imdlib version
__version__ = "0.0.2"


def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


example_module = Pybind11Extension(
    'snandi',
    ["src/fib.cpp"],
    include_dirs=['include'],
    extra_compile_args=['-O3']
)

setup(
    name="ndizta",
    version="0.0.2",
    author="Saswata Nandi",
    author_email="iamsaswata@yahoo.com",
    description="A pybind test package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamsaswata/",
    license="MIT",
    packages=find_packages(),
    classifiers=[
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Topic :: Scientific/Engineering :: Hydrology",
    ],
    python_requires='>=3.0',
    keywords='na_na',
    # packages=['':'cct_nn'],
    install_requires=['urllib3', ],
    ext_modules=[example_module],
    cmdclass={"build_ext": build_ext},
)
