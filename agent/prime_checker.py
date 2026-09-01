"""
Prime checking utilities.

This module provides a single function, :func:`is_prime`, which determines
whether a given integer is a prime number.

The function validates its input, raising ``ValueError`` for non‑positive
integers or non‑integer types.
"""

from __future__ import annotations

import math
from typing import Any

__all__ = ["is_prime"]


def is_prime(n: Any) -> bool:
    """
    Determine whether *n* is a prime number.

    Parameters
    ----------
    n : Any
        The number to test. It must be a positive integer.

    Returns
    -------
    bool
        ``True`` if *n* is prime, ``False`` otherwise.

    Raises
    ------
    ValueError
        If *n* is not a positive integer.
    """
    # Input validation
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n <= 0:
        raise ValueError("Input must be a positive integer (greater than 0).")

    # 1 is not prime
    if n == 1:
        return False
    # 2 is the only even prime
    if n == 2:
        return True
    # Exclude even numbers greater than 2
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    limit = math.isqrt(n)
    for divisor in range(3, limit + 1, 2):
        if n % divisor == 0:
            return False
    return True 
