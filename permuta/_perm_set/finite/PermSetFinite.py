import abc

from ..PermSetBase import PermSetBase


class PermSetFinite(PermSetBase):
    @abc.abstractmethod
    def random(self):
        # Return a random element from the range
        # Only possible due to it being finite
        pass
