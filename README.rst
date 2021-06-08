#######
permuta
#######

.. image:: https://travis-ci.org/PermutaTriangle/Permuta.svg?branch=master
    :alt: Travis
    :target: https://travis-ci.org/PermutaTriangle/Permuta
.. image:: https://img.shields.io/pypi/v/Permuta.svg
    :alt: PyPI
    :target: https://pypi.python.org/pypi/Permuta
.. image:: https://img.shields.io/pypi/l/Permuta.svg
    :target: https://pypi.python.org/pypi/Permuta
.. image:: https://img.shields.io/pypi/pyversions/Permuta.svg
    :target: https://pypi.python.org/pypi/Permuta
.. image:: http://img.shields.io/badge/readme-tested-brightgreen.svg
    :alt: Travis
    :target: https://travis-ci.org/PermutaTriangle/Permuta
.. image:: https://requires.io/github/PermutaTriangle/Permuta/requirements.svg?branch=master
    :target: https://requires.io/github/PermutaTriangle/Permuta/requirements/?branch=master
    :alt: Requirements Status
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4725759.svg
   :target: https://doi.org/10.5281/zenodo.4725759

Permuta is a Python library for working with perms (short for permutations),
patterns, and mesh patterns.

If you need support, you can join us in our `Discord support server`_.

.. _Discord support server: https://discord.gg/ngPZVT5

Installing
==========

To install Permuta on your system, run:

.. code-block:: bash

    pip install permuta

It is also possible to install Permuta in development mode to work on the
source code, in which case you run the following after cloning the repository:

.. code-block:: bash

    ./setup.py develop

To run the unit tests:

.. code-block:: bash

    pip install -r test_requirements.txt
    ./setup.py test

Using Permuta
#############

Once you've installed Permuta, it can be imported by a Python script or an
interactive Python session, just like any other Python library:

.. code-block:: python

    >>> from permuta import *

Importing ``*`` from it supplies you with the 'Perm' and 'PermSet'
classes along with the 'AvoidanceClass' class (with alias 'Av') for generating
perms avoiding a set of patterns. It also gives you the 'MeshPatt' class
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

Printing perms gives zero-based strings.

.. code-block:: python

    >>> print(Perm(()))
    ε
    >>> print(Perm((2, 1, 0)))
    210
    >>> print(Perm((6, 2, 10, 9, 3, 8, 0, 1, 5, 11, 4, 7)))
    (6)(2)(10)(9)(3)(8)(0)(1)(5)(11)(4)(7)

The avoids, contains, and occurrence methods enable working with patterns:

.. code-block:: python

    >>> p = Perm((0,2,1,3))
    >>> p.contains(Perm((2, 1, 0)))
    False
    >>> p.avoids(Perm((0, 1)))
    False
    >>> list(p.occurrences_of(Perm((1, 0))))
    [(1, 2)]
    >>> list(Perm((0, 1)).occurrences_in(p))
    [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]

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
    Perm((5, 7, 6, 8, 0, 1, 2, 3, 4))

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

Perm classes are specified with a basis:

.. code-block:: python

    >>> basis = Basis(Perm((1, 0, 2)), Perm((1, 2, 0)))
    >>> basis
    Basis((Perm((1, 0, 2)), Perm((1, 2, 0))))
    >>> perm_class = Av(basis)
    >>> perm_class
    Av(Basis((Perm((1, 0, 2)), Perm((1, 2, 0)))))

You can ask whether a perm belongs to the perm class:

.. code-block:: python

    >>> Perm((3, 2, 1, 0)) in perm_class
    True
    >>> Perm((0, 2, 1, 3)) in perm_class
    False

You can get its enumeration up to a fixed length.

