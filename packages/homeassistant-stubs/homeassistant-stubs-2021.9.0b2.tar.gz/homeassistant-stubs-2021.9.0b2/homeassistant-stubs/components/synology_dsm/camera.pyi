from . import SynoApi as SynoApi, SynologyDSMBaseEntity as SynologyDSMBaseEntity
from .const import COORDINATOR_CAMERAS as COORDINATOR_CAMERAS, DOMAIN as DOMAIN, ENTITY_ENABLE as ENTITY_ENABLE, SYNO_API as SYNO_API
from homeassistant.components.camera import Camera as Camera, SUPPORT_STREAM as SUPPORT_STREAM
from homeassistant.components.sensor import ATTR_STATE_CLASS as ATTR_STATE_CLASS
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import ATTR_DEVICE_CLASS as ATTR_DEVICE_CLASS, ATTR_ICON as ATTR_ICON, ATTR_NAME as ATTR_NAME, ATTR_UNIT_OF_MEASUREMENT as ATTR_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.entity import DeviceInfo as DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator as DataUpdateCoordinator
from synology_dsm.api.surveillance_station import SynoCamera as SynoCamera
from typing import Any

_LOGGER: Any

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class SynoDSMCamera(SynologyDSMBaseEntity, Camera):
    coordinator: DataUpdateCoordinator[dict[str, dict[str, SynoCamera]]]
    _camera_id: Any
    def __init__(self, api: SynoApi, coordinator: DataUpdateCoordinator[dict[str, dict[str, SynoCamera]]], camera_id: str) -> None: ...
    @property
    def camera_data(self) -> SynoCamera: ...
    @property
    def device_info(self) -> DeviceInfo: ...
    @property
    def available(self) -> bool: ...
    @property
    def supported_features(self) -> int: ...
    @property
    def is_recording(self) -> bool: ...
    @property
    def motion_detection_enabled(self) -> bool: ...
    def camera_image(self, width: Union[int, None] = ..., height: Union[int, None] = ...) -> Union[bytes, None]: ...
    async def stream_source(self) -> Union[str, None]: ...
    def enable_motion_detection(self) -> None: ...
    def disable_motion_detection(self) -> None: ...
