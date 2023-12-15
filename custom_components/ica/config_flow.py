"""Config flow for ICA integration."""

from http import HTTPStatus
import logging
from typing import Any

from requests.exceptions import HTTPError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .icaapi_async import IcaAPIAsync
from .const import DOMAIN, CONF_ICA_ID, CONF_ICA_PIN, CONF_NUM_RECIPES

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ICA_ID, description="user id (personal ID number)"): str,
        vol.Required(CONF_ICA_PIN, description="pin code"): str,
        vol.Required(
            CONF_NUM_RECIPES, default=5, description="# random recipes to retrieve"
        ): int,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ICA."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, str] = {}
        if user_input is not None:
            api = IcaAPIAsync(user_input[CONF_ICA_ID], user_input[CONF_ICA_PIN])
            nRecipes = user_input[CONF_NUM_RECIPES]
            try:
                await api.get_shopping_lists()
            except HTTPError as err:
                if err.response.status_code == HTTPStatus.UNAUTHORIZED:
                    errors["base"] = "invalid_credentials"
                else:
                    errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=DOMAIN, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
