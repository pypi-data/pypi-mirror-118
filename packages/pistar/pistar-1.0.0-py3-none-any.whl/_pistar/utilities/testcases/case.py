import inspect
import os
import queue
import threading
from typing import Callable, Dict

from attr import attrs, attrib, Factory

from _pistar.pistar_pytest.utils import now
from _pistar.utilities.condition.condition import ConditionManager
from _pistar.utilities.constants import (
    LOGGING_LEVEL,
    TESTCASE_EXECUTION_STATUS as STATUS,
)
from _pistar.utilities.exceptions import (
    PassedException,
    FailedException,
    InvestigatedException,
    UnavailableException,
    BlockedException,
    UnexecutedException,
    TestCaseStatusException,
)
from _pistar.utilities.logger.logger import ExecuteLogger
from _pistar.utilities.messages import call_begin, call_successfully, call_failed
from _pistar.utilities.testcase.base import TeststepQueue
from _pistar.utilities.testcase.decorators import is_teststep
from _pistar.utilities.testcases.exception import ExceptionInfo, ExcInfoFormatter


@attrs
class TestCaseStepRecord:
    condition_result_cache = attrib(type=dict, default=Factory(dict))
    start_time = attrib(type=int, default=None)
    end_time = attrib(type=int, default=None)
    status_code = attrib(type=str, default=None)
    exception = attrib(type=dict, default=Factory(dict))


