import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "permuta",
    version = "0.0.1",
    author = "Henning Ulfarsson",
    author_email = "henningu@ru.is",
    description = "A library of stuff related to permutations.",
    license = "BSD-3",
    keywords = "permutations patterns",
    url = "https://github.com/PermutaTriangle/Permuta",
    packages=['permuta'],
    long_description=read('README.md'),
    test_suite = 'tests'
)
