#######
permuta
#######

.. image:: https://travis-ci.org/PermutaTriangle/Permuta.svg?branch=master
    :alt: Travis
    :target: https://travis-ci.org/PermutaTriangle/Permuta
.. image:: https://coveralls.io/repos/github/PermutaTriangle/Permuta/badge.svg?branch=master
    :alt: Coveralls
    :target: https://coveralls.io/github/PermutaTriangle/Permuta?branch=master
.. image:: https://img.shields.io/pypi/v/Permuta.svg
    :alt: PyPI
    :target: https://pypi.python.org/pypi/Permuta
.. image:: https://img.shields.io/pypi/l/Permuta.svg
    :target: https://pypi.python.org/pypi/Permuta
.. image:: https://img.shields.io/pypi/pyversions/Permuta.svg
    :target: https://pypi.python.org/pypi/Permuta

Permuta is a Python library for working with perms (short for permutations),
patts (patterns), and mesh patts.

Installing
==========

To install Permuta on your system, simply run the following command as a superuser:
.. code-block:: bash

    # pip install permuta

It is also possible to install Permuta in development mode to work on the
source code, in which case you run the following after cloning the repository:

.. code-block:: bash

    # ./setup.py develop

To run the unit tests using pytest run:
.. code-block:: bash

    # ./setup.py test

This requires ``pytest``, ``pytest-cov``, ``pytest-pep8`` and ``pytest-isort``.

Using Permuta
#############

Once you've installed Permuta, it can be imported by a Python script or an
interactive Python session, just like any other Python library:

.. code-block:: python

    >>> from permuta import *

Importing ``*`` from it supplies you with the 'Perm' and 'PermSet'
classes along with the 'AvoidanceClass' class (with alias 'Av') for generating
permutations avoiding a set of patterns. It also gives you the 'MeshPatt' class
and some other submodules which we will not discuss in this readme.

Creating a single perm
######################

Permutations are zero-based in Permuta and can be created using any iterable.

.. code-block:: python

    >>> Perm()  # Empty perm
    Perm(())
    >>> Perm([])  # Another empty perm
    Perm(())
    >>> Perm((0, 1, 2, 3)) # The zero-based version of 1234
    Perm((0, 1, 2, 3))
    >>> Perm((2, 1, 3)) # Warning: it will initialise with any iterable
    Perm((2, 1, 3))
    >>> Perm((2, 1, 3), check=True) # If you are unsure, you can check
    ValueError: Element out of range: 3
    >>> Perm((4, 2, 3, 0, 0), check=True)
    ValueError: Duplicate element: 0
    >>> Perm("123", check=True)
    TypeError: ''1'' object is not an integer

Permutations can also be created using some specific class methods.

.. code-block:: python

    >>> Perm.from_string("201")  # strings
    Perm((2, 0, 1))
    >>> Perm.one_based((1, 3, 2, 4)) # one-based iterable of integers
    Perm((0, 2, 1, 3))
    >>> Perm.to_standard("a2gsv3") # standardising any iterable using '<'
    Perm((2, 0, 3, 4, 5, 1))
    >>> Perm.from_integer(210) # an integer between 0 and 9876543210
    Perm((2, 1, 0))
    >>> Perm.from_integer(321) # any integer given is standardised
    Perm((2, 1, 0))
    >>> Perm.from_integer(201)
    Perm((2, 0, 1))

Printing Perm is done as a zero-based strings

