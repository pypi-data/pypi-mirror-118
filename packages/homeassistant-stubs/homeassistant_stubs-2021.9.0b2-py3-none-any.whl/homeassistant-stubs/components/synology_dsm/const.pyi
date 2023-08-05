from homeassistant.components.binary_sensor import DEVICE_CLASS_SAFETY as DEVICE_CLASS_SAFETY, DEVICE_CLASS_UPDATE as DEVICE_CLASS_UPDATE
from homeassistant.components.sensor import ATTR_STATE_CLASS as ATTR_STATE_CLASS, STATE_CLASS_MEASUREMENT as STATE_CLASS_MEASUREMENT
from homeassistant.const import ATTR_DEVICE_CLASS as ATTR_DEVICE_CLASS, ATTR_ICON as ATTR_ICON, ATTR_NAME as ATTR_NAME, ATTR_UNIT_OF_MEASUREMENT as ATTR_UNIT_OF_MEASUREMENT, DATA_MEGABYTES as DATA_MEGABYTES, DATA_RATE_KILOBYTES_PER_SECOND as DATA_RATE_KILOBYTES_PER_SECOND, DATA_TERABYTES as DATA_TERABYTES, DEVICE_CLASS_TEMPERATURE as DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_TIMESTAMP as DEVICE_CLASS_TIMESTAMP, PERCENTAGE as PERCENTAGE, TEMP_CELSIUS as TEMP_CELSIUS
from typing import Any, Final, TypedDict

class EntityInfo(TypedDict):
    name: str
    unit_of_measurement: Union[str, None]
    icon: Union[str, None]
    device_class: Union[str, None]
    state_class: Union[str, None]
    enable: bool

DOMAIN: str
PLATFORMS: Any
COORDINATOR_CAMERAS: str
COORDINATOR_CENTRAL: str
COORDINATOR_SWITCHES: str
SYSTEM_LOADED: str
EXCEPTION_DETAILS: str
EXCEPTION_UNKNOWN: str
SYNO_API: str
UNDO_UPDATE_LISTENER: str
CONF_SERIAL: str
CONF_VOLUMES: str
CONF_DEVICE_TOKEN: str
DEFAULT_USE_SSL: bool
DEFAULT_VERIFY_SSL: bool
DEFAULT_PORT: int
DEFAULT_PORT_SSL: int
DEFAULT_SCAN_INTERVAL: int
DEFAULT_TIMEOUT: int
ENTITY_UNIT_LOAD: str
ENTITY_ENABLE: Final[str]
SERVICE_REBOOT: str
SERVICE_SHUTDOWN: str
SERVICES: Any
UPGRADE_BINARY_SENSORS: dict[str, EntityInfo]
SECURITY_BINARY_SENSORS: dict[str, EntityInfo]
STORAGE_DISK_BINARY_SENSORS: dict[str, EntityInfo]
UTILISATION_SENSORS: dict[str, EntityInfo]
STORAGE_VOL_SENSORS: dict[str, EntityInfo]
STORAGE_DISK_SENSORS: dict[str, EntityInfo]
INFORMATION_SENSORS: dict[str, EntityInfo]
SURVEILLANCE_SWITCH: dict[str, EntityInfo]
