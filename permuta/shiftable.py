import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class Shiftable(ABC):

    @abc.abstractmethod
    def shift_right(self, times=1):
        """Return self shifted times steps to the right.

        If shift is negative, shifted to the left.
        """
        pass

    @abc.abstractmethod
    def shift_left(self, times=1):
        """Return self shifted times steps to the left.

        If times is negative, shifted to the right.
        """
        pass

    @abc.abstractmethod
    def shift_up(self, times=1):
        """Return self shifted times steps up.

        If times is negative, shifted down.
        """
        pass

    @abc.abstractmethod
    def shift_down(self, times=1):
        """Return self shifted times steps down.

        If times is negative, shifted up.
        """
        pass