class TestCase:
    """A Class responsible for setting up and executing a pistar test case.

    param case_obj:
        The origin pistar test case derived from BaseTestCase.
    param arguments:
        The console parameter.
    """

    _start_time = None
    _end_time = None
    __execution_status = None

    execute_records = dict()
    exceptions = list()

    @property
    def end_time(self):
        return self._end_time

    @property
    def testcase_class(self):
        return self.__testcase_class

    @property
    def execution_status(self):
        return self.__execution_status

    @property
    def path(self) -> str:
        """case file absolute path."""
        return inspect.getfile(self.testcase_class)

    @property
    def document(self) -> str:
        return self.testcase_class.__document__

    @property
    def start_time(self):
        return self._start_time

    def debug(self, message):
        if getattr(self, "logger", None):
            self.logger.debug(message)

    def info(self, message):
        if getattr(self, "logger", None):
            self.logger.info(message)

    def warning(self, message):
        if getattr(self, "logger", None):
            self.logger.warning(message)

    def error(self, message):
        if getattr(self, "logger", None):
            self.logger.error(message)

    def critical(self, message):
        if getattr(self, "logger", None):
            self.logger.critical(message)

    def __init__(self, case_obj, arguments):
        self.execute_records = dict()
        self.exceptions = list()

        if arguments.debug:
            self.__logger_path = os.path.join(os.getcwd(), "logs", "pistar.log")
            self.logger = ExecuteLogger(
                name=case_obj.__name__,
                level=LOGGING_LEVEL.DEBUG,
                logger_format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                output_path=self.__logger_path,
            )
        case_obj.__parse_arguments__(arguments)

        case_obj.__initialize__()

        self.__testcase_class = case_obj

    def initialize_step(self):
        try:
            self.testcase = self.__testcase_class()
        except BaseException as _exception:
            self.exceptions.append(_exception)
            raise _exception

        self.setup = self.testcase.setup
        self.teardown = self.testcase.teardown
        self.failure = self.testcase.failure

        self.__schedule_step()

    def _log_for_exceptions(
            self,
            _exception: BaseException,
            dependence: Callable,
            pure_traceback_exception: Dict[str, str],
    ) -> None:
        """
        description: Used to output complete exception information and
        pure script exception information to framework log
        """
        self.testcase.error(
            f'exception: {pure_traceback_exception["title"]}\n'
            f'{pure_traceback_exception["detail"]}'
        )
        self.debug(call_failed(dependence.__name__, _exception))

    @staticmethod
    def _format_exception_by_pure_traceback(dependence: Callable) -> Dict[str, str]:
        """
        description: Format the complete exception information to get the
        pure exception information on the script side
        """
        exc_info = ExceptionInfo.from_current()
        fmt = ExcInfoFormatter(exc_info=exc_info, func=dependence)
        fmt.pure_traceback()
        exception_title = exc_info.exc_only()
        exception_detail = fmt.get_formatted_exc_info()
        exception = dict()
        exception["title"] = exception_title
        exception["detail"] = exception_detail
        return exception

    def __set_manual_status(self, exception):
        """
        description: when the result is manually specified by self.status
        in the test case script, the test case result is set according to the
        corresponding exception class

        :param exception: exception class corresponding to manual status
        :type exception: TestCaseStatusException
        """
        if isinstance(exception, PassedException):
            self.__execution_status = STATUS.PASSED
            self.info(exception)
        elif isinstance(exception, FailedException):
            self.__execution_status = STATUS.FAILED
            self.error(exception)
        elif isinstance(exception, InvestigatedException):
            self.__execution_status = STATUS.INVESTIGATED
            self.error(exception)
        elif isinstance(exception, UnavailableException):
            self.__execution_status = STATUS.UNAVAILABLE
            self.error(exception)
        elif isinstance(exception, BlockedException):
            self.__execution_status = STATUS.BLOCKED
            self.error(exception)
        elif isinstance(exception, UnexecutedException):
            self.__execution_status = STATUS.UNEXECUTED
            self.error(exception)

    def __schedule_step(self):
        teststep_queue = list()

        child = self.testcase.__class__
        for attribute_name in child.__dict__:
            if is_teststep(child.__dict__.get(attribute_name)):
                teststep_queue.append(getattr(self.testcase, attribute_name))

        self.teststep_queue = TeststepQueue(teststep_queue)

    def __run(self, dependence):
        start_time = now()
        try:
            self.debug(call_begin(dependence.__name__))
            dependence()
            self.debug(call_successfully(dependence.__name__))
        except PassedException as _exception:
            self.__set_manual_status(_exception)
            exception = _exception
            status_code = STATUS.PASSED
            self.debug(call_successfully(dependence.__name__))
        except TestCaseStatusException as _exception:
            self.__set_manual_status(_exception)
            exception = TestCase._format_exception_by_pure_traceback(dependence)
            status_code = self.__execution_status
            self._log_for_exceptions(_exception, dependence, exception)
        except BaseException as _exception:
            self.__execution_status = STATUS.FAILED
            exception = TestCase._format_exception_by_pure_traceback(dependence)
            status_code = self.__execution_status
            self._log_for_exceptions(_exception, dependence, exception)
        else:
            exception = None
            status_code = STATUS.PASSED
        end_time = now()
        if exception:
            self.exceptions.append(exception)

        self._set_execute_records(dependence,
                                  TestCaseStepRecord(start_time=start_time, end_time=end_time, status_code=status_code,
                                                     exception=exception))

        return exception

    def __get_thread(self, teststep, con_manager: ConditionManager):
        def teststep_thread():
            start_time = now()

            signature = inspect.signature(teststep)
            parameters = signature.parameters
            para_list = [item for item in parameters]
            self.debug(call_begin(teststep.__name__, para_list))
            condition_result = dict()
            condition_result_cache = dict()
            try:
                if not parameters:
                    teststep()
                else:
                    for parameter in parameters:
                        if parameter in con_manager.name2confunc:
                            result = con_manager.execute(parameter)
                            if result[1]:
                                condition_result[parameter] = None
                                raise result[1]
                            else:
                                condition_result[parameter] = result[0]
                                condition_result_cache[parameter] = result
                    teststep(**condition_result)
            except PassedException as _exception:
                exception = None
                self.__set_manual_status(_exception)
                status_code = STATUS.PASSED
                self.debug(call_successfully(teststep.__name__))
            except TestCaseStatusException as _exception:
                self.__set_manual_status(_exception)

                exception = TestCase._format_exception_by_pure_traceback(inspect.unwrap(teststep))
                status_code = self.__execution_status
                self._log_for_exceptions(_exception, teststep, exception)
            except BaseException as _exception:
                self.__execution_status = STATUS.FAILED

                exception = TestCase._format_exception_by_pure_traceback(inspect.unwrap(teststep))
                status_code = self.__execution_status
                self._log_for_exceptions(_exception, teststep, exception)
            else:
                status_code = STATUS.PASSED
                exception = None
                self.debug(call_successfully(teststep.__name__))
            end_time = now()
            if exception:
                self.exceptions.append(exception)

            self._set_execute_records(teststep, TestCaseStepRecord(condition_result_cache=condition_result_cache,
                                                                   start_time=start_time,
                                                                   end_time=end_time, status_code=status_code,
                                                                   exception=exception))
            self.__queue.put(exception)

        return teststep_thread

    def _set_execute_records(self, step: Callable, tc_step_record: TestCaseStepRecord):
        """
        description: Set the execution result for each step
        :param step: setup,teardown,failure or test step
        :type step: Callable
        :param tc_step_record: record for one step
        :type tc_step_record: TestCaseStepRecord
        :return: None
        """
        self.execute_records[step.__name__] = {
            "before": tc_step_record.condition_result_cache,
            "start_time": tc_step_record.start_time,
            "end_time": tc_step_record.end_time,
            "status_code": tc_step_record.status_code,
            "exception": tc_step_record.exception,
        }

    def execute(self, con_management: ConditionManager):
        self._start_time = now()

        self.__queue = queue.Queue()

        self.__execution_status = STATUS.BLOCKED

        threads_pools = list()
        exception = self.__run(self.setup)
        if isinstance(exception, PassedException):
            self.__run(self.teardown)
        elif exception:
            self.__run(self.failure)
        else:
            for _ in range(len(self.teststep_queue)):
                teststeps = self.teststep_queue.pop_teststeps()
                for teststep in teststeps:
                    thread = threading.Thread(
                        target=self.__get_thread(teststep, con_management)
                    )
                    threads_pools.append(thread)
                    thread.start()

                exception = self.__queue.get()
                if exception:
                    break
            else:
                exception = None

            if exception and not isinstance(exception, PassedException):
                self.__run(self.failure)
            else:
                self.__execution_status = STATUS.PASSED
                self.__run(self.teardown)
        self._end_time = now()
