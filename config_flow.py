"""
Setting up Rainpoint config flow for homeassistant
"""
import logging
import traceback

from typing import Any, Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant import config_entries

from .api import Rainpoint
from .const import DOMAIN, CONF_API_KEY, CONF_API_SECRET, CONF_DEVICES


_LOGGER = logging.getLogger(__name__)

KEY_SCHEMA = vol.Schema(
    {vol.Required(CONF_API_KEY): cv.string, vol.Required(CONF_API_SECRET): cv.string}
)


class RainpointCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Rainpoint config flow"""

    VERSION = 1

    async def validate_auth(self, api_key: str, api_secret: str) -> dict[dict]:
        """
        Validates credentials for Rainpoint Cloud.
        """
        try:
            rainpoint = Rainpoint(api_key, api_secret)
            await self.hass.async_add_executor_job(rainpoint.login)
            
            devices = await self.hass.async_add_executor_job(rainpoint.devices)
            _LOGGER.info("Rainpoint Validate Authenticatin done devices %s" % devices)
            return devices if devices is not None else []
        
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Error validating Tuya Cloud Access")
            _LOGGER.exception(exception)
        
        


    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                devices = await self.validate_auth(
                    user_input[CONF_API_KEY], user_input[CONF_API_SECRET]
                )
            except Exception as exception:  # pylint: disable=broad-except
                _LOGGER.error("Error validating Tuya Cloud Access")
                _LOGGER.exception(exception)
                errors["base"] = "auth"
            if not errors:
                # Input is valid, set data
                self.data = user_input
                self.data[CONF_DEVICES] = devices
                
                _LOGGER.debug("Setup Device device data: %s" % devices)
                return self.async_create_entry(title='Rainpoint', data=self.data )
        _LOGGER.info("MG Setup API key done")
        return self.async_show_form(
            step_id="user", data_schema=KEY_SCHEMA, errors=errors
        )
    


