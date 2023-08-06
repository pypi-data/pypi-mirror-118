"""
description: this module provides decorator teststep.
"""

import functools
import inspect

from _pistar.utilities.constants import TESTCASE_EXECUTION_STATUS
from _pistar.utilities.exceptions import DuplicatedTestStepNameException
from _pistar.utilities.exceptions import UnsupportParameterTypeException
from _pistar.utilities.exceptions import UnsupportStartTypeException
from .thread_status import Status
from .timeout import Timeout


def is_teststep(function):
    """
    description: this function is used to check whether a function is teststep.
    arguments:
        function:
            type: any
            assertion: callable
    return:
        type: bool
        description: if the function is a teststep, return True,
                     else return False.
    """
    return hasattr(function, 'start') \
           and hasattr(function, 'end') \
           and callable(function)


def teststep(
        test_function=None,
        *,
        start=None, skip=None, mark=None, timeout=None, parameters=None
):
    """
    description: decorate of teststep, parse actual teststep arguments
                 and run the step
    arguments:
        start:
            description: indicate teststep when to run
            type: str
            default: None
        skip:
            description: set the teststep not to run
            type: bool
        mark:
            description: set mark to teststep,  specific mark step
    return:
        type: TestStep
        description: actual step function results
    """
    teststep_obj = TestStep(start=start, skip=skip, mark=mark, timeout=timeout,
                            parameters=parameters)
    if test_function:
        return teststep_obj(test_function)

    return teststep_obj


class TestStep:
    """
    description: teststep decorate class, generate schedule strategy based on
                 testcase class
    attribute:
        start:
            description: indicate teststep when to run
            type: str
            default: None
        skip:
            description: set the teststep not to run
            type: bool
        mark:
            description: set mark to teststep,  specific mark step
    """
    start = None
    skip = None
    mark = None
    parameters = None

    __status_dictionary = {
        key: value
        for key, value in TESTCASE_EXECUTION_STATUS.__dict__.items()
        if not key.startswith('__')
    }
    __teststep_list = None

    def __get_previous_teststep(self):
        caller_frame = inspect.currentframe()
        while True:
            if not caller_frame.f_code.co_filename == __file__:
                break
            caller_frame = caller_frame.f_back

        member_name_list = list(caller_frame.f_locals.keys())
        for member_name in member_name_list[::-1]:
            last_member = caller_frame.f_locals[member_name]

            if is_teststep(last_member):
                self.__teststep_list.append(last_member)

        if self.__teststep_list:
            return self.__teststep_list[0]
        return None

    def __init__(
            self, start=None, skip=None, mark=None, timeout=None,
            parameters=None
    ):
        self.skip = skip
        self.mark = mark
        self.timeout = timeout
        self.__teststep_list = list()

        previous_teststep = self.__get_previous_teststep()
        if start is None:
            if previous_teststep:
                self.start = previous_teststep.end
            else:
                self.start = Status(True)
        elif not isinstance(start, Status):
            raise UnsupportStartTypeException(start)
        else:
            self.start = start

        if isinstance(parameters, dict):
            self.parameters = list()
            for item in zip(*parameters.values()):
                self.parameters.append(dict(zip(parameters.keys(), item)))
        elif isinstance(parameters, list):
            self.parameters = parameters
        else:
            self.parameters = parameters
        self.parameters = self.parameters if self.parameters else [()]

    def __execute(self, function, testcase, **kwargs):
        for parameter in self.parameters:
            if isinstance(parameter, tuple):
                function(testcase, *parameter, **kwargs)
            elif isinstance(parameter, dict):
                function(testcase, **parameter, **kwargs)
            else:
                raise UnsupportParameterTypeException(parameter=parameter)

    def __call__(self, function, **kwargs):
        if function.__name__ in [
            item.__name__ for item in self.__teststep_list
        ]:
            raise DuplicatedTestStepNameException(function.__name__)
        function = Timeout(self.timeout)(function)

        @functools.wraps(function, **kwargs)
        def wrapper(*args, **kwargs):
            testcase = args[0]
            function.__globals__.update(**self.__status_dictionary)

            if self.skip:
                # if skip is not False, do not execute the function.
                pass
            elif not self.mark:
                # if self.mark is None, execute the function.
                self.__execute(function, testcase, **kwargs)
            elif not wrapper.marks:
                # if marks is None, execute the function.
                self.__execute(function, testcase, **kwargs)
            elif self.mark not in wrapper.marks:
                # if mark is not in marks, do not execute the function.
                pass
            else:
                # else, execute the function.
                self.__execute(function, testcase, **kwargs)

            wrapper.end.value = True

        wrapper.start = self.start
        wrapper.end = Status(False)
        wrapper.marks = list()
        wrapper.parameters = self.parameters
        return wrapper
