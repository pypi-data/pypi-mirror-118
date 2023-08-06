"""
description: this module provides the function trace_error.
"""

import traceback


def trace_exception(exception):
    """
    description: this function is used to convert exception to string.
    arguments:
        exception:
            type: BaseException
            description: the exception.
    """
    return '{type}: {text}\n  traceback:\n{stack}'.format(
        type='.'.join(
            [exception.__class__.__module__, exception.__class__.__name__]),
        text=str(exception),
        stack='\n'.join(
            [
                '  - {file_path}:{line_number}\n  {code}'.format(
                    file_path=item.filename,
                    line_number=item.lineno,
                    code=item.line
                ) for item in
                traceback.TracebackException.from_exception(exception).stack
            ]
        )
    )
