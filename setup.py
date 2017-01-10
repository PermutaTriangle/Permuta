#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "permuta",
    version = "0.0.1",
    author = "Henning Ulfarsson",
    author_email = "henningu@ru.is",
    description = "A comprehensive high performance permutation library.",
    license = "BSD-3",
    keywords = "permutation mesh pattern avoid contain statistic",
    url = "https://github.com/PermutaTriangle/Permuta",
    packages=["permuta"],
    long_description=read("README.md"),
)
