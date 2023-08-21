"""
    Sensor: Rainpoint 
"""

import logging
from typing import Optional
import collections.abc

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from datetime import timedelta
from homeassistant import core, config_entries
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA
)
from .const import (
    CONF_API_KEY,
    CONF_API_SECRET, 
    CONF_DEVICES
)

from homeassistant.core import DOMAIN

from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

_LOGGER = logging.getLogger(__name__)

# Time between updating data from tuya api
SCAN_INTERVAL = timedelta(minutes=1)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_API_SECRET): cv.string,
    }
)

from .live_sensor import LiveSensor



async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    live_sensors = [
        LiveSensor(config[CONF_API_KEY], config[CONF_API_SECRET], deviceId)
        for deviceId in config[CONF_DEVICES]
    ]
    _LOGGER.debug("Rainpoint Sensor Setup done  - DOMAIN: %s", DOMAIN)
    async_add_entities(live_sensors, update_before_add=True)
    


async def async_setup_platform(
    hass: HomeAssistantType,  # pylint: disable=unused-argument
    config: ConfigType,
    async_add_entities: collections.abc.Callable,
    discovery_info: Optional[
        DiscoveryInfoType
    ] = None,  # pylint: disable=unused-argument
) -> None:
    """Set up the sensor platform by adding it into configuration.yaml"""
    live_sensor = LiveSensor(config[CONF_API_KEY], config[CONF_API_SECRET] , config[CONF_DEVICES] )
    async_add_entities([live_sensor], update_before_add=True)

