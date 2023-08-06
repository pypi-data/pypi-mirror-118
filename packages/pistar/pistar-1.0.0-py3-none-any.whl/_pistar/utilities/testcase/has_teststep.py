"""
description: this module provides function has_teststep.
"""


def has_teststep(cls):
    """
    description: this function is used to
                 check whether a testcase has teststep.
    arguments:
        Class:
            type: type
    return:
        type: bool
    """

    for member in cls.__dict__.values():
        if hasattr(member, 'start') and hasattr(member, 'end'):
            return True
    return False
