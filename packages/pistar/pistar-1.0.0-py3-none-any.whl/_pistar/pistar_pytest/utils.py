# -*- coding: utf-8 -*-
import hashlib
import io
import json
import os
import time
import traceback
import uuid
from itertools import chain
from itertools import islice
import six
from attr import asdict
import pytest

from _pistar.pistar_pytest.models import Exceptions
from _pistar.pistar_pytest.models import LabelType
from _pistar.pistar_pytest.models import Status
from _pistar.utilities.constants import ENCODE
from _pistar.utilities.constants import FILE_MODE


def now() -> int:
    """
    Get current UNIX timestamp(ms).
    """
    return int(round(1000 * time.time()))


def uuid4() -> str:
    """
    Generate an uuid4 string.
    """
    return str(uuid.uuid4())


def sha256(*args) -> str:
    """
    Generate a sha256 string from an obj list
    This function is also used to generate
    a fixed folder name from an file case's
    absolute path.
    :return: sha256 string
    """
    m = hashlib.sha256()
    for arg in args:
        part = arg.encode("utf-8")
        m.update(part)
    return m.hexdigest()


def suite_labels(item):
    """
    Get suite for a pytest case.

    A pytest case may have three suite:
    parent_suite,suite,sub_suite(possibly).

    Parent_suite is the package name.
    Suite is the module(or file) name.
    Sub_suite is the class name(if exists).
    """
    head, possibly_clazz, tail = islice(chain(item.nodeid.split("::"), [None], [None]), 3)
    clazz = possibly_clazz if tail else None
    file_name, path = islice(chain(reversed(head.rsplit("/", 1)), [None]), 2)
    module = file_name.split(".")[0]
    package = path.replace("/", ".") if path else None
    pairs = dict(zip([LabelType.PARENT_SUITE, LabelType.SUITE, LabelType.SUB_SUITE], [package, module, clazz]))
    default_suite_labels = []
    for label, value in pairs.items():
        if value:
            default_suite_labels.append((label, value))

    return default_suite_labels


def escape_non_unicode_symbols(item):
    if not (six.PY2 and isinstance(item, str)):
        return item

    def escape_symbol(s):
        try:
            s.decode(encoding=ENCODE.UTF8)
            return s
        except UnicodeDecodeError:
            return repr(s)[1:-1]

    return "".join(map(escape_symbol, item))


def get_description(item) -> str:
    """
    Get function document from a pytest Item,like Function or FixtureDef.

    :param item: A pytest Item
    :return: Function document if it exists.
    """
    if hasattr(item, "function"):
        return item.function.__doc__


def get_outcome_status(outcome):
    if outcome.excinfo:
        _, exc, _ = outcome.excinfo
    else:
        exc = None
    return get_status(exc)


def get_status_details(exception_type, exception, exception_traceback):
    message = escape_non_unicode_symbols(format_exception(exception_type, exception))
    trace = escape_non_unicode_symbols(format_traceback(exception_traceback))
    return Exceptions(title=message, detail=trace) if message or trace else None


def get_status(exception):
    if exception is None:
        return Status.PASSED
    if isinstance(exception, (AssertionError, pytest.fail.Exception)):
        return Status.FAILED
    if isinstance(exception, pytest.skip.Exception):
        return Status.SKIPPED
    return Status.BROKEN


def write_json(data, folder: str, file: str) -> None:
    """
    Write an object to a specific path.Ignore None type and empty
    list or dict.
    :param data: target object
    :param folder: specific folder.Insure it exists.
    :param file: specific file name.
    """
    json_data = asdict(data, filter=lambda attr, value: isinstance(value, (bool, int)) or bool(value))
    with io.open(os.path.join(folder, file), mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)


def format_traceback(exc_traceback):
    return "".join(traceback.format_tb(exc_traceback)) if exc_traceback else None


def format_exception(etype, value):
    return "\n".join(traceback.format_exception_only(etype, value)) if etype or value else None
