#!/usr/bin/env python
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "permuta",
    version = "0.0.1",
    author = "Henning Ulfarsson",
    author_email = "henningu@ru.is",
    description = "A comprehensive high performance permutation library.",
    license = "BSD-3",
    keywords = "permutation perm mesh pattern patt avoid contain occurrence statistic",
    url = "https://github.com/PermutaTriangle/Permuta",
    install_requires = read("requirements.txt").splitlines(),
    extras_require = {"plot": ["seaborn"]},
    packages=find_packages(),
    long_description=read("README.md"),
)
