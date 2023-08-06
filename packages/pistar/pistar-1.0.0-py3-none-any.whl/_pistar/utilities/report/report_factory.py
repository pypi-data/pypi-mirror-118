import json
import os

from _pistar.utilities.condition.condition import ConditionManager
from _pistar.utilities.constants import ENCODE
from _pistar.utilities.constants import FILE_MODE
from _pistar.utilities.constants import \
    PISTAR_TESTCASE_EXECUTION_STATUS as PISTAR_STATUS
from _pistar.utilities.constants import REPORT_TYPE
from .pistar_report_info import PistarReportInfo


def get_report_info(testcase, con_manager: ConditionManager, report_type=REPORT_TYPE.PISTAR):
    """
    description: get report data by report_type
    parameter:
        report_type:
            description: the report_type
            type:str
    return:
        report
    """
    report_info = PistarReportInfo(testcase, con_manager)

    return report_info


def generate_report_file(testcase, report_info):
    output_path = testcase.testcase.testcase_result_path
    for teststep in report_info.get('details'):
        report_json_file = '.'.join([teststep.get('uuid') + '-result', 'json'])
        with open(os.path.join(output_path, report_json_file),
                  mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
            file.write(json.dumps(
                teststep, ensure_ascii=False, indent=4, default=str
            )
            )

    finish_data = dict()
    finish_data['start_time'] = testcase.start_time
    finish_data['end_time'] = testcase.end_time
    finish_data['duration'] = testcase.end_time - testcase.start_time
    finish_data['result'] = PISTAR_STATUS.PASSED \
        if testcase.execution_status == '0' else PISTAR_STATUS.FAILED

    with open(os.path.join(output_path, 'finished.json'),
              mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
        file.write(json.dumps(
            finish_data, ensure_ascii=False, indent=4, default=str
        )
        )
