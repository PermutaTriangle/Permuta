#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="permuta",
    version="0.1.1",
    author="Henning Ulfarsson",
    author_email="henningu@ru.is",
    description="A comprehensive high performance permutation library.",
    license="BSD-3",
    keywords=("permutation perm mesh pattern patt avoid contain occurrence"
              "statistic"),
    url="https://github.com/PermutaTriangle/Permuta",
    project_urls={
        'Source': 'https://github.com/PermutaTriangle/Permuta',
        'Tracker': 'https://github.com/PermutaTriangle/Permuta/issues'
    },
    packages=find_packages(),
    long_description=read("README.rst"),
    extras_require={"plot": ["seaborn"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest",
                   "permuta",
                   "pytest-pep8",
                   "pytest-isort"],
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)
