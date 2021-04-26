#!/usr/bin/env python

import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="permuta",
    version=get_version("permuta/__init__.py"),
    author="Permuta Triangle",
    author_email="permutatriangle@gmail.com",
    description="A comprehensive high performance permutation library.",
    license="BSD-3",
    keywords=(
        "permutation perm mesh pattern patt avoid contain occurrence" "statistic"
    ),
    url="https://github.com/PermutaTriangle/Permuta",
    project_urls={
        "Source": "https://github.com/PermutaTriangle/Permuta",
        "Tracker": "https://github.com/PermutaTriangle/Permuta/issues",
    },
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={"permuta": ["py.typed"]},
    long_description=read("README.rst"),
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    entry_points={"console_scripts": ["permtools=permuta.cli:main"]},
)
