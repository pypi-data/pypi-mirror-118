#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
description: this module provides class BaseTestCase.
"""
import collections
import inspect
import os
import shutil

from _pistar.pistar_pytest.utils import sha256
from _pistar.pistar_pytest.utils import uuid4
from _pistar.resources.configuration import configuration
from _pistar.utilities.assertion import AssertThat
from _pistar.utilities.constants import LOGGING_LEVEL
from _pistar.utilities.constants import TESTCASE_EXECUTION_STATUS as STATUS
from _pistar.utilities.exceptions import BlockedException
from _pistar.utilities.exceptions import FailedException
from _pistar.utilities.exceptions import InvestigatedException
from _pistar.utilities.exceptions import PassedException
from _pistar.utilities.exceptions import UnavailableException
from _pistar.utilities.exceptions import UnexecutedException
from _pistar.utilities.logger import Logger
from .assert_that import assert_that as _assert_that
from .metaclass import MetaTestCase


class TeststepQueue(set):
    """
    this class is used to save the teststeps and pop avaliable teststeps.
    """

    def pop_teststeps(self):
        """
        description: this member functions is uses to
                     pop the avaliable teststeps.
        """
        teststeps = {teststep
                     for teststep in self
                     if teststep.start()}
        self.difference_update(teststeps)
        return teststeps


class BaseTestCase(
    metaclass=MetaTestCase
):
    """
    this class is the base class of testcase.
    """

    __execution_status = None
    __start_time = None
    __end_time = None
    __assertion_list = None
    __action_word_information = None
    __status_dictionary = None
    __globals = None
    __log_path = None
    __report_path = None

    testcase_result_path = None
    failure = None

    @classmethod
    def __initialize__(cls):
        """
        description: this is the constructor of the class BaseTestCase.
        """
        # initialize the logger
        cls.__assertion_list = list()
        cls.__action_word_information = collections.defaultdict(list)

        cls.__status_dictionary = {
            STATUS.PASSED: PassedException,
            STATUS.FAILED: FailedException,
            STATUS.BLOCKED: BlockedException,
            STATUS.INVESTIGATED: InvestigatedException,
            STATUS.UNAVAILABLE: UnavailableException,
            STATUS.UNEXECUTED: UnexecutedException
        }

        cls.user_logger = Logger(
            name=cls.__name__,
            level=getattr(
                LOGGING_LEVEL, configuration.loggers.user.level.upper()
            ),
            logger_format=configuration.loggers.user.format,
            output_path=cls.__log_path
        )

        cls.debug = cls.user_logger.debug
        cls.info = cls.user_logger.info
        cls.warning = cls.user_logger.warning
        cls.error = cls.user_logger.error
        cls.critical = cls.user_logger.critical

    @property
    def status(self):
        """
        description: user can fetch testcase status with this attribute.
        """
        return self.__execution_status

    @status.setter
    def status(self, value):
        """
        description: if user set this attribute, raise corresponding exception.
        """
        frame = inspect.currentframe()
        line_number = frame.f_back.f_lineno
        raise self.__status_dictionary[value](line_number)

    @property
    def logger_path(self):
        """
        description: this function is used to get logger_path.
        """
        return self.user_logger.output_path

    def setup(self):
        """
        description: this is the setup of testcase.
        """
        return

    def teardown(self):
        """
        description: this is the teardown of testcase.
        """
        return

    def assert_that(self, value) -> AssertThat:
        """
        description: this member function is used to make assertion.
        arguments:
            value:
                type: any
                description: the value to be asserted
        return:
            type: assert_that
            description: if assertion is passed, return itself,
                         if it is failed, raise exception
        """
        caller = inspect.getframeinfo(inspect.stack()[1][0])

        return _assert_that(
            value=value,
            testcase=self,
            file_name=caller.filename,
            line_number=caller.lineno
        )

    def append_assertion(self, file_name, line_number, value, assertion_list):
        """
        description: this function is used to add assertion information into
                     member variable __assertion_list.
        arguments:
            method:
                type: str
                description: the method name
            value:
                type: any
                description: the value need to be asserted
            line_number:
                type: int
                description: the line number of assertion expression
            args:
                type: tuple
                description: the parameters of assertion expression
            kwargs:
                type: dict
                description: the parameters of assertion expression
            exception:
                type: Exception
                description: the exception of assertion
        """
        self.__assertion_list.append(
            (file_name, line_number, value, assertion_list)
        )

    def append_action_word_execution_information(
            self, module_name, caller_name, action_word_name, time_consuming
    ):
        """
        description: this function is used to add action word information into
                     member variable __action_word_information.
        arguments:
            module_name:
                type: str
                description: the module name of the action word
            action_word_name:
                type: str
                description: the name of the action word
            time_consuming:
                type: float
                description: the time consuming of action word execution,
                             unit is second
        """
        self.__action_word_information['.'.join(
            [module_name, caller_name, action_word_name]
        )].append(time_consuming)

    @property
    def execution_status(self):
        """
        description: return the execution status of this testcase.
        """
        return self.__execution_status

    @property
    def assertions(self):
        """
        description: return the assertions of this testcase.
        """
        return self.__assertion_list

    @property
    def action_word_information(self):
        """
        description: return the action word information of this testcase.
        """
        return self.__action_word_information

    @classmethod
    def __parse_arguments__(cls, arguments):
        """
        description: this function is used to parse the command from console.
        """
        output_abspath = os.path.abspath(arguments.output)
        if not os.path.exists(output_abspath):
            os.makedirs(output_abspath)

        cls.testcase_result_path = os.path.join(
            output_abspath, sha256(inspect.getfile(cls)))
        if os.path.exists(cls.testcase_result_path):
            shutil.rmtree(cls.testcase_result_path)
        os.makedirs(cls.testcase_result_path)
        report_path = os.path.join(cls.testcase_result_path, uuid4() + '.html')
        logger_path = os.path.join(
            cls.testcase_result_path, uuid4() + '-attachment.log'
        )
        cls.__log_path = logger_path
        cls.__report_path = report_path
