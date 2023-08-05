import ruamel.yaml
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.util.yaml import secret_yaml as secret_yaml
from ruamel.yaml.constructor import SafeConstructor
from typing import Any, Union

_LOGGER: Any
JSON_TYPE = Union[list, dict, str]

class ExtSafeConstructor(SafeConstructor):
    name: Union[str, None]

class UnsupportedYamlError(HomeAssistantError): ...
class WriteError(HomeAssistantError): ...

def _include_yaml(constructor: ExtSafeConstructor, node: ruamel.yaml.nodes.Node) -> JSON_TYPE: ...
def _yaml_unsupported(constructor: ExtSafeConstructor, node: ruamel.yaml.nodes.Node) -> None: ...
def object_to_yaml(data: JSON_TYPE) -> str: ...
def yaml_to_object(data: str) -> JSON_TYPE: ...
def load_yaml(fname: str, round_trip: bool = ...) -> JSON_TYPE: ...
def save_yaml(fname: str, data: JSON_TYPE) -> None: ...
