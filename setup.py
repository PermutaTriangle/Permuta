#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="permuta",
    version="0.1.0",
    author="Henning Ulfarsson",
    author_email="henningu@ru.is",
    description="A comprehensive high performance permutation library.",
    license="BSD-3",
    keywords=("permutation perm mesh pattern patt avoid contain occurrence"
              "statistic"),
    url="https://github.com/PermutaTriangle/Permuta",
    packages=find_packages(),
    long_description=read("README.md"),
    extras_require={"plot": ["seaborn"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest",
                   "permuta",
                   "pytest-pep8",
                   "pytest-isort"],
)
