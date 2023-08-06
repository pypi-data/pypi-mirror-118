"""
description: |
    this module provides the class Configuration.
    the class Configuration can be initialized by file path or yaml string.
    you can access its attribute by __getattr__ or __getitem__.
"""

import yaml

from _pistar.utilities.constants import ENCODE
from _pistar.utilities.constants import FILE_MODE
from .exceptions import InvalidTypeException
from .exceptions import MissingKeyException
from .exceptions import SyntaxException


class Configuration(dict):
    """
    description: |
        this class is used to load and modify the configuration file.
        you can used __getattr__ and __getitem__ to access its attributes.
    """

    def __init__(self, file_path=None, content=None):
        """
        description: this is the constructor.
        """

        super().__init__()

        if file_path is not None:
            with open(file_path, FILE_MODE.READ, encoding=ENCODE.UTF8) \
                    as file:
                content = yaml.load(file.read(), Loader=yaml.SafeLoader)

        content = content if content else dict()

        for key, value in content.items():
            if isinstance(value, dict):
                self[key] = Configuration(content=value)
            else:
                self[key] = value

    def __getattr__(self, key):
        """
        description: |
            override the member function __getattr__.
            if access a nonexist attribute, return None.
        """

        return None

    def __setitem__(self, key, value):
        """
        description: |
            override the member function __getitem__.
            call __setattr__ and __setitem__.
        """
        super().__setattr__(key, value)
        super().__setitem__(key, value)

    def __setattr__(self, key, value):
        """
        description: override the member function __setattr__.
        """

        self[key] = value

    def get_value(self, keys):
        """
        description: this function is used to get attribute with keys,
                     such as loggers.user.debug.
        arguments:
            keys:
                type: str
                description: the keys splitted with dot.
        return:
            type: any
        """

        iterator = self
        for key in keys.split('.'):
            if key not in iterator:
                raise MissingKeyException(key=keys)
            iterator = iterator[key]

        if not isinstance(iterator, str):
            raise InvalidTypeException(type(iterator))

        return iterator

    def set_value(self, expression):
        """
        description: this function is used to set attribute with keys,
                     such as loggers.user.level=debug.
        arguments:
            expression:
                type: str
                description: the assignment expression with format keys=value.
        """

        if '=' not in expression:
            raise SyntaxException(expression=expression)

        keys, value = expression.split('=', 1)
        iterator = self

        for index, key in enumerate(keys.split('.')):
            if key not in iterator:
                raise MissingKeyException(key=keys)

            if index < keys.count('.'):
                iterator = iterator[key]
            else:
                iterator[key] = value

    def save(self, file_path):
        """
        description: this function is used to
                     save this configuration to the file.
        arguments:
            file_path:
                type: str
                description: the output file path.
        """

        with open(file_path, FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
            file.write(yaml.dump(self.__dict__))

    def to_dictionary(self):
        """
        description: this function is used to
                     convert the configuration to dictionary.
        """

        return {
            key: value.to_dictionary()
            if isinstance(value, Configuration)
            else value for key, value in self.items()
        }
