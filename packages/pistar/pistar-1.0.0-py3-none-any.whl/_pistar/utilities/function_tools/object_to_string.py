"""
description: this module provides the function object_to_string.
"""


def object_to_string(instance):
    """
    description: this function is used to get the object string represent.
    """

    if isinstance(instance, type):
        return instance.__name__
    return repr(instance)