.. code-block:: python

    >>> print(Perm(()))
    ε
    >>> print(Perm((2, 1, 0)))
    210
    >>> print(Perm((6, 2, 10, 9, 3, 8, 0, 1, 5, 11, 4, 7))
    62(10)938015(11)47

The avoids, contains, and occurrence methods enable working with patts:

.. code-block:: python

    >>> p = Perm((0,2,1,3))
    Perm((0,2,1,3))
    >>> p.contains(Perm((2, 1, 0)))
    False
    >>> p.avoids(Perm((0, 1)))
    False
    >>> p.occurrences_of(Perm((1, 0)))
    [[3, 2]]
    >>> Perm((0, 1)).occurrences_in(p)
    [[1, 3], [1, 2], [1, 4], [3, 4], [2, 4]]

The basic symmetries are implemented:

.. code-block:: python

    >>> [p.reverse(), p.complement(), p.inverse()]
    [Perm((3, 1, 2, 0)), Perm((3, 1, 2, 0)), Perm((0, 2, 1, 3))]

To take direct sums and skew sums we use ``+`` and ``-``:

.. code-block:: python

    >>> q = Perm((0, 1, 2, 3, 4))
    >>> p + q
    Perm((0, 2, 1, 3, 4, 5, 6, 7, 8))
    >>> p - q
    Perm((4, 5, 6, 7, 8, 0, 2, 1, 3))

There are numerous practical methods available:

.. code-block:: python

    >>> list(p.fixed_points())
    [0, 3]
    >>> list(p.ascents())
    [0, 2]
    >>> list(p.descents())
    [1]
    >>> list(p.inversions())
    [(1, 2)]
    >>> p.major_index()
    2

Creating a perm class
#####################

You might want the set of all perms:

.. code-block:: python

    >>> all_perms = PermClass()
    >>> all_perms
    <All perms>

Perm classes can be specified with a basis:

.. code-block:: python

    >>> basis = [213, Perm((2, 3, 1))]
    >>> basis
    [213, (2, 3, 1)]
    >>> perm_class = Av(basis)
    >>> perm_class
    <Perms avoiding: (2, 1, 3) and (2, 3, 1)>

Recall that Av is just an alias of PermClass.

You can ask whether a perm belongs to the perm class:

.. code-block:: python

    >>> 4321 in perm_class
    True
    >>> 1324 in perm_class
    False

You can get the n-th perm of the class or iterate:

.. code-block:: python

    >> [perm_class[n] for n in range(10)]
    [(), (1), (1, 2), (2, 1), (1, 2, 3), (1, 3, 2), (3, 2, 1), (3, 1, 2), (4, 3, 2, 1), (4, 1, 3, 2)]
    >>> perm_class_iter = iter(perm_class)
    >>> [next(perm_class_iter) for _ in range(10)]
    [(), (1), (1, 2), (2, 1), (1, 2, 3), (1, 3, 2), (3, 2, 1), (3, 1, 2), (4, 3, 2, 1), (4, 1, 3, 2)]

(BEWARE: Lexicographic order is not guaranteed at the moment!)

The subset of a perm class where the perms are a specific length
################################################################

You can define a subset of perms of a specific length in the perm class:

.. code-block:: python

    >>> perm_class_14 = perm_class.of_length(14)
    >>> perm_class_14
    <Perms of length 14 avoiding: (2, 1, 3) and (2, 3, 1)>

You can ask for the size of the subset because it is guaranteed to be finite:

.. code-block:: python

    >>> len(perm_class_14)
    8192

The iterating and containment functionality is the same as with `perm_class`,
but indexing has yet to be implemented:

.. code-block:: python

    >>> 321 in perm_class_14
    False
    >>> (1, 14, 2, 13, 3, 4, 5, 12, 6, 11, 7, 8, 9, 10) in perm_class_14
    True
    >>> Perm(range(10)) - Perm(range(4)) in perm_class_14
    False
    >>> next(iter(perm_class_14))
    (14, 1, 2, 3, 4, 5, 13, 12, 11, 10, 6, 9, 7, 8)

To get a feeling for the perm class, you can plot a heatmap of this subset
 using matplotlib/seaborn:

.. code-block:: python

    >>> ax = perm_class_14.plot()
    >>> plt.show()

.. figure:: README.d/av_213_231_of_length_14_heatmap.png
    :align: center

    A heatmap plot for the perms of length 14 avoiding 213 and 231


Life in Permuta beyond the demo
###############################

If your work has reached a place where your require functionality beyond
that offered by the demo, it may be time to proceed to the non-demo version
of Permuta. The first hurdle will be coming to terms with the zero based indexing.
Here's how to get started:

.. code-block:: python

    >>> from permuta import Perm, PermSet, MeshPatt

License
#######

BSD-3: see the `LICENSE <https://github.com/PermutaTriangle/Permuta/blob/master/LICENSE>`_ file.
