import abc

from ..PermSetBase import PermSetBase


class PermSetFinite(PermSetBase):
    """Base class for all finite perm sets."""
    @abc.abstractmethod
    def random(self):
        # Return a random element from the range
        # Only possible due to the perm set being finite
        pass
