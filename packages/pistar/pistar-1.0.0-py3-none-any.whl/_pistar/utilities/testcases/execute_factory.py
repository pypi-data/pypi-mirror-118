import inspect
import json
import os

from _pistar.utilities.constants import ENCODE
from _pistar.utilities.constants import FILE_MODE
from _pistar.utilities.constants import \
    PISTAR_TESTCASE_EXECUTION_STATUS as PISTAR_STATUS
from _pistar.utilities.constants import REPORT_TYPE
from _pistar.utilities.function_tools import trace_exception
from _pistar.utilities.report import generate_report_file
from _pistar.utilities.report import get_report_info
from _pistar.utilities.testcases.case import TestCase
from _pistar.utilities.testcases.collector import Collector
from .console_output import console_testcase_end
from .console_output import console_testcase_start


def generate_start_file(testcase_path, output_dir):
    start_data = dict()
    start_data['cur_script'] = testcase_path

    with open(os.path.join(output_dir, 'task_meta_info.json'),
              mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
        file.write(json.dumps(
            start_data, ensure_ascii=False, indent=4, default=str))


class ExecuteFactory:
    def __init__(self, collect: Collector):
        self.testcases = collect.testcases
        self.condition_manager = collect.condition_manager

    def execute(self, arguments):
        results = dict()
        for testcase in self.testcases:
            console_testcase_start(testcase)
            generate_start_file(inspect.getfile(testcase), arguments.output)
            case = TestCase(testcase, arguments)
            try:
                case.initialize_step()
            except BaseException as _exception:
                case.logger.error(trace_exception(_exception))
            else:
                case.execute(self.condition_manager)
            finally:
                if testcase is self.testcases[-1]:
                    finish_condition = self.condition_manager.finish()
                    last_step = list(case.execute_records.keys())[-1]
                    case.execute_records.get(last_step)['after'] = \
                        finish_condition

                report_info = get_report_info(case, self.condition_manager,
                                              REPORT_TYPE.SINGLE)
                generate_report_file(case, report_info)
                results["::".join([case.path, case.testcase_class.__name__])] = PISTAR_STATUS.PASSED \
                    if case.execution_status == '0' else PISTAR_STATUS.FAILED
                console_testcase_end(testcase)

        return results
