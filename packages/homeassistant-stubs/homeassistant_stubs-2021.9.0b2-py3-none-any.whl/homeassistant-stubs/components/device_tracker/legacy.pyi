import voluptuous as vol
from .const import ATTR_ATTRIBUTES as ATTR_ATTRIBUTES, ATTR_BATTERY as ATTR_BATTERY, ATTR_CONSIDER_HOME as ATTR_CONSIDER_HOME, ATTR_DEV_ID as ATTR_DEV_ID, ATTR_GPS as ATTR_GPS, ATTR_HOST_NAME as ATTR_HOST_NAME, ATTR_LOCATION_NAME as ATTR_LOCATION_NAME, ATTR_MAC as ATTR_MAC, ATTR_SOURCE_TYPE as ATTR_SOURCE_TYPE, CONF_CONSIDER_HOME as CONF_CONSIDER_HOME, CONF_NEW_DEVICE_DEFAULTS as CONF_NEW_DEVICE_DEFAULTS, CONF_SCAN_INTERVAL as CONF_SCAN_INTERVAL, CONF_TRACK_NEW as CONF_TRACK_NEW, DEFAULT_CONSIDER_HOME as DEFAULT_CONSIDER_HOME, DEFAULT_TRACK_NEW as DEFAULT_TRACK_NEW, DOMAIN as DOMAIN, LOGGER as LOGGER, PLATFORM_TYPE_LEGACY as PLATFORM_TYPE_LEGACY, SCAN_INTERVAL as SCAN_INTERVAL, SOURCE_TYPE_BLUETOOTH as SOURCE_TYPE_BLUETOOTH, SOURCE_TYPE_BLUETOOTH_LE as SOURCE_TYPE_BLUETOOTH_LE, SOURCE_TYPE_GPS as SOURCE_TYPE_GPS, SOURCE_TYPE_ROUTER as SOURCE_TYPE_ROUTER
from collections.abc import Coroutine, Sequence
from datetime import timedelta
from homeassistant import util as util
from homeassistant.components import zone as zone
from homeassistant.config import async_log_exception as async_log_exception, load_yaml_config_file as load_yaml_config_file
from homeassistant.const import ATTR_ENTITY_ID as ATTR_ENTITY_ID, ATTR_GPS_ACCURACY as ATTR_GPS_ACCURACY, ATTR_ICON as ATTR_ICON, ATTR_LATITUDE as ATTR_LATITUDE, ATTR_LONGITUDE as ATTR_LONGITUDE, ATTR_NAME as ATTR_NAME, CONF_ICON as CONF_ICON, CONF_MAC as CONF_MAC, CONF_NAME as CONF_NAME, DEVICE_DEFAULT_NAME as DEVICE_DEFAULT_NAME, STATE_HOME as STATE_HOME, STATE_NOT_HOME as STATE_NOT_HOME
from homeassistant.core import HomeAssistant as HomeAssistant, ServiceCall as ServiceCall, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers import config_per_platform as config_per_platform, discovery as discovery
from homeassistant.helpers.entity_registry import async_get_registry as async_get_registry
from homeassistant.helpers.event import async_track_time_interval as async_track_time_interval, async_track_utc_time_change as async_track_utc_time_change
from homeassistant.helpers.restore_state import RestoreEntity as RestoreEntity
from homeassistant.helpers.typing import ConfigType as ConfigType, GPSType as GPSType, StateType as StateType
from homeassistant.setup import async_prepare_setup_platform as async_prepare_setup_platform, async_start_setup as async_start_setup
from homeassistant.util import dt as dt_util
from homeassistant.util.yaml import dump as dump
from types import ModuleType
from typing import Any, Callable, Final

SERVICE_SEE: Final[str]
SOURCE_TYPES: Final[tuple[str, ...]]
NEW_DEVICE_DEFAULTS_SCHEMA: Any
PLATFORM_SCHEMA: Final[Any]
PLATFORM_SCHEMA_BASE: Final[vol.Schema]
SERVICE_SEE_PAYLOAD_SCHEMA: Final[vol.Schema]
YAML_DEVICES: Final[str]
EVENT_NEW_DEVICE: Final[str]

def see(hass: HomeAssistant, mac: Union[str, None] = ..., dev_id: Union[str, None] = ..., host_name: Union[str, None] = ..., location_name: Union[str, None] = ..., gps: Union[GPSType, None] = ..., gps_accuracy: Union[int, None] = ..., battery: Union[int, None] = ..., attributes: Union[dict, None] = ...) -> None: ...
async def async_setup_integration(hass: HomeAssistant, config: ConfigType) -> None: ...

