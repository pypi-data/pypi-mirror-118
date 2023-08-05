import re
import voluptuous as vol
from collections.abc import Hashable
from datetime import date as date_sys, datetime as datetime_sys, time as time_sys, timedelta
from enum import Enum
from homeassistant.const import ATTR_AREA_ID as ATTR_AREA_ID, ATTR_DEVICE_ID as ATTR_DEVICE_ID, ATTR_ENTITY_ID as ATTR_ENTITY_ID, CONF_ABOVE as CONF_ABOVE, CONF_ALIAS as CONF_ALIAS, CONF_ATTRIBUTE as CONF_ATTRIBUTE, CONF_BELOW as CONF_BELOW, CONF_CHOOSE as CONF_CHOOSE, CONF_CONDITION as CONF_CONDITION, CONF_CONDITIONS as CONF_CONDITIONS, CONF_CONTINUE_ON_TIMEOUT as CONF_CONTINUE_ON_TIMEOUT, CONF_COUNT as CONF_COUNT, CONF_DEFAULT as CONF_DEFAULT, CONF_DELAY as CONF_DELAY, CONF_DEVICE_ID as CONF_DEVICE_ID, CONF_DOMAIN as CONF_DOMAIN, CONF_ENTITY_ID as CONF_ENTITY_ID, CONF_ENTITY_NAMESPACE as CONF_ENTITY_NAMESPACE, CONF_EVENT as CONF_EVENT, CONF_EVENT_DATA as CONF_EVENT_DATA, CONF_EVENT_DATA_TEMPLATE as CONF_EVENT_DATA_TEMPLATE, CONF_FOR as CONF_FOR, CONF_ID as CONF_ID, CONF_PLATFORM as CONF_PLATFORM, CONF_REPEAT as CONF_REPEAT, CONF_SCAN_INTERVAL as CONF_SCAN_INTERVAL, CONF_SCENE as CONF_SCENE, CONF_SEQUENCE as CONF_SEQUENCE, CONF_SERVICE as CONF_SERVICE, CONF_SERVICE_TEMPLATE as CONF_SERVICE_TEMPLATE, CONF_STATE as CONF_STATE, CONF_TARGET as CONF_TARGET, CONF_TIMEOUT as CONF_TIMEOUT, CONF_UNIT_SYSTEM_IMPERIAL as CONF_UNIT_SYSTEM_IMPERIAL, CONF_UNIT_SYSTEM_METRIC as CONF_UNIT_SYSTEM_METRIC, CONF_UNTIL as CONF_UNTIL, CONF_VALUE_TEMPLATE as CONF_VALUE_TEMPLATE, CONF_VARIABLES as CONF_VARIABLES, CONF_WAIT_FOR_TRIGGER as CONF_WAIT_FOR_TRIGGER, CONF_WAIT_TEMPLATE as CONF_WAIT_TEMPLATE, CONF_WHILE as CONF_WHILE, ENTITY_MATCH_ALL as ENTITY_MATCH_ALL, ENTITY_MATCH_NONE as ENTITY_MATCH_NONE, SUN_EVENT_SUNRISE as SUN_EVENT_SUNRISE, SUN_EVENT_SUNSET as SUN_EVENT_SUNSET, TEMP_CELSIUS as TEMP_CELSIUS, TEMP_FAHRENHEIT as TEMP_FAHRENHEIT, WEEKDAYS as WEEKDAYS
from homeassistant.core import split_entity_id as split_entity_id, valid_entity_id as valid_entity_id
from homeassistant.exceptions import TemplateError as TemplateError
from homeassistant.helpers import template as template_helper
from homeassistant.helpers.logging import KeywordStyleAdapter as KeywordStyleAdapter
from homeassistant.util import raise_if_invalid_path as raise_if_invalid_path
from typing import Any, Callable, TypeVar

TIME_PERIOD_ERROR: str
byte: Any
small_float: Any
positive_int: Any
positive_float: Any
latitude: Any
longitude: Any
gps: Any
sun_event: Any
port: Any
T = TypeVar('T')

def path(value: Any) -> str: ...
def has_at_least_one_key(*keys: Any) -> Callable[[dict], dict]: ...
def has_at_most_one_key(*keys: Any) -> Callable[[dict], dict]: ...
def boolean(value: Any) -> bool: ...

_WS: Any

def whitespace(value: Any) -> str: ...
def isdevice(value: Any) -> str: ...
def matches_regex(regex: str) -> Callable[[Any], str]: ...
def is_regex(value: Any) -> re.Pattern[Any]: ...
def isfile(value: Any) -> str: ...
def isdir(value: Any) -> str: ...
def ensure_list(value: Union[T, list[T], None]) -> list[T]: ...
def entity_id(value: Any) -> str: ...
def entity_ids(value: Union[str, list]) -> list[str]: ...

comp_entity_ids: Any

def entity_domain(domain: Union[str, list[str]]) -> Callable[[Any], str]: ...
def entities_domain(domain: Union[str, list[str]]) -> Callable[[Union[str, list]], list[str]]: ...
def enum(enumClass: type[Enum]) -> vol.All: ...
def icon(value: Any) -> str: ...

time_period_dict: Any

