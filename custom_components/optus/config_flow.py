import logging

import voluptuous as vol
from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback

from .const import (  # pylint:disable=unused-import
    DOMAIN,
    MOBILE
)
from optus import Account

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(MOBILE): vol.All(str, vol.Length(min=10, max=10)),
    }
)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    _LOGGER.debug(data[MOBILE])
    account = Account(data[CONF_USERNAME], data[CONF_PASSWORD], data[MOBILE])

    try:
        result = await hass.async_add_executor_job(account.auth)

    except Exception as ex:
        raise InvalidAuth from ex

    if not result:
        _LOGGER.error("Failed to authenticate with optus")
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {"title": f"Mobile ({data[MOBILE]})"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Optus."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                print("EXCEPT")
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )




class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
    _LOGGER.error("Failed to authenticate with optus")