class DeviceTrackerPlatform:
    LEGACY_SETUP: Final[tuple[str, ...]]
    name: str
    platform: ModuleType
    config: dict
    @property
    def type(self) -> Union[str, None]: ...
    async def async_setup_legacy(self, hass: HomeAssistant, tracker: DeviceTracker, discovery_info: Union[dict[str, Any], None] = ...) -> None: ...
    def __init__(self, name, platform, config) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

async def async_extract_config(hass: HomeAssistant, config: ConfigType) -> list[DeviceTrackerPlatform]: ...
async def async_create_platform_type(hass: HomeAssistant, config: ConfigType, p_type: str, p_config: dict) -> Union[DeviceTrackerPlatform, None]: ...
def async_setup_scanner_platform(hass: HomeAssistant, config: ConfigType, scanner: DeviceScanner, async_see_device: Callable[..., Coroutine[None, None, None]], platform: str) -> None: ...
async def get_tracker(hass: HomeAssistant, config: ConfigType) -> DeviceTracker: ...

class DeviceTracker:
    hass: Any
    devices: Any
    mac_to_dev: Any
    consider_home: Any
    track_new: Any
    defaults: Any
    _is_updating: Any
    def __init__(self, hass: HomeAssistant, consider_home: timedelta, track_new: bool, defaults: dict[str, Any], devices: Sequence[Device]) -> None: ...
    def see(self, mac: Union[str, None] = ..., dev_id: Union[str, None] = ..., host_name: Union[str, None] = ..., location_name: Union[str, None] = ..., gps: Union[GPSType, None] = ..., gps_accuracy: Union[int, None] = ..., battery: Union[int, None] = ..., attributes: Union[dict, None] = ..., source_type: str = ..., picture: Union[str, None] = ..., icon: Union[str, None] = ..., consider_home: Union[timedelta, None] = ...) -> None: ...
    async def async_see(self, mac: Union[str, None] = ..., dev_id: Union[str, None] = ..., host_name: Union[str, None] = ..., location_name: Union[str, None] = ..., gps: Union[GPSType, None] = ..., gps_accuracy: Union[int, None] = ..., battery: Union[int, None] = ..., attributes: Union[dict, None] = ..., source_type: str = ..., picture: Union[str, None] = ..., icon: Union[str, None] = ..., consider_home: Union[timedelta, None] = ...) -> None: ...
    async def async_update_config(self, path: str, dev_id: str, device: Device) -> None: ...
    def async_update_stale(self, now: dt_util.dt.datetime) -> None: ...
    async def async_setup_tracked_device(self) -> None: ...

class Device(RestoreEntity):
    host_name: Union[str, None]
    location_name: Union[str, None]
    gps: Union[GPSType, None]
    gps_accuracy: int
    last_seen: Union[dt_util.dt.datetime, None]
    battery: Union[int, None]
    attributes: Union[dict, None]
    last_update_home: bool
    _state: str
    hass: Any
    entity_id: Any
    consider_home: Any
    dev_id: Any
    mac: Any
    track: Any
    config_name: Any
    config_picture: Any
    _icon: Any
    source_type: Any
    _attributes: Any
    def __init__(self, hass: HomeAssistant, consider_home: timedelta, track: bool, dev_id: str, mac: Union[str, None], name: Union[str, None] = ..., picture: Union[str, None] = ..., gravatar: Union[str, None] = ..., icon: Union[str, None] = ...) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def state(self) -> str: ...
    @property
    def entity_picture(self) -> Union[str, None]: ...
    @property
    def state_attributes(self) -> dict[str, StateType]: ...
    @property
    def extra_state_attributes(self) -> dict[str, Any]: ...
    @property
    def icon(self) -> Union[str, None]: ...
    async def async_seen(self, host_name: Union[str, None] = ..., location_name: Union[str, None] = ..., gps: Union[GPSType, None] = ..., gps_accuracy: Union[int, None] = ..., battery: Union[int, None] = ..., attributes: Union[dict[str, Any], None] = ..., source_type: str = ..., consider_home: Union[timedelta, None] = ...) -> None: ...
    def stale(self, now: Union[dt_util.dt.datetime, None] = ...) -> bool: ...
    def mark_stale(self) -> None: ...
    async def async_update(self) -> None: ...
    async def async_added_to_hass(self) -> None: ...

class DeviceScanner:
    hass: Union[HomeAssistant, None]
    def scan_devices(self) -> list[str]: ...
    async def async_scan_devices(self) -> list[str]: ...
    def get_device_name(self, device: str) -> Union[str, None]: ...
    async def async_get_device_name(self, device: str) -> Union[str, None]: ...
    def get_extra_attributes(self, device: str) -> dict: ...
    async def async_get_extra_attributes(self, device: str) -> dict: ...

async def async_load_config(path: str, hass: HomeAssistant, consider_home: timedelta) -> list[Device]: ...
def update_config(path: str, dev_id: str, device: Device) -> None: ...
def get_gravatar_for_email(email: str) -> str: ...
