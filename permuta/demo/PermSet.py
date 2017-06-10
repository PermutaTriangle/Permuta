"""A wrapper around the permuta PermSet class."""


#import numbers
import tempfile
import webbrowser

#import numpy
import seaborn

from .Perm import Perm
from ..Perm import Perm as _ZBPerm
from ..PermSet import PermSet as _ZBPermSet


__all__ = ("Av", "PermutationClass")


class PermutationClass:
    def __init__(self, basis_perms, length):
        self.basis_perms = [Perm(perm) for perm in basis_perms]
        self.length = length
        self._zb_perm_set = _ZBPermSet.avoiding([basis_perm._zb_perm
                                                 for basis_perm
                                                 in self.basis_perms]).of_length(length)

    def list_all(self):
        for p in self._zb_perm_set:
            print(p)

    def heatmap(self, *, browser=False, filename=None, file_format="svg", **kwargs):
        # TODO: Perm class slice?
        """Display or save a heatmap of the perm class slice.

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
            Set the "cmap" kwarg to another map like "YlOrRd", "Reds", or "hot".
            Set the "cbar" kwarg to True to display the scale.
            Set the "vmax" kwarg to the length of the ??? to make it so that
            only an element that appears in all the perms gets the maximum
            color value.
            Set the "xticklabels" kwarg as range(???) for a labelled x-axis.
        """
        # Compile the data
        data = [[0]*self.length for _ in range(self.length)]
        for zb_perm in self._zb_perm_set:
            for index, value in enumerate(zb_perm):
                data[value][index] += 1
        data.reverse()

        # Create the figure
        axes = seaborn.heatmap(data,
                               **(dict(self.heatmap.default_kwargs, **kwargs)
                                  if kwargs else
                                  self.heatmap.default_kwargs))
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
                figure.savefig(file_pointer, format=file_format, bbox_inches="tight")
                file_pointer.flush()
                webbrowser.open(file_pointer.name)

        return axes, figure

    heatmap.default_kwargs = {  # TODO: Good place for default kwargs?
        "cbar": False,
        "cmap": "Greys",
        "square": True,
        "vmin": 0,
        "xticklabels": False,
        "yticklabels": False
    }


Av = PermutationClass
