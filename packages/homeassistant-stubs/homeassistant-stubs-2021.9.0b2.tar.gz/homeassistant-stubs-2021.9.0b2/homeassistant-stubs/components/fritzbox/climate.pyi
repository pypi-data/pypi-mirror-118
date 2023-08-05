from . import FritzBoxEntity as FritzBoxEntity
from .const import ATTR_STATE_BATTERY_LOW as ATTR_STATE_BATTERY_LOW, ATTR_STATE_DEVICE_LOCKED as ATTR_STATE_DEVICE_LOCKED, ATTR_STATE_HOLIDAY_MODE as ATTR_STATE_HOLIDAY_MODE, ATTR_STATE_LOCKED as ATTR_STATE_LOCKED, ATTR_STATE_SUMMER_MODE as ATTR_STATE_SUMMER_MODE, ATTR_STATE_WINDOW_OPEN as ATTR_STATE_WINDOW_OPEN, CONF_COORDINATOR as CONF_COORDINATOR
from .model import ClimateExtraAttributes as ClimateExtraAttributes
from homeassistant.components.climate import ClimateEntity as ClimateEntity
from homeassistant.components.climate.const import ATTR_HVAC_MODE as ATTR_HVAC_MODE, HVAC_MODE_HEAT as HVAC_MODE_HEAT, HVAC_MODE_OFF as HVAC_MODE_OFF, PRESET_COMFORT as PRESET_COMFORT, PRESET_ECO as PRESET_ECO, SUPPORT_PRESET_MODE as SUPPORT_PRESET_MODE, SUPPORT_TARGET_TEMPERATURE as SUPPORT_TARGET_TEMPERATURE
from homeassistant.components.sensor import ATTR_STATE_CLASS as ATTR_STATE_CLASS
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import ATTR_BATTERY_LEVEL as ATTR_BATTERY_LEVEL, ATTR_DEVICE_CLASS as ATTR_DEVICE_CLASS, ATTR_ENTITY_ID as ATTR_ENTITY_ID, ATTR_NAME as ATTR_NAME, ATTR_TEMPERATURE as ATTR_TEMPERATURE, ATTR_UNIT_OF_MEASUREMENT as ATTR_UNIT_OF_MEASUREMENT, PRECISION_HALVES as PRECISION_HALVES, TEMP_CELSIUS as TEMP_CELSIUS
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from typing import Any

SUPPORT_FLAGS: Any
OPERATION_LIST: Any
MIN_TEMPERATURE: int
MAX_TEMPERATURE: int
PRESET_MANUAL: str
ON_API_TEMPERATURE: float
OFF_API_TEMPERATURE: float
ON_REPORT_SET_TEMPERATURE: float
OFF_REPORT_SET_TEMPERATURE: float

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class FritzboxThermostat(FritzBoxEntity, ClimateEntity):
    @property
    def supported_features(self) -> int: ...
    @property
    def temperature_unit(self) -> str: ...
    @property
    def precision(self) -> float: ...
    @property
    def current_temperature(self) -> float: ...
    @property
    def target_temperature(self) -> float: ...
    async def async_set_temperature(self, **kwargs: Any) -> None: ...
    @property
    def hvac_mode(self) -> str: ...
    @property
    def hvac_modes(self) -> list[str]: ...
    async def async_set_hvac_mode(self, hvac_mode: str) -> None: ...
    @property
    def preset_mode(self) -> Union[str, None]: ...
    @property
    def preset_modes(self) -> list[str]: ...
    async def async_set_preset_mode(self, preset_mode: str) -> None: ...
    @property
    def min_temp(self) -> int: ...
    @property
    def max_temp(self) -> int: ...
    @property
    def extra_state_attributes(self) -> ClimateExtraAttributes: ...
