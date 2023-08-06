import io
import json
import os
import shutil
from collections import OrderedDict

from six import text_type

from _pistar.pistar_pytest.models import ATTACHMENT_PATTERN
from _pistar.pistar_pytest.models import Attachment
from _pistar.pistar_pytest.models import AttachmentType
from _pistar.pistar_pytest.models import Executable
from _pistar.pistar_pytest.models import TestResult
from _pistar.pistar_pytest.utils import now, write_json
from _pistar.utilities.constants import ENCODE
from _pistar.utilities.constants import FILE_MODE


class Reporter:
    def __init__(self, report_dir):
        self._report_base = report_dir
        self._report_dir = report_dir
        self._items = OrderedDict()
        self._finished = list()

    def set_file_finished(self, finish):
        write_json(finish, self._report_dir, "finished.json")

    def update_file_output_path(self, folder_md5):
        self._report_dir = os.path.join(self._report_base, folder_md5)

        if os.path.exists(self._report_dir):
            shutil.rmtree(self._report_dir)
        os.makedirs(self._report_dir)

    def update_cur_file(self, cur_file):
        data = dict()
        data["cur_script"] = cur_file
        destination = os.path.join(self._report_base, "task_meta_info.json")
        with io.open(destination, mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    def _update_item(self, uuid, **kwargs):
        item = self._items[uuid] if uuid else self._items[next(reversed(self._items))]
        for key, value in kwargs.items():
            attribute = getattr(item, key)
            if isinstance(attribute, list):
                attribute.append(value)
            else:
                setattr(item, key, value)

    def schedule_test(self, uuid, test_case):
        self._items[uuid] = test_case

    def close_test(self, uuid):
        test_case = self._items.pop(uuid)
        self.report_item(test_case, uuid)

    def get_test(self, uuid):
        return self.get_item(uuid) if uuid else self.get_last_item(TestResult)

    def get_item(self, uuid: str):
        return self._items.get(uuid)

    def get_last_item(self, item_type=None):
        for _uuid in reversed(self._items):
            if item_type is None or isinstance(self._items[_uuid], item_type):
                return self._items.get(_uuid)

    def _last_executable(self):
        for _uuid in reversed(self._items):
            if isinstance(self._items[_uuid], Executable):
                return _uuid

    def start_before_fixture(self, uuid, fixture):
        self._items[uuid] = fixture

    def stop_before_fixture(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
        self._items.pop(uuid)

    def start_after_fixture(self, uuid, fixture):
        self._items[uuid] = fixture

    def stop_after_fixture(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
        fixture = self._items.pop(uuid)
        fixture.stop = now()

    def report_item(self, item, uuid):
        filename = item.file_pattern.format(prefix=uuid)
        write_json(item, self._report_dir, filename)

    def attach_data(self, uuid, body, name=None, attachment_type=None):
        file_name = self._attach(uuid, name=name, attachment_type=attachment_type)
        self.report_attached_data(body=body, file_name=file_name)

    def _attach(self, uuid, name=None, attachment_type=None):
        mime_type = attachment_type
        extension = "attach"

        if isinstance(attachment_type, AttachmentType):
            extension = attachment_type.extension
            mime_type = attachment_type.mime_type

        file_name = ATTACHMENT_PATTERN.format(prefix=uuid, ext=extension)
        file_abs_name = os.path.join(self._report_dir, file_name)
        attachment = Attachment(path=file_abs_name, name=name, type=mime_type)
        last_uuid = self._last_executable()
        self._items[last_uuid].attachments.append(attachment)

        return file_name

    def report_attached_data(self, body, file_name):
        destination = os.path.join(self._report_dir, file_name)
        with open(destination, mode=FILE_MODE.BINARY_WRITE) as attached_file:
            if isinstance(body, text_type):
                attached_file.write(body.encode(ENCODE.UTF8))
            else:
                attached_file.write(body)
