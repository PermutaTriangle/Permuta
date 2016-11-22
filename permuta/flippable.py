import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class Flippable(ABC):

    @abc.abstractmethod
    def flip_horizontal(self):
        """Return self flipped horizontally."""
        pass

    @abc.abstractmethod
    def flip_vertical(self):
        """Return self flipped vertically."""
        pass

    @abc.abstractmethod
    def flip_diagonal(self):
        """Return self flipped along the diagonal."""
        pass

    @abc.abstractmethod
    def flip_antidiagonal(self):
        """Return self flipped along the antidiagonal."""
        pass
