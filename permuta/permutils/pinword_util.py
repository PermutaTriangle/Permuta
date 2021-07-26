from fractions import Fraction
from typing import Callable, Dict, List, Tuple


class PinWordUtil:
    """Utility class for pinwords"""

    def __init__(self) -> None:
        self.caller: Dict[
            str, Callable[[List[Tuple[Fraction, Fraction]]], Tuple[Fraction, Fraction]]
        ] = {
            "1": self.char_1,
            "2": self.char_2,
            "3": self.char_3,
            "4": self.char_4,
            "U": self.char_u,
            "L": self.char_l,
            "D": self.char_d,
            "R": self.char_r,
        }
        self.zero = Fraction(0, 1)
        self.one = Fraction(1, 1)
        self.half = Fraction(1, 2)

    @staticmethod
    def rzero() -> Fraction:
        """Returns the fraction zero"""
        return Fraction(0, 1)

    def call(self, char, pre_perm) -> Tuple[Fraction, Fraction]:
        """Main help function"""
        return self.caller[char](pre_perm)

    def char_1(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        next_x = PinWordUtil.max_x(pre_perm) + self.one
        next_y = PinWordUtil.max_y(pre_perm) + self.one
        return next_x, next_y

    def char_2(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        next_x = PinWordUtil.min_x(pre_perm) - self.one
        next_y = PinWordUtil.max_y(pre_perm) + self.one
        return next_x, next_y

    def char_3(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        next_x = PinWordUtil.min_x(pre_perm) - self.one
        next_y = PinWordUtil.min_y(pre_perm) - self.one
        return next_x, next_y

    def char_4(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        next_x = PinWordUtil.max_x(pre_perm) + self.one
        next_y = PinWordUtil.min_y(pre_perm) - self.one
        return next_x, next_y

    def char_u(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        (last_x, _) = pre_perm[-1]
        if last_x > PinWordUtil.max_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.max_x(pre_perm[:-1]))
            next_y = PinWordUtil.max_y(pre_perm) + self.one
        elif last_x < PinWordUtil.min_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.min_x(pre_perm[:-1]))
            next_y = PinWordUtil.max_y(pre_perm) + self.one
        else:
            assert False
        return next_x, next_y

    def char_l(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        _, last_y = pre_perm[-1]
        if last_y > PinWordUtil.max_y(pre_perm[:-1]):
            next_x = PinWordUtil.min_x(pre_perm) - self.one
            next_y = self.half * (last_y + PinWordUtil.max_y(pre_perm[:-1]))
        elif last_y < PinWordUtil.min_y(pre_perm[:-1]):
            next_x = PinWordUtil.min_x(pre_perm) - self.one
            next_y = self.half * (last_y + PinWordUtil.min_y(pre_perm[:-1]))
        else:
            assert False
        return next_x, next_y

    def char_d(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        (last_x, _) = pre_perm[-1]
        if last_x > PinWordUtil.max_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.max_x(pre_perm[:-1]))
            next_y = PinWordUtil.min_y(pre_perm) - self.one
        elif last_x < PinWordUtil.min_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.min_x(pre_perm[:-1]))
            next_y = PinWordUtil.min_y(pre_perm) - self.one
        else:
            assert False
        return next_x, next_y

    def char_r(
        self, pre_perm: List[Tuple[Fraction, Fraction]]
    ) -> Tuple[Fraction, Fraction]:
        """."""
        _, last_y = pre_perm[-1]
        if last_y > PinWordUtil.max_y(pre_perm[:-1]):
            next_x = PinWordUtil.max_x(pre_perm) + self.one
            next_y = self.half * (last_y + PinWordUtil.max_y(pre_perm[:-1]))
        elif last_y < PinWordUtil.min_y(pre_perm[:-1]):
            next_x = PinWordUtil.max_x(pre_perm) + self.one
            next_y = self.half * (last_y + PinWordUtil.min_y(pre_perm[:-1]))
        else:
            assert False
        return next_x, next_y

    @staticmethod
    def min_x(pre_perm: List[Tuple[Fraction, Fraction]]) -> Fraction:
        """Utility function"""
        return min(pre_perm, key=lambda x: x[0])[0]

    @staticmethod
    def max_x(pre_perm: List[Tuple[Fraction, Fraction]]) -> Fraction:
        """Utility function"""
        return max(pre_perm, key=lambda x: x[0])[0]

    @staticmethod
    def min_y(pre_perm: List[Tuple[Fraction, Fraction]]) -> Fraction:
        """Utility function"""
        return min(pre_perm, key=lambda x: x[1])[1]

    @staticmethod
    def max_y(pre_perm: List[Tuple[Fraction, Fraction]]) -> Fraction:
        """Utility function"""
        return max(pre_perm, key=lambda x: x[1])[1]
