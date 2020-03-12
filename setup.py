#!/usr/bin/env python

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="permuta",
    version="1.2.1",
    author="Permuta Triangle",
    author_email="permutatriangle@gmail.com",
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
    setup_requires=["pytest-runner==5.2"],
    tests_require=["pytest==5.4.0",
                   "pytest-cov==2.8.1",
                   "pytest-pep8==1.0.6",
                   "pytest-isort==0.3.1"],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)
