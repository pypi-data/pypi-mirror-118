"""
description: this module provides the class Timeout.
"""

import threading
import functools


class TimeoutException(Exception):
    """
    description: if a function is timeout, raise this exception.
    """
    def __init__(self, function_name, timeout):
        super().__init__(
            'teststep \'{function_name}\' is terminated due to'
            ' timeout {timeout} seconds'
            .format(function_name=function_name, timeout=timeout)
        )


class Timeout:
    """
    description: this class is used to wrap a function with timeout limit.
    """
    timeout = None

    def __init__(self, timeout=None):
        self.timeout = timeout

    def __call__(self, function):
        if self.timeout is None:
            return function

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            results = [
                TimeoutException(
                    function_name=function.__name__, timeout=self.timeout
                )
            ]

            def thread_function():
                try:
                    results[0] = function(*args, **kwargs)
                except BaseException \
                        as exception:
                    results[0] = exception

            thread = threading.Thread(target=thread_function)
            thread.daemon = True

            thread.start()
            thread.join(self.timeout)

            if isinstance(results[0], Exception):
                raise results[0]

            return results[0]

        return wrapper