.. code-block:: python

    >>> perm_class.enumeration(10)
    [1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    >>> perm_class.count(11)
    1024

You can also look to see if some well know enumeration strategies apply to a
given class.

.. code-block:: python

    >>> from permuta.enumeration_strategies import find_strategies
    >>> basis = [Perm((3, 2, 0, 1)), Perm((1, 0, 2, 3))]
    >>> for strat in find_strategies(basis):
    ...     print(strat.reference())
    The insertion encoding of permutations: Corollary 10
    >>> basis = [Perm((1, 2, 0, 3)), Perm((2, 0, 1, 3)), Perm((0, 1, 2, 3))]
    >>> for strat in find_strategies(basis):
    ...     print(strat.reference())
    Enumeration of Permutation Classes and Weighted Labelled Independent Sets: Corollary 4.3

Permutation statistics
######################

With the ``PermutationStatistic`` class we can look for distributions of statistics for
classes and look for statistics preservations (or transformation) either for two classes
or given a bijection. First we need to import it.

.. code-block:: python

    >>> from permuta.permutils.statistics import PermutationStatistic

To see a distribution for a given statistic we grab its instance and provide a length
and a class (no class will use the set of all permutations).

.. code-block:: python

    >>> PermutationStatistic.show_predefined_statistics() # Show all statistics with id
    [0] Number of inversions
    [1] Number of non-inversions
    [2] Major index
    [3] Number of descents
    [4] Number of ascents
    [5] Number of peaks
    [6] Number of valleys
    [7] Number of cycles
    [8] Number of left-to-right minimas
    [9] Number of left-to-right maximas
    [10] Number of right-to-left minimas
    [11] Number of right-to-left maximas
    [12] Number of fixed points
    [13] Order
    [14] Longest increasing subsequence
    [15] Longest decreasing subsequence
    [16] Depth
    [17] Number of bounces
    [18] Maximum drop size
    [19] Number of primes in the column sums
    [20] Holeyness of a permutation
    [21] Number of stack-sorts needed
    [22] Number of pop-stack-sorts needed
    [23] Number of pinnacles
    [24] Number of cyclic peaks
    [25] Number of cyclic valleys
    [26] Number of double excedance
    [27] Number of double drops
    [28] Number of foremaxima
    [29] Number of afterminima

    >>> depth = PermutationStatistic.get_by_index(16)
    >>> depth.distribution_for_length(5)
    [1, 4, 12, 24, 35, 24, 20]
    >>> depth.distribution_up_to(4, Av.from_string("123"))
    [[1], [1], [1, 1], [0, 2, 3], [0, 0, 3, 7, 4]]

Given a bijection as a dictionary, we can check which statistics are preserved with 
``check_all_preservations`` and which are transformed with ``check_all_transformed``

.. code-block:: python

    >>> bijection = {p: p.reverse() for p in Perm.up_to_length(5)}
    >>> for stat in PermutationStatistic.check_all_preservations(bijection):
    ...     print(stat)
    Number of peaks
    Number of valleys
    Holeyness of a permutation
    Number of pinnacles

We can find all (predefined) statistics equally distributed over two permutation
classes with ``equally_distributed``. We also support checks for joint distribution
of more than one statistics with ``jointly_equally_distributed`` and transformation
of jointly distributed stats with ``jointly_transformed_equally_distributed``.

.. code-block:: python

    >>> cls1 = Av.from_string("2143,415263")
    >>> cls2 = Av.from_string("3142")
    >>> for stat in PermutationStatistic.equally_distributed(cls1, cls2, 6):
    ...     print(stat)
    Major index
    Number of descents
    Number of ascents
    Number of peaks
    Number of valleys
    Number of left-to-right minimas
    Number of right-to-left maximas
    Longest increasing subsequence
    Longest decreasing subsequence
    Number of pinnacles

The BiSC algorithm
==================

The BiSC algorithm can tell you what mesh patterns are avoided by a set of
permutations. Although the output of the algorithm is only guaranteed to
describe the finite inputted set of permutations, the user usually hopes that
the patterns found by the algorithm describe an infinite set of permutatations.
To use the algorithm we first need to import it.

.. code-block:: python

    >>> from permuta.bisc import *

A classic example of a set of permutations described by pattern avoidance are
the permutations sortable in one pass through a stack. We use the function
``stack_sortable`` which returns ``True`` for permutations that satisfy this
property. The user now has two choices: Run
``auto_bisc(Perm.stack_sortable)`` and let the algorithm run
without any more user input. It will try to use sensible values, starting by
learning small patterns from small permutations, and only considering longer
patterns when that fails. If the user wants to have more control over what
happens that is also possible and we now walk through that: We input the
property into ``bisc`` and ask it to search for patterns of length 3.

.. code-block:: python

    >>> bisc(Perm.stack_sortable, 3)
    I will use permutations up to length 7
    {3: {Perm((1, 2, 0)): [set()]}}

When this command is run without specifying what length of permutations you
want to consider, ``bisc`` will create permutations up to length 7 that satisfy
the property of being stack-sortable. The output means: There is a single
length 3 pattern found, and its underlying classical pattern is the permutation
``Perm((1, 2, 0))``. Ignore the ``[set()]`` in the output for now. We can use
``show_me`` to get a better visualization of the patterns found. In this call
to the algorithm we also specify that only permutations up to length 5 should
be considered.

.. code-block:: python

    >>> SG = bisc(Perm.stack_sortable, 3, 5)
    >>> show_me(SG)
    There are 1 underlying classical patterns of length 3
    There are 1 different shadings on 120
    The number of sets to monitor at the start of the clean-up phase is 1
    <BLANKLINE>
    Now displaying the patterns
    <BLANKLINE>
     | | |
    -+-●-+-
     | | |
    -●-+-+-
     | | |
    -+-+-●-
     | | |
    <BLANKLINE>

We should ignore the ``The number of sets to monitor at the start of the clean-up phase
is 1`` message for now.

We do not really need this algorithm for sets of permutations described by the
avoidance of classical patterns. Its main purpose is to describe sets with mesh
patterns, such as the West-2-stack-sortable permutations

.. code-block:: python

    >>> SG = bisc(Perm.west_2_stack_sortable, 5, 7)
    >>> show_me(SG)
    There are 2 underlying classical patterns of length 4
    There are 1 different shadings on 1230
    There are 1 different shadings on 2130
    The number of sets to monitor at the start of the clean-up phase is 1
    There are 1 underlying classical patterns of length 5
    There are 1 different shadings on 42130
    <BLANKLINE>
    Now displaying the patterns
    <BLANKLINE>
     | | | |
    -+-+-●-+-
     | | | |
    -+-●-+-+-
     | | | |
    -●-+-+-+-
     | | | |
    -+-+-+-●-
     | | | |
    <BLANKLINE>
     |▒| | |
    -+-+-●-+-
     | | | |
    -●-+-+-+-
     | | | |
    -+-●-+-+-
     | | | |
    -+-+-+-●-
     | | | |
    <BLANKLINE>
     |▒| | | |
    -●-+-+-+-+-
     | |▒| | |
    -+-+-+-●-+-
     | | | | |
    -+-●-+-+-+-
     | | | | |
    -+-+-●-+-+-
     | | | | |
    -+-+-+-+-●-
     | | | | |
    <BLANKLINE>

This is good news and bad news. Good because we quickly got a description of the
set we were looking at, that would have taken a long time to find by hand. The bad news
is that there is actually some redundancy in the output. To understand better what is
going on we will start by putting the permutations under investigation in a dictionary,
which keeps them separated by length.

.. code-block:: python

    >>> A, B = create_bisc_input(7, Perm.west_2_stack_sortable)

This creates two dictionaries with keys 1, 2, ..., 7 such that ``A[i]`` points
to the list of permutations of length ``i`` that are West-2-stack-sortable, and
``B[i]`` points to the complement. We can pass the A dictionary directly into
BiSC since only the permutations satisfying the property are used to find the
patterns. We can use the second dictionary to check whether every permutation
in the complement contains at least one of the patterns we found.

.. code-block:: python

    >>> SG = bisc(A, 5, 7)
    >>> patterns_suffice_for_bad(SG, 7, B)
    Starting sanity check with bad perms
    Now checking permutations of length 0
    Now checking permutations of length 1
    Now checking permutations of length 2
    Now checking permutations of length 3
    Now checking permutations of length 4
    Now checking permutations of length 5
    Now checking permutations of length 6
    Now checking permutations of length 7
    Sanity check passes for the bad perms
    (True, [])

In this case it is true that every permutation in B, up to length 7, contains
at least one of the patterns found. Had that not been the case a list of
permutations would have been outputted (instead of just the empty list).

Now, we claim that there is actually redundancy in the patterns we found, and
the length 4 mesh patterns should be enough to describe the set. This can occur
and it can be tricky to theoretically prove that one mesh pattern is implied
by another pattern (or a set of others, as is the case here). We use the dictionary
``B`` again and run

.. code-block:: python

    >>> bases, dict_numbs_to_patts = run_clean_up(SG, B)
    <BLANKLINE>
    The bases found have lengths
    [2]

There is one basis of mesh patterns found, with 2 patterns

.. code-block:: python

    >>> show_me_basis(bases[0], dict_numbs_to_patts)
    <BLANKLINE>
    Displaying the patterns in the basis
    <BLANKLINE>
     | | | |
    -+-+-●-+-
     | | | |
    -+-●-+-+-
     | | | |
    -●-+-+-+-
     | | | |
    -+-+-+-●-
     | | | |
    <BLANKLINE>
     |▒| | |
    -+-+-●-+-
     | | | |
    -●-+-+-+-
     | | | |
    -+-●-+-+-
     | | | |
    -+-+-+-●-
     | | | |
    <BLANKLINE>

This is the output we were expecting. There are several other properties of
permutations that can be imported from ``permuta.bisc.perm_properties``, such
as ``smooth``, ``forest-like``, ``baxter``, ``simsun``, ``quick_sortable``, etc.

Both ``bisc`` and ``auto_bisc`` can accept input in the form of a property,
or a list of permutations (satisfying some property).

License
#######

BSD-3: see the `LICENSE <https://github.com/PermutaTriangle/Permuta/blob/master/LICENSE>`_ file.

Citing
######

If you found this library helpful with your research and would like to cite us, 
you can use the following `BibTeX`_ or go to `Zenodo`_ for alternative formats. 

.. _BibTex: https://zenodo.org/record/4725759/export/hx#.YImTibX7SUk

.. _Zenodo: https://doi.org/10.5281/zenodo.4725759