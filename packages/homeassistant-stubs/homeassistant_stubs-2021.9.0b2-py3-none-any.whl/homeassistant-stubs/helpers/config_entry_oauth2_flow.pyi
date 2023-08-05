import abc
import logging
from .aiohttp_client import async_get_clientsession as async_get_clientsession
from abc import ABC, ABCMeta, abstractmethod
from aiohttp import client as client, web
from collections.abc import Awaitable
from homeassistant import config_entries as config_entries
from homeassistant.components import http as http
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.helpers.network import NoURLAvailableError as NoURLAvailableError
from typing import Any, Callable

_LOGGER: Any
DATA_JWT_SECRET: str
DATA_VIEW_REGISTERED: str
DATA_IMPLEMENTATIONS: str
DATA_PROVIDERS: str
AUTH_CALLBACK_PATH: str
HEADER_FRONTEND_BASE: str
CLOCK_OUT_OF_SYNC_MAX_SEC: int

class AbstractOAuth2Implementation(ABC, metaclass=abc.ABCMeta):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @property
    @abstractmethod
    def domain(self) -> str: ...
    @abstractmethod
    async def async_generate_authorize_url(self, flow_id: str) -> str: ...
    @abstractmethod
    async def async_resolve_external_data(self, external_data: Any) -> dict: ...
    async def async_refresh_token(self, token: dict) -> dict: ...
    @abstractmethod
    async def _async_refresh_token(self, token: dict) -> dict: ...

class LocalOAuth2Implementation(AbstractOAuth2Implementation):
    hass: Any
    _domain: Any
    client_id: Any
    client_secret: Any
    authorize_url: Any
    token_url: Any
    def __init__(self, hass: HomeAssistant, domain: str, client_id: str, client_secret: str, authorize_url: str, token_url: str) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def domain(self) -> str: ...
    @property
    def redirect_uri(self) -> str: ...
    @property
    def extra_authorize_data(self) -> dict: ...
    async def async_generate_authorize_url(self, flow_id: str) -> str: ...
    async def async_resolve_external_data(self, external_data: Any) -> dict: ...
    async def _async_refresh_token(self, token: dict) -> dict: ...
    async def _token_request(self, data: dict) -> dict: ...

class AbstractOAuth2FlowHandler(config_entries.ConfigFlow, metaclass=ABCMeta):
    DOMAIN: str
    VERSION: int
    external_data: Any
    flow_impl: Any
    def __init__(self) -> None: ...
    @property
    @abstractmethod
    def logger(self) -> logging.Logger: ...
    @property
    def extra_authorize_data(self) -> dict: ...
    async def async_step_pick_implementation(self, user_input: Union[dict, None] = ...) -> FlowResult: ...
    async def async_step_auth(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_creation(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_oauth_create_entry(self, data: dict) -> FlowResult: ...
    async def async_step_user(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    @classmethod
    def async_register_implementation(cls, hass: HomeAssistant, local_impl: LocalOAuth2Implementation) -> None: ...

def async_register_implementation(hass: HomeAssistant, domain: str, implementation: AbstractOAuth2Implementation) -> None: ...
async def async_get_implementations(hass: HomeAssistant, domain: str) -> dict[str, AbstractOAuth2Implementation]: ...
async def async_get_config_entry_implementation(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> AbstractOAuth2Implementation: ...
def async_add_implementation_provider(hass: HomeAssistant, provider_domain: str, async_provide_implementation: Callable[[HomeAssistant, str], Awaitable[Union[AbstractOAuth2Implementation, None]]]) -> None: ...

class OAuth2AuthorizeCallbackView(http.HomeAssistantView):
    requires_auth: bool
    url: Any
    name: str
    async def get(self, request: web.Request) -> web.Response: ...

class OAuth2Session:
    hass: Any
    config_entry: Any
    implementation: Any
    def __init__(self, hass: HomeAssistant, config_entry: config_entries.ConfigEntry, implementation: AbstractOAuth2Implementation) -> None: ...
    @property
    def token(self) -> dict: ...
    @property
    def valid_token(self) -> bool: ...
    async def async_ensure_token_valid(self) -> None: ...
    async def async_request(self, method: str, url: str, **kwargs: Any) -> client.ClientResponse: ...

async def async_oauth2_request(hass: HomeAssistant, token: dict, method: str, url: str, **kwargs: Any) -> client.ClientResponse: ...
def _encode_jwt(hass: HomeAssistant, data: dict) -> str: ...
def _decode_jwt(hass: HomeAssistant, encoded: str) -> Union[dict, None]: ...
