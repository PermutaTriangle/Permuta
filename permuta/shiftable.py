import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class Shiftable(ABC):

    @abc.abstractmethod
    def shift_right(self, times=1):
        """Return self shifted times steps to the right.

        If shift is negative, shifted to the left.
        """
        pass

    shift = shift_right
    cyclic_shift = shift_right
    cyclic_shift_right = shift_right

    def shift_left(self, times=1):
        """Return self shifted times steps to the left.

        If times is negative, shifted to the right.
        """
        return self.shift_right(-times)

    cyclic_shift_left = shift_left

    @abc.abstractmethod
    def shift_up(self, times=1):
        """Return self shifted times steps up.

        If times is negative, shifted down.
        """
        pass

    def shift_down(self, times=1):
        """Return self shifted times steps down.

        If times is negative, shifted up.
        """
        return self.shift_up(-times)
