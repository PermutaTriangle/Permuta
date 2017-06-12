# permuta

[![Build Status](https://travis-ci.org/PermutaTriangle/Permuta.svg?branch=master)](https://travis-ci.org/PermutaTriangle/Permuta)

Permuta is a Python library for working with perms (short for permutations) and
mesh patts (short for mesh patterns).

## Installing

To install Permuta on your system, simply run the following command as a
superuser:

```
# ./setup.py install
```

It is also possible to install Permuta in development mode, in which case you
run the following instead:

```
# ./setup.py develop
```

To run the unit tests using pytest run

```
pytest --cov permuta tests
```

This requires `pytest` and `pytest-cov`.

## Demo

Once you've installed Permuta, it can be imported by a Python script or an
interactive Python session, just like any other Python library.

```python
>>> from permuta.demo import *
```

For this section we focus on a subset of modified features exposed in the `demo`
submodule. Importing `*` from it supplies you with the Perm and PermClass
classes (and their aliases Permutation and Av).

### Creating a single perm

There are several ways of creating a perm:

```python
>>> Perm()  # Empty perm
()
>>> Perm([])  # Another empty perm
()
>>> Perm(132)  # From number
(1, 3, 2)
>>> Perm(248)  # Attempted interpretation
(1, 2, 3)
>>> Perm("1234")  # From string
(1, 2, 3, 4)
>>> Perm("dcab")  # This is equivalent to ...
(4, 3, 1, 2)
>>> Perm(["d", "c", "a", "b"])  # ... this
(4, 3, 1, 2)
>>> Perm(0, 0, 2, 1)  # Index is tie-breaker
(1, 2, 4, 3)
>>> Perm("Ragnar", "Christian", "Henning")
(3, 1, 2)
```

You can visualize a perm:

```python
>>> import matplotlib.pyplot as plt
>>> p = Perm((1, 3, 2, 4))
>>> ax = p.plot()
>>> plt.show()
```

![alt text](https://github.com/PermutaTriangle/Permuta/img/american-mink.jpg "Plot of a perm")

The basic symmetries are implemented:

```python
>>> [p.reverse(), p.complement(), p.inverse()]
 [Perm((4, 2, 3, 1), Perm((4, 2, 3, 1)), Perm((1, 3, 2, 4))]
```

To take direct sums and skew sums we use `+` and `-`:

```python
>>> q = Perm((1, 2, 3, 4, 5))
>>> p + q
(1, 3, 2, 4, 5, 6, 7, 8, 9)
>>> p - q
(6, 8, 7, 9, 1, 2, 3, 4, 5)
```

There are several functions, or perm statistics, you can apply t

```python
>>> [p.count_ascents(), p.count_inversions(), p.count_fixed_points(), p.length_of_longestrun(), p.majorindex(), p.count_cycles()]
 [2, 1, 2, 2, 2, 3]
```

```python
>>> [p.count_peaks(), p.count_ltrmin(), p.count_bonds(), p.count_valleys()]
 [1, 1, 1, 1]
```

### Creating the set of permutations of a specific length
Typing

```python
>>> A = PermSet(6)
>>> A
 <PermSet of all perms of length 6>
```

creates the set of permutations of six elements. You can choose a random
permutation by doing

```python
>>> p = A.random()
>>> p
 Perm((3, 2, 5, 0, 4, 1))
```

### Avoiding patterns
Given a list of pattern `L` we can create the permutation class representing all
permutations that avoid every pattern in `L`

```python
>>> B = PermSet.avoiding([Perm((0, 1, 2)), Perm((0, 2, 1))])
>>> B
 <The set of all perms avoiding Basis((Perm((0, 1, 2)), Perm((0, 2, 1))))>
```

We can ask whether a specific permutation `q` belongs to B
```python
>>> B.contains(Perm((2, 0, 1, 3)))
 False
```

If you want all permutations of length six in B you can do

```python
>>> C = B.of_length(6)
>>> C
 <PermSet of all perms of length 6 avoiding Basis((Perm((0, 1)),))>
```

If you want permutations of length up to and including six you can do

```python
>>> D = B.up_to(7)
```

Note that we follow the usual range convention of Python of not including the
last element.

Note that if you later want permutations up to length eight in this class you
can do

```python
>>> D = B.up_to(9)
```

and this will use the work that was done in computing `B.up_to(7)` and not do the
work all over again.

### Statistics on sets of permutations

If we have a statistic we want to apply to an entire set of permutations of a
certain length we do

```python
>>> E = PermSet.avoiding(Perm((0,2,1,3))) # note that we do not need to put a single pattern in a list
>>> E.of_length(8).total_statistic(Perm.inversions)
 XXX
```

For the distribution (as a polynomial you can do)

```python
>>> E[8].distribution(Perm.inversions)
 XXX
```

To get a feeling for what an average permutation looks like you can create a
heatmap

```python
>>> C = PermSet.avoiding(Permutation((0, 2, 1, 3)))[9]
>>> C.heatmap()
```

![alt text](https://github.com/PermutaTriangle/Permuta/img/american-mink.jpg "Plot of a permutation")

## License
BSD-3: see the [LICENSE](https://github.com/PermutaTriangle/Permuta/blob/master/LICENSE) file.
