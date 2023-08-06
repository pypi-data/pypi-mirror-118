"""
description: this module provides the function keyword_arguments_to_list.
"""

from .object_to_string import object_to_string


def keyword_arguments_to_list(kwargs):
    """
    description: this function is used to convert key value dictionary to
                 list with item format key=value.
    """

    return [
        '{key}={value}'.format(
            key=key,
            value=object_to_string(value)
        ) for key, value in kwargs.items()
    ]
