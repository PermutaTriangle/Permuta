Installing
##########

To install Permuta on your system, simply run the following command as
a superuser::

    ./setup.py install

It is also possible to install Permuta in development mode, in which case you
run the following instead::

    ./setup.py develop

To run the unit tests, you can run the following command::

    ./setup.py test


Once you've installed Permuta, it can be imported into a Python script just like any other Python library::

    from permuta import Permutation, MeshPattern
