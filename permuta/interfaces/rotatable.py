import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class Rotatable(ABC):

    def rotate(self, times=1):
        """Return self rotated 90 degrees to the right."""
        return self._rotate(times)

    rotate_right = rotate

    def rotate_left(self, times=1):
        """Return self rotated 90 degrees to the left."""
        return self._rotate(-times)

    def _rotate(self, times=1):
        """Return self rotated 90 times times degrees to the right."""
        times = times % 4
        if times == 0:
            return self
        elif times == 1:
            return self._rotate_right()
        elif times == 2:
            return self._rotate_180()
        else:
            return self._rotate_left()

    def _rotate_180(self):
        """Return self rotated 180 degrees."""
        return self._rotate_right()._rotate_right()

    def _rotate_left(self):
        """Return self rotated 90 degrees left."""
        return self._rotate_180()._rotate_right()
        pass

    @abc.abstractmethod
    def _rotate_right(self):
        """Return self rotated 90 degrees right."""
        pass