def time(value: Any) -> time_sys: ...
def date(value: Any) -> date_sys: ...
def time_period_str(value: str) -> timedelta: ...
def time_period_seconds(value: Union[float, str]) -> timedelta: ...

time_period: Any

def match_all(value: T) -> T: ...
def positive_timedelta(value: timedelta) -> timedelta: ...

positive_time_period_dict: Any
positive_time_period: Any

def remove_falsy(value: list[T]) -> list[T]: ...
def service(value: Any) -> str: ...
def slug(value: Any) -> str: ...
def schema_with_slug_keys(value_schema: Union[T, Callable], *, slug_validator: Callable[[Any], str] = ...) -> Callable: ...
def slugify(value: Any) -> str: ...
def string(value: Any) -> str: ...
def string_with_no_html(value: Any) -> str: ...
def temperature_unit(value: Any) -> str: ...

unit_system: Any

def template(value: Union[Any, None]) -> template_helper.Template: ...
def dynamic_template(value: Union[Any, None]) -> template_helper.Template: ...
def template_complex(value: Any) -> Any: ...

positive_time_period_template: Any

def datetime(value: Any) -> datetime_sys: ...
def time_zone(value: str) -> str: ...

weekdays: Any

def socket_timeout(value: Union[Any, None]) -> object: ...
def url(value: Any) -> str: ...
def url_no_path(value: Any) -> str: ...
def x10_address(value: str) -> str: ...
def uuid4_hex(value: Any) -> str: ...
def ensure_list_csv(value: Any) -> list: ...

class multi_select:
    options: Any
    def __init__(self, options: dict) -> None: ...
    def __call__(self, selected: list) -> list: ...

def deprecated(key: str, replacement_key: Union[str, None] = ..., default: Union[Any, None] = ...) -> Callable[[dict], dict]: ...
def key_value_schemas(key: str, value_schemas: dict[Hashable, vol.Schema]) -> Callable[[Any], dict[Hashable, Any]]: ...
def key_dependency(key: Hashable, dependency: Hashable) -> Callable[[dict[Hashable, Any]], dict[Hashable, Any]]: ...
def custom_serializer(schema: Any) -> Any: ...

PLATFORM_SCHEMA: Any
PLATFORM_SCHEMA_BASE: Any
ENTITY_SERVICE_FIELDS: Any

def make_entity_service_schema(schema: dict, *, extra: int = ...) -> vol.Schema: ...

SCRIPT_VARIABLES_SCHEMA: Any

def script_action(value: Any) -> dict: ...

SCRIPT_SCHEMA: Any
SCRIPT_ACTION_BASE_SCHEMA: Any
EVENT_SCHEMA: Any
SERVICE_SCHEMA: Any
NUMERIC_STATE_THRESHOLD_SCHEMA: Any
CONDITION_BASE_SCHEMA: Any
NUMERIC_STATE_CONDITION_SCHEMA: Any
STATE_CONDITION_BASE_SCHEMA: Any
STATE_CONDITION_STATE_SCHEMA: Any
STATE_CONDITION_ATTRIBUTE_SCHEMA: Any

def STATE_CONDITION_SCHEMA(value: Any) -> dict: ...

SUN_CONDITION_SCHEMA: Any
TEMPLATE_CONDITION_SCHEMA: Any
TIME_CONDITION_SCHEMA: Any
TRIGGER_CONDITION_SCHEMA: Any
ZONE_CONDITION_SCHEMA: Any
AND_CONDITION_SCHEMA: Any
OR_CONDITION_SCHEMA: Any
NOT_CONDITION_SCHEMA: Any
DEVICE_CONDITION_BASE_SCHEMA: Any
DEVICE_CONDITION_SCHEMA: Any
CONDITION_SCHEMA: vol.Schema
TRIGGER_BASE_SCHEMA: Any
TRIGGER_SCHEMA: Any
_SCRIPT_DELAY_SCHEMA: Any
_SCRIPT_WAIT_TEMPLATE_SCHEMA: Any
DEVICE_ACTION_BASE_SCHEMA: Any
DEVICE_ACTION_SCHEMA: Any
_SCRIPT_SCENE_SCHEMA: Any
_SCRIPT_REPEAT_SCHEMA: Any
_SCRIPT_CHOOSE_SCHEMA: Any
_SCRIPT_WAIT_FOR_TRIGGER_SCHEMA: Any
_SCRIPT_SET_SCHEMA: Any
SCRIPT_ACTION_DELAY: str
SCRIPT_ACTION_WAIT_TEMPLATE: str
SCRIPT_ACTION_CHECK_CONDITION: str
SCRIPT_ACTION_FIRE_EVENT: str
SCRIPT_ACTION_CALL_SERVICE: str
SCRIPT_ACTION_DEVICE_AUTOMATION: str
SCRIPT_ACTION_ACTIVATE_SCENE: str
SCRIPT_ACTION_REPEAT: str
SCRIPT_ACTION_CHOOSE: str
SCRIPT_ACTION_WAIT_FOR_TRIGGER: str
SCRIPT_ACTION_VARIABLES: str

def determine_script_action(action: dict[str, Any]) -> str: ...

ACTION_TYPE_SCHEMAS: dict[str, Callable[[Any], dict]]
currency: Any
