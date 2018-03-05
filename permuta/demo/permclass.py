"""A wrapper around the permuta PermSet class."""


import tempfile
import warnings
import webbrowser

from ..permset import PermSet as _ZBPermSet
from .perm import Perm

try:
    import seaborn
    _SEABORN_AVAILABLE = True
except ImportError:
    _SEABORN_AVAILABLE = False
    warnings.warn("Unable to load seaborn for Perm plotting")


__all__ = ("Av", "PermClass")


class PermClass:
    """A perm(utation) class object.

    Pass it an iterable of Perms or something that can be interpreted as such.
    Each non-Perm element is passed to the Perm constructor.

    Examples:
        >>> PermClass()
        <All perms>
        >>> PermClass(["1423", "1234"])
        <Perms avoiding: (1, 2, 3, 4) and (1, 4, 2, 3)>
        >>> PermClass([123, "321", Perm(3, 1, 2)])
        <Perms avoiding: (1, 2, 3), (3, 1, 2), and (3, 2, 1)>
        >>> PermClass([62, 123])
        <Perms avoiding: (2, 1) and (1, 2, 3)>
    """
    def __init__(self, basis=()):
        try:
            self._zb_perm_set = _ZBPermSet.avoiding(
                Perm(basis_element)._zb_perm for basis_element in basis)
            self.basis = tuple(Perm(basis_element)
                               for basis_element
                               in self._zb_perm_set.basis)
        except Exception:
            format_string = "Don't know how to get a basis from args: {}"
            message = format_string.format(basis)
            raise ValueError(message)

    def __repr__(self):
        if len(self.basis) > 0:
            repr_string_parts = ["<Perms avoiding: "]
            if len(self.basis) == 1:
                repr_string_parts.append(repr(self.basis[0]))
                repr_string_parts.append(">")
            elif len(self.basis) == 2:
                repr_string_parts.append(repr(self.basis[0]))
                repr_string_parts.append(" and ")
                repr_string_parts.append(repr(self.basis[1]))
                repr_string_parts.append(">")
            else:
                for basis_perm_index in range(len(self.basis) - 1):
                    basis_perm = self.basis[basis_perm_index]
                    repr_string_parts.append(repr(basis_perm))
                    repr_string_parts.append(", ")
                repr_string_parts.append("and ")
                repr_string_parts.append(repr(self.basis[-1]))
                repr_string_parts.append(">")
            repr_string = "".join(repr_string_parts)
            return repr_string
        else:
            return "<All perms>"

    def of_length(self, length):
        """Return the subset of perms of a certain length."""
        return _PermClassOfLength(self, length)

    def __iter__(self):
        for zb_perm in self._zb_perm_set:
            yield Perm(zb_perm)

    def __getitem__(self, index):
        return Perm(self._zb_perm_set[index])

    def __contains__(self, perm):
        perm = Perm(perm)
        return perm._zb_perm in self._zb_perm_set

    def __eq__(self, other):
        return (isinstance(other, PermClass) and
                self._zb_perm_set == other._zb_perm_set)

    def __hash__(self):
        return hash(self._zb_perm_set)


Av = PermClass


class _PermClassOfLength:
    def __init__(self, parent, length):
        self._parent = parent
        self.length = length
        self._zb_perm_subset = parent._zb_perm_set.of_length(length)

    def plot(self, *, browser=False, filename=None, file_format=None,
             **kwargs):
        """Display or save a heatmap with seaborn/matplotlib.

        Returns the Axes object or None if seaborn is unavailable.

        Keyword arguments:
            browser: If True, sends the image to a browser for viewing.
            filename: Where to save the image.
            file_format: The file format if one wishes to force one.

        Other keyword arguments are passed to seaborn.heatmap.
        The default keyword arguments passed are:
            cbar=False
            cmap="Greys"
            square=True
            vmin=0
            xticklabels=False
            yticklabels=False

        Tips:
            Set the "vmax" kwarg to 0 if you want a scale over all the perms.
            Set the "cmap" kwarg to another map like "YlOrRd", "Reds", or
            "hot".
            Set the "cbar" kwarg to True to display the scale.
            Set the "vmax" kwarg to len(self) to make it so that only an
            element that appears in all the perms gets the maximum color value.
            Set the "xticklabels" kwarg as range(self.length) for a labelled
            x-axis.
        """
        if not _SEABORN_AVAILABLE:
            return None

        # Compile the data
        data = [[0]*self.length for _ in range(self.length)]
        for zb_perm in self._zb_perm_subset:
            for index, value in enumerate(zb_perm):
                data[value][index] += 1
        data.reverse()

        # Create the figure
        axes = seaborn.heatmap(data,
                               **(dict(self.plot.default_kwargs, **kwargs)
                                  if kwargs else
                                  self.plot.default_kwargs))
        figure = axes.get_figure()

        # Possibly display and/or save the figure
        if filename:
            figure.savefig(filename,
                           format=file_format,
                           bbox_inches="tight",
                           pad_inches=0)
            if browser:
                webbrowser.open(filename)
        elif browser:
            with tempfile.NamedTemporaryFile(delete=False) as file_pointer:
                figure.savefig(
                    file_pointer,
                    format="svg" if file_format is None else file_format,
                    bbox_inches="tight")
                file_pointer.flush()
                webbrowser.open(file_pointer.name)

        return axes

    plot.default_kwargs = {  # TODO: Good place for default kwargs?
        "cbar": False,
        "cmap": "Greys",
        "square": True,
        "vmin": 0,
        "xticklabels": False,
        "yticklabels": False
    }

    def __iter__(self):
        for zb_perm in self._zb_perm_subset:
            yield Perm(zb_perm)

    def __getitem__(self, index):
        return Perm(self._zb_perm_subset[index])

    def __contains__(self, perm):
        perm = Perm(perm)
        return perm._zb_perm in self._zb_perm_subset

    def __len__(self):
        return len(self._zb_perm_subset)

    def __repr__(self):
        parent_repr = repr(self._parent)
        if parent_repr == "<All perms>":
            return "<All perms of length {}>".format(self.length)
        else:
            return "{}of length {} {}".format(parent_repr[:7],
                                              self.length,
                                              parent_repr[7:])
