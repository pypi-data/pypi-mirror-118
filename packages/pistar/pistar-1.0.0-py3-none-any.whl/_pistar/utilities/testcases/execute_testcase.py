import os
from pathlib import Path
from typing import List, Dict

from _pistar.pistar_pytest.utils import now
from _pistar.utilities.pytest import execute_pytest_testcases
from _pistar.utilities.testcases.collector import Collector, UsageError
from _pistar.utilities.testcases.execute_factory import ExecuteFactory
from .console_output import console_output
from .console_output import console_summary_collection


class TESTCASE_TYPE:
    PISTAR = "pistar"
    PYTEST = "pytest"


def init_output_dir(output_directory):
    output_abspath = os.path.realpath(output_directory)
    if not os.path.exists(output_abspath):
        os.makedirs(output_abspath)


def legal_check(paths: List[str]) -> List[Path]:
    """
    Check path arguments and return List[Path].

    Command-line arguments can point to files or ONLY ONE directory, for example:

      "pkg/tests/test_foo.py pkg/tests/test_bar.py"

    or one directory:

      "pkg/tests/"

    This function ensures the path exists, and returns a List:

        (List[Path("/full/path/to/pkg/tests/test_foo.py")]

    If the path doesn't exist, raise UsageError.

    """
    assert len(paths) > 0
    absolute_paths: List[Path] = list()

    for it in paths:
        path = Path(it)
        if path.is_dir() and len(paths) > 1:
            msg = "pistar only support one directory argument"
            raise UsageError(msg)
        if not path.exists():
            msg = f"file or directory not found: {path}"
            raise UsageError(msg)
        absolute_paths.append(path.absolute())
    return absolute_paths


def group_by_folder(paths: List[Path]) -> Dict[str, List[Path]]:
    """
    Group test case by its parent path.

    In pistar,The cases which have same parent path
    have same scope.They will be collected by the
    same Collector.

    Nothing to do if path is a directory.
    """

    path_grouped_by = dict()
    for it in paths:
        path = Path(it)
        abs_path = path.absolute()
        parent = str(abs_path.parent) if abs_path.is_file() else str(abs_path)

        if parent not in path_grouped_by:
            path_grouped_by[parent] = list()

        path_grouped_by[parent].append(abs_path)
    return path_grouped_by


def execute(arguments):
    """
    description: the function is the entry of running testcases
    """
    start_time = now()
    init_output_dir(arguments.output)
    if arguments.type == TESTCASE_TYPE.PISTAR:

        collectors = pistar_collection(arguments.files_or_dir)

        all_case_results = dict()

        for collect in collectors:
            run_loop = ExecuteFactory(collect)
            all_case_results.update(run_loop.execute(arguments))

        console_summary_collection(all_case_results, now() - start_time)
    elif arguments.type == TESTCASE_TYPE.PYTEST:
        execute_pytest_testcases(arguments)


def pistar_collection(args: List[str]) -> List[Collector]:
    """
    Perform the collection phase for the given session.
    """

    resolved_path = legal_check(args)
    group_by_cases = group_by_folder(resolved_path)
    collectors: List[Collector] = []
    testcase_num = 0
    console_output("collecting...")
    for path in group_by_cases:
        collect = Collector(Path(path), group_by_cases.get(path))
        collectors.append(collect)
        testcase_num += len(collect.testcases)
    if testcase_num == 1:
        info = "collected 1 test case\n"
    else:
        info = f"collected {testcase_num} test cases\n"
    console_output(info)
    return collectors
