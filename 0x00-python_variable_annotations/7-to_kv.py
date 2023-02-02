#!/usr/bin/env python3
"""
to kv
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Returns a tuple containing k and v as a float
    """
    return (k, float(v ** 2))
