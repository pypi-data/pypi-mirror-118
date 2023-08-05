"""Simple utilities for calculating averages"""

from __future__ import division

__version__ = '3.0.0'


def _optional_int(value):
    """Converts a ``float`` to an ``int`` if they're the same value

    Args:
        value (float)

    Returns:
        Either the original input or the input as an ``int``

    Example:
        >>> _optional_int(3.0)
        3

        >>> _optional_int(1.2)
        1.2
    """

    if value == int(value):
        return int(value)

    return value


def average(*values):
    """Calculates an unweighted average

    Args:
        values: The values to find the average of

    Returns:
        The average of the inputs

    Example:
        >>> average(1, 2, 3)
        2
    """

    res = sum(values) / len(values)

    return _optional_int(res)


def weighted_average(*values):
    """Calculates an weighted average

    Args:
        values: The values to find the average as an iterable of
            ``(value, weight)`` pairs

    Returns:
        The weighted average of the inputs

    Example:
        >>> weighted_average((1, 2), (2, 3))
        1.6
    """

    dividend, divisor = 0, 0

    for value, weight in values:
        if weight < 0:
            raise ValueError('Weights cannot be less than zero')

        dividend += value * weight
        divisor += weight

    res = dividend / divisor

    return _optional_int(res)


def median(*values):
    """Calculates the median, or middle number

    Args:
        values: The values to find the median of

    Returns:
        The median of the inputs

    Examples:
        >>> median(1, 2, 3)
        2

        >>> median(1, 2, 3, 4)
        2.5
    """

    values = sorted(values)
    middle = len(values) // 2

    if len(values) % 2 == 0:
        return average(values[middle], values[middle - 1])

    return _optional_int(values[middle])


def mode(*values):
    """Calculates the mode, or most common value

    Args:
        values: The values to find the mode of

    Returns:
        The mode(s) of the inputs (returned as a set if more than one)

    Examples:
        >>> mode(1, 2, 2, 3)
        2

        >>> mode(1, 1, 2, 2)
        {1, 2}
    """

    counts = {}

    for value in values:
        counts[value] = counts.get(value, 0) + 1

    result = {k for k, v in counts.items() if v == max(counts.values())}

    if len(result) == 1:
        return result.pop()

    return result
