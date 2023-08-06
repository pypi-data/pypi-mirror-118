"""
this is the set of exceptions of action word.
"""


class ActionWordException(Exception):
    """
    description: this is the base class action word exception.
    """


class MissingPropertyException(Exception):
    """
    description: if any properties are missing in action word docstring,
                 raise this exception.
    """

    def __init__(self, property_name, value_name):
        message = 'cannot find property \'{property_name}\' in' \
                  ' \'{value_name}\''.format(
                      property_name=property_name,
                      value_name=value_name
                  )
        super().__init__(message)


class TypeMismatchException(Exception):
    """
    description: if the argument's type does not match the docstring,
                 raise this exception.
    """

    def __init__(self, name, value, expect_type):
        message = '{name} = {value}, but the type should be {expect_type}' \
            .format(
                name=name,
                value=repr(value),
                expect_type=expect_type
            )
        super().__init__(message)


class AssertionFailureException(Exception):
    """
    description: if the assertion of argument fails, raise this exception.
    """

    def __init__(self, name, value, assertion):
        message = '{name} = {value}, cannot pass the assertion ' \
                  '\'{assertion}\''.format(
                      name=name,
                      value=repr(value),
                      assertion=assertion
                  )
        super().__init__(message)


class EnumerationFailureException(Exception):
    """
    description: if the argument value is not in enumerate,
                 raise this exception.
    """

    def __init__(self, name, value, enumeration):
        message = '{name} = {value}, does not in enumeration {enumeration}'. \
            format(
                name=name,
                value=repr(value),
                enumeration=repr(enumeration)
            )
        super().__init__(message)


class MissingFieldInActionWordException(ActionWordException):
    """
    description: if the argument's type does not match the docstring,
                 raise this exception.
    """

    def __init__(self, field_name, action_word_name):
        message = 'cannot find field \'{field_name}\' in action word ' \
                  '\'{action_word_name}\''.format(
                      field_name=field_name,
                      action_word_name=action_word_name
                  )
        super().__init__(message)


class UnknownStatusException(ActionWordException):
    """
    description: if status of action word is not in enumeration,
                 raise this exception.
    """

    def __init__(self, status, action_word_name):
        message = 'unknown status \'{status}\' of the action word ' \
                  '\'{action_word_name}\''.format(
                      status=status, action_word_name=action_word_name
                  )
        super().__init__(message)


class DisabledActionWordException(ActionWordException):
    """
    description: if status of action word is disable, raise this exception.
    """

    def __init__(self, action_word_name):
        message = 'the action word \'{action_word_name}\' is disabled'.format(
            action_word_name=action_word_name
        )
        super().__init__(message)


class DeprecatedActionWordException(ActionWordException):
    """
    description: if status of action word is deprecated, raise this exception.
    """

    def __init__(self, action_word_name):
        message = 'the action word \'{action_word_name}\' is deprecated' \
            .format(action_word_name=action_word_name)
        super().__init__(message)


class MissingArgumentSchemaException(ActionWordException):
    """
    description: if schema of argument is missing, raise this exception.
    """

    def __init__(self, argument_name, action_word_name):
        message = 'cannot find schema of argument \'{argument_name}\' of' \
                  ' action word \'{action_word_name}\''.format(
                      argument_name=argument_name,
                      action_word_name=action_word_name
                  )
        super().__init__(message)


class MissingReturnSchemaException(ActionWordException):
    """
    description: if schema of return is missing, raise this exception.
    """

    def __init__(self, action_word_name):
        message = 'cannot find schema of return of action word ' \
                  '\'{action_word_name}\''.format(
                      action_word_name=action_word_name
                  )
        super().__init__(message)


class MissingDocumentException(Exception):
    """
    description: if __doc__ is None, raise this exception.
    """

    def __init__(self, action_word_name):
        message = 'action word {action_word_name} has no __doc__'.format(
            action_word_name=action_word_name)
        super().__init__(message)
