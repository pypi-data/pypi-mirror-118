"""
description: this module provides the function process_assert_that.
"""

import yaml

from _pistar.utilities.function_tools import object_to_string
from _pistar.utilities.assertion import AssertThat
from _pistar.utilities.exceptions import AssertionBaseException

from _pistar.utilities.exceptions import HasNoAttributeException
from _pistar.utilities.function_tools import keyword_arguments_to_list


def format_arguments(method, args, kwargs):
    """
    description: parse assert method arguments based on method.
    arguments:
        method:
            type: str
            description: assert method
        args:
            description: non-keyworded arguments, can be variable number
        kwargs:
            description: keyworded arguments, can be variable number
    """
    if method.__name__ == 'matches_schema':
        if args:
            return (yaml.load(args[0], Loader=yaml.SafeLoader), ), kwargs
        return args, {key: yaml.load(value, Loader=yaml.SafeLoader)
                      for key, value in kwargs.items()}
    return args, kwargs


def process_assert_that(origin_assert_that):
    """
    description: package assert_that class for base testcase
    arguments:
        origin_assert_that:
            type: assert_that, class define in assertion
    """
    class AssertThat:
        """
        description: new assert_that class for testcase
        attribute:
            value:
                type: same type of asserted object
                description: value of object that will to assert
                permission: private
            testcase:
                type: testcase, derive from BaseTestcase
                description: actual testcase to test
                permission: public
            assertion_list:
                type: list
                description: list of assertions of one testcase
                permission: public
            file_name:
                type: str
                description: file name where the assertion make
                permission: public
            line_number:
                type: int
                description: line number where the assertion make
                permission: public
        """
        __value = None
        testcase = None
        assertion_list = None

        file_name = None
        line_number = None

        def get_value(self):
            '''
            description: this function is used to
                         get the private member variable __value.
            '''
            return self.__value

        def __init__(
            self, value, testcase=None, file_name=None, line_number=None
        ):
            self.__value = value
            self.testcase = testcase

            self.file_name = file_name
            self.line_number = line_number
            self.assertion_list = list()

        def __getattr__(self, attribute):
            raise HasNoAttributeException(
                class_name=self.__class__.__name__,
                attribute_name=attribute,
                file_path=self.file_name,
                line_number=self.line_number
            )

        def __del__(self):
            if self.assertion_list:
                self.testcase.append_assertion(
                    self.file_name,
                    self.line_number,
                    self.__value,
                    self.assertion_list
                )

    methods = {
        key: value
        for key,
        value in origin_assert_that.__dict__.items()
        if not key.startswith('_') and callable(value)
    }

    for method_name, method in methods.items():
        if not callable(method):
            continue

        if method_name.startswith('_'):
            continue

        def generate_method(method):
            """
            description: decorator of actual assert method
            arguments:
                method:
                    type: str
                    description: method name
            """
            def wrapper(self, *args, **kwargs):
                try:
                    method(self, *args, **kwargs)
                    # for report
                    args, kwargs = format_arguments(method, args, kwargs)

                    args = ', '.join([object_to_string(arg) for arg in args])
                    kwargs = ', '.join(keyword_arguments_to_list(kwargs))
                    arguments = args + ', ' + kwargs if kwargs else args
                    self.assertion_list.append(
                        dict(
                            value=self.get_value(),
                            line_number=self.line_number,
                            code='{method}({arguments})'.format(
                                method=method.__name__, arguments=arguments
                            ),
                            exception=None
                        )
                    )
                except AssertionBaseException as exception:
                    # for report
                    args, kwargs = format_arguments(method, args, kwargs)
                    args = ', '.join([object_to_string(arg) for arg in args])
                    kwargs = ', '.join(keyword_arguments_to_list(kwargs))
                    arguments = args + ', ' + kwargs if kwargs else args
                    self.assertion_list.append(
                        dict(
                            value=self.get_value(),
                            line_number=self.line_number,
                            code='{method}({arguments})'.format(
                                method=method.__name__, arguments=arguments
                            ),
                            exception=exception
                        )
                    )
                    self.testcase.append_assertion(
                        self.file_name,
                        self.line_number,
                        self.get_value(),
                        self.assertion_list
                    )
                    self.assertion_list = list()
                    raise exception
                except BaseException as exception:
                    raise exception

                return self

            return wrapper

        setattr(AssertThat, method_name, generate_method(method))
    return AssertThat


assert_that = process_assert_that(AssertThat)
