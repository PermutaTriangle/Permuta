# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
### Changed
- Updated `__str__` method of `Av` and `MeshPatt`.

## [1.3.0] - 2019-12-16
### Added
- `MeshPatt`s are now comparable (i.e. a mesh patt is always less then,
  equal to or greater than another mesh patt) and therefore sortable
- Added enumeration strategies that can point out to useful results to find the
  enumeration of a permutation class.

## [1.2.1] - 2019-09-10
### Fixed
- Allow for a mix of permutation and mesh patterns in MeshBasis

## [1.2.0] - 2019-09-05
### Added
- The `occurences_in` method of permutation can can handle coloured
  permutations.
- Support for containment of mesh pattern in a mesh pattern.

## [1.1.0] - 2019-08-26
### Added
- The ascii_plot, and to_tikz method in MeshPatt
- is_subclass method in Av
- Support for avoidance of mesh patterns with `Av`
### Removed
- The broken latex method in MeshPatt
### Fixed
- Wrong examples in the README. README.rst is now tested

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
