from . import Recorder as Recorder
from .const import DOMAIN as DOMAIN
from .models import StatisticMetaData as StatisticMetaData, Statistics as Statistics, StatisticsMeta as StatisticsMeta, StatisticsRuns as StatisticsRuns, process_timestamp_to_utc_isoformat as process_timestamp_to_utc_isoformat
from .util import execute as execute, retryable_database_job as retryable_database_job, session_scope as session_scope
from datetime import datetime
from homeassistant.const import PRESSURE_PA as PRESSURE_PA, TEMP_CELSIUS as TEMP_CELSIUS, VOLUME_CUBIC_FEET as VOLUME_CUBIC_FEET, VOLUME_CUBIC_METERS as VOLUME_CUBIC_METERS
from homeassistant.core import Event as Event, HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers import entity_registry as entity_registry
from homeassistant.util.unit_system import UnitSystem as UnitSystem
from sqlalchemy.orm.scoping import scoped_session as scoped_session
from typing import Any

QUERY_STATISTICS: Any
QUERY_STATISTIC_META: Any
QUERY_STATISTIC_META_ID: Any
STATISTICS_BAKERY: str
STATISTICS_META_BAKERY: str
UNIT_CONVERSIONS: Any
_LOGGER: Any

def async_setup(hass: HomeAssistant) -> None: ...
def get_start_time() -> datetime: ...
def _get_metadata_ids(hass: HomeAssistant, session: scoped_session, statistic_ids: list[str]) -> list[str]: ...
def _update_or_add_metadata(hass: HomeAssistant, session: scoped_session, statistic_id: str, new_metadata: StatisticMetaData) -> str: ...
def compile_statistics(instance: Recorder, start: datetime) -> bool: ...
def _get_metadata(hass: HomeAssistant, session: scoped_session, statistic_ids: Union[list[str], None], statistic_type: Union[str, None]) -> dict[str, StatisticMetaData]: ...
def get_metadata(hass: HomeAssistant, statistic_id: str) -> Union[StatisticMetaData, None]: ...
def _configured_unit(unit: str, units: UnitSystem) -> str: ...
def list_statistic_ids(hass: HomeAssistant, statistic_type: Union[str, None] = ...) -> list[Union[StatisticMetaData, None]]: ...
def statistics_during_period(hass: HomeAssistant, start_time: datetime, end_time: Union[datetime, None] = ..., statistic_ids: Union[list[str], None] = ...) -> dict[str, list[dict[str, str]]]: ...
def get_last_statistics(hass: HomeAssistant, number_of_stats: int, statistic_id: str) -> dict[str, list[dict]]: ...
def _sorted_statistics_to_dict(hass: HomeAssistant, stats: list, statistic_ids: Union[list[str], None], metadata: dict[str, StatisticMetaData]) -> dict[str, list[dict]]: ...
