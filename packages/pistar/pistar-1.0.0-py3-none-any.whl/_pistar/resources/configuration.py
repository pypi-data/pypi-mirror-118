import os
import yaml

from _pistar.utilities.constants.encode import ENCODE
from _pistar.utilities.constants.file_mode import FILE_MODE

from _pistar.utilities.function_tools import update_dict
from _pistar.utilities.configuration import Configuration

from _pistar.utilities.constants import ROOT_CONFIGURATION_PATH
from _pistar.utilities.match_schema import match_schema


CONFIGURATION_SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'utilities',
    'schemata',
    'configuration.yaml'
)

with open(
    CONFIGURATION_SCHEMA_PATH, mode=FILE_MODE.READ, encoding=ENCODE.UTF8
) as file:
    CONFIGURATION_SCHEMA = file.read()

with open(
    ROOT_CONFIGURATION_PATH, mode=FILE_MODE.READ, encoding=ENCODE.UTF8
) as file:
    ROOT_CONFIGURATION = yaml.load(file.read(), Loader=yaml.SafeLoader)

exception = match_schema(
    value=ROOT_CONFIGURATION,
    schema=CONFIGURATION_SCHEMA
)
if exception:
    raise Exception(str(exception))

configuration = ROOT_CONFIGURATION

configuration = Configuration(
    content=update_dict(ROOT_CONFIGURATION, dict())
)
