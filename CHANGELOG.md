# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
 - Statistic: bounce of a permutation.
 - Statistic: maximum drop size.
 - Statistic: number of primes in the column sums.
 - Statistic: holeyness of a permutation.
 - Algorith: `pop stack sort`.
 - Statistic: count stack sorts.
 - Statistic: count pop stack sorts.
 - Statistic: Pinnacle set and number of pinnacles.

### Changed
  - Functions for ascents and descents now take an optional argument to specify what step size to calculate.
  - Moved sortings functions from `permuta/bisc/perm_properties.py` to `permuta/patterns/perm.py`.

## 2.0.3 - 2021-04-28
### Added
 - using Github Actions for testing and deployment
 - `containment_to_tikz` method in `Perm` that returns an iterator of tikz pictures
   displaying occurrences of classical patterns in self.
 - `permuta.permutils.PermutationStatistic` to check statistic distribution in
   classes and preservation and transformation in bijections.

### Deprecated
 - Python 3.6 is no longer supported

## 2.0.2 - 2020-08-06
### Fixed
  - Include the type hints in the pypi release.

## 2.0.1 - 2020-07-23
### Fixed
  - Typing for `apply` in `Perm` fixed. It is now of the same base type as argument.

## 2.0.0 - 2020-07-20
### Added
  - Two new tools added to permtools. A command to check if a class has a regular
    insertion encoding, and a command to compute the lexicographically minimal
    basis.
  - Typing
  - pylint
  - `clear_cache` method in `Perm` and `Av`
  - `up_to_length`, `of_length`, `first` iterators in Perm and Av
  - `to_svg` for all patterns
  - `show` method for all patterns (opens browser tab)
  - Functions returning list (or other data structures) made into generators when possible
  - `BivincularPatt`, `VincularPatt`, `CovincularPatt` patterns,
  - `dihedral_group` generator added to `permutils`
  - `from_string` method to `Basis` and `Av`. It accepts both 0 and 1 based perms
    seperated by anything
  - Check if polynomial added to `cli`, which can be used with the `poly` command

### Fixed
  - Bisc's resource files now included with pypi package

### Changed
  - Type and condition checking and Exception throwing changed to assertions
  - `Basis` moved to `permset` module
  - `gen_meshpatt` moved to meshpatt as `of_length` generator
  - Client now uses `Basis.from_string` to parse basis

### Removed
  - Permsets and their interfaces
  - Unused algorithms and utils
  - Symmetric interfaces
  - All rotate function other than `rotate`
  - `descriptors` module
  - sympy dependency

## 1.5.0 - 2020-06-23
## Added
- A quick command line interface to compute the enumeration of a permutation class.
- `Perm.skew_decomposition` and `Perm.sum_decomposition` methods.

## 1.4.2 - 2020-06-17
### Fixed
- Make `permuta.bisc.permsets` a proper package.

## 1.4.1 - 2020-06-12
### Removed
- The unused `permuta.misc.misc` module

### Fixed
- Installation on windows

## 1.4.0 - 2020-05-11
### Added
- The BiSC algorithm that can tell you what mesh patterns are avoided by a set
  of permutations.

### Changed
- Updated `__str__` method of `Av` and `MeshPatt`.
- Introduce a more efficient algorithm to build permutation in a permutation
  class.

### Fixed
- `Av([])` returns `PermSetAll()`

### Removed
- Support for Python 3.5 and earlier

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
