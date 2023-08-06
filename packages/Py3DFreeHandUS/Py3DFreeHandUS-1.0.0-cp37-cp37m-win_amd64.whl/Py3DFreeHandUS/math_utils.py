# -*- coding: utf-8 -*-
"""
.. module:: math_utils
   :synopsis: module for analyzing image-based muscles properties

"""

import fractions
try:
    from functools import reduce
except:
    pass

def lcm(a, b):
    """Calculate least common multiple (LCM) between 2 numbers.

    Parameters
    ----------
    a, b : int
        Numbers.

    Returns
    -------
    int
        LCM

    """
    return abs(a * b) / fractions.gcd(a,b) if a and b else 0


def lcmm(*args):
    """Calculate least common multiple (LCM) between N numbers.

    Parameters
    ----------
    *args
        Numbers.

    Returns
    -------
    int
        LCM

    """
    return reduce(lcm, args)
