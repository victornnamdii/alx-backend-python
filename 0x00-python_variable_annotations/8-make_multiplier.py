#!/usr/bin/env python3
"""
make multiplier
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Takes a float multiplier as argument and returns a function that
    multiplies a float by multiplier
    """
    def func1(number: float) -> float:
        """
        Multiplies a float with the multiplier
        """
        return multiplier * number

    return func1
