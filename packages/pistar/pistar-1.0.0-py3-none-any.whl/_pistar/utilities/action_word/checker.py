"""
description: this module provides class ActionWordChecker.
"""

import ast
import inspect
import yaml
import astunparse

from _pistar.utilities.constants import ACTION_WORD_KEYS as KEYS
from _pistar.utilities.constants import ACTION_WORD_STATUS as STATUS
from _pistar.utilities.exceptions import DeprecatedActionWordException
from _pistar.utilities.exceptions import DisabledActionWordException
# action word static exceptions.
from _pistar.utilities.exceptions import MissingArgumentSchemaException
# action word dynamic exceptions.
# their names must be same with exceptions in
# utilities.match_schema.exceptions.
from _pistar.utilities.exceptions import MissingDocumentException
from _pistar.utilities.exceptions import MissingFieldInActionWordException
from _pistar.utilities.exceptions import MissingReturnSchemaException
from _pistar.utilities.exceptions import UnknownStatusException
from _pistar.utilities.match_schema import instantiate_assertion
from _pistar.utilities.match_schema import match_schema


class ActionWordChecker:
    """
    description: this class is used to check the action word.
    """

    __document = None
    __action_word = None
    __logger = None

    __argument_list = None
    __parse_arguments = None

    def __init__(self, action_word):
        """
        description: this is the constructor of the class ActionWordChecker.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
            action_word:
                type: function
                description: the action word
        return: None
        """

        if action_word.__doc__ is None:
            raise MissingDocumentException(
                action_word_name=action_word.__name__
            )

        self.__document = yaml.load(
            action_word.__doc__,
            Loader=yaml.SafeLoader
        )

        self.__document = self.__document if self.__document is not None \
            else dict()
        self.__action_word = action_word

        specification = inspect.getfullargspec(action_word)
        self.__argument_list = specification.args.copy()
        if specification.varargs:
            self.__argument_list.append(specification.varargs)
        if specification.varkw:
            self.__argument_list.append(specification.varkw)
        if specification.kwonlyargs:
            self.__argument_list += specification.kwonlyargs

        source_code = inspect.getsource(action_word).split('\n')
        first_line = source_code[0]
        indent = len(first_line) - len(first_line.lstrip())
        source_code = '\n'.join([line[indent:] for line in source_code])

        tree = ast.parse(source_code)
        arguments = astunparse.unparse(tree.body[0].args).strip()
        self.__parse_arguments = eval(
            'lambda {arguments}: locals()'.format(
                arguments=arguments
            )
        )

    def check_fields(self):
        """
        description: this function is used to check the field of action word
                     docstring.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
        return:
            type:
                - MissingFieldInActionWordException
                - None
            description: if there is no missing field, return None,
                         else return MissingFieldInActionWordException.
        """

        required_fields = [
            KEYS.DESCRIPTION,
            KEYS.ARGUMENTS,
            KEYS.RETURN,
            KEYS.AUTHOR,
            KEYS.MODIFY_RECORDS,
            KEYS.STATUS
        ]

        for field_name in required_fields:
            if field_name in self.__document:
                continue
            return MissingFieldInActionWordException(
                field_name=field_name,
                action_word_name=self.__action_word.__name__
            )
        return None

    def check_status(self):
        """
        description: this function is used to check the status of action word.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
        return:
            type:
                - DisabledActionWordException
                - DeprecatedActionWordException
                - UnknownStatusException
                - None
            description: |
                if there is no missing field, return None,
                else return DisabledActionWordException,
                DeprecatedActionWordException, or UnknownStatusException.
        """

        status = self.__document[KEYS.STATUS]

        if status == STATUS.DISABLE:
            return DisabledActionWordException(
                action_word_name=self.__action_word.__name__
            )

        if status == STATUS.DEPRECATED:
            return DeprecatedActionWordException(
                action_word_name=self.__action_word.__name__
            )

        if status == STATUS.ENABLE:
            return None

        return UnknownStatusException(
            status=status,
            action_word_name=self.__action_word.__name__
        )

    def check_argument_schemata(self):
        """
        description: this function is used to
                     check the argument schemata of action word.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
        return:
            type:
                - MissingArgumentSchemaException
                - None
            description: |
                if there is no missing schema, return None,
                else return MissingArgumentSchemaException.
        """

        for argument_name in self.__argument_list:
            if isinstance(self.__document[KEYS.ARGUMENTS], dict) and \
                    argument_name in self.__document[KEYS.ARGUMENTS]:
                continue

            return MissingArgumentSchemaException(
                argument_name=argument_name,
                action_word_name=self.__action_word.__name__
            )
        return None

    def check_return_schema(self):
        """
        description: this function is used to
                     check the return schema of action word.
        argument:
            self:
                type: ActionWordChecker
                description: itself
        return:
            type:
                - MissingReturnSchemaException
                - None
            description: |
                if there is schema of return, return None,
                else return MissingReturnSchemaException.
        """

        if isinstance(self.__document[KEYS.RETURN], dict):
            return None
        return MissingReturnSchemaException(
            action_word_name=self.__action_word.__name__
        )

    def check_arguments(self, *args, **kwargs):
        """
        description: this function is used to
                     check the argument value of action word.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
        return:
            type:
                - Exception
                - None
            description: |
                if there is any argument value that does not match its schema,
                 return Exception, elss return None.
        """

        # get the argument dictionary.
        try:
            argument_dictionary = self.__parse_arguments(*args, **kwargs)
        except BaseException as exception:
            return exception

        # for each argument
        for argument_name, argument_value in argument_dictionary.items():
            exception = match_schema(
                value=argument_value,
                schema=self.__document[KEYS.ARGUMENTS][argument_name],
                name=argument_name
            )
            if exception is not None:
                return self.format_exception(exception)

        return None

    def format_exception(self, exception):
        """
        description: this function is used to format the exception message.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
            exception:
                type: Exception
                description: the exception
        return:
            type:
                - TypeMismatchException
                - AssertionFailureException
                - EnumerationFailureException
                - MissingPropertyException
            description: the formatted exception.
        """

        # add message into the exception.
        exception.args = (
                             'in action word \'{action_word_name}\': '.format(
                                 action_word_name='.'.join(
                                     [self.__action_word.__module__,
                                      self.__action_word.__name__]
                                 )
                             ) + exception.args[0],
                         ) + exception.args[1:]

        return exception

    def check_return_value(self, return_value):
        """
        description: this function is used to
                     check whether return value does match the schema.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
            return_value:
                type: any
                description: the return value
        return:
            type:
                - Exception
                - None
            description: if the return value match its schema, return None,
                         else return Exception.
        """

        exception = match_schema(
            name=KEYS.RETURN,
            value=return_value,
            schema=self.__document[KEYS.RETURN]
        )

        if exception:
            return self.format_exception(exception)
        return None

    def instantiate_assertions(self):
        """
        description: this function is used to
                     instantiate the assertions in action word docstring.
        arguments:
            self:
                type: ActionWordChecker
                description: itself
        return: None
        """

        if self.__document[KEYS.ARGUMENTS]:
            for argument_name in self.__document[KEYS.ARGUMENTS]:
                self.__document[KEYS.ARGUMENTS][argument_name] = \
                    instantiate_assertion(
                        self.__document[KEYS.ARGUMENTS][argument_name]
                    )

        self.__document[KEYS.RETURN] = instantiate_assertion(
            self.__document[KEYS.RETURN]
        )
