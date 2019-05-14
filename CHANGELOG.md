# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- The ascii_plot, and to_tikz method in MeshPatt
### Removed
- The broken latex method in MeshPatt

## [1.0.0] - 2019-04-15
### Added
- Made master branch deploy to PyPi.
- Added testing for Python 3.7 and 3.8.
- Added a from integer method, for creating a Perm from integer.
- Added inversions and non-inversions function that yield pairs.
### Changed
- Updated repr and str methods to Av, PermSetAll and PermSetStatic.
- The string of a Perm is now one-line notation.
- Can no longer initialise Perm with an integer.
### Removed
- The demo.
- Broken plot function
- Support for Python 3.4 and earlier.
### Fixed
- The ascii plot, and to_tikz method in Perm.
- Bug in polynomial checker.

## [0.1.1] - 2017-03-05
### Added
- Readme was rewritten in ReST.
- Classifiers and python versions added to setup.py.

## [0.1.0] - 2017-03-05
### Added
- This CHANGELOG file.
- Package added to PYPI
- Tests passing.
- Conforming to PEP8.
