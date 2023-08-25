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
    CONF_DEVICES,
    CONF_COORDINATOR
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

from .temp_sensor import TempSensor
from .moisture_sensor import MoistureSensor
from .flow_sensor import FlowSensor



async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.info("------------")
    _LOGGER.info(config)
    _LOGGER.info("------------")
    coordinator = hass.data[DOMAIN][CONF_COORDINATOR]
    _LOGGER.info(coordinator)
    _LOGGER.info("------------")

    await coordinator.async_config_entry_first_refresh()
    
    
    temp_sensors = [
        TempSensor(coordinator, config[CONF_API_KEY], config[CONF_API_SECRET], deviceId, config[CONF_DEVICES][deviceId]['deviceName'])
        for deviceId in config[CONF_DEVICES]
    ]
    moisture_sensors = [
        MoistureSensor(coordinator, config[CONF_API_KEY], config[CONF_API_SECRET], deviceId, config[CONF_DEVICES][deviceId]['deviceName'])
        for deviceId in config[CONF_DEVICES]
    ]
    flow_sensors = [
        FlowSensor(coordinator, config[CONF_API_KEY], config[CONF_API_SECRET], deviceId, config[CONF_DEVICES][deviceId]['deviceName'])
        for deviceId in config[CONF_DEVICES]
    ]

    _LOGGER.info("!!!Rainpoint Sensor Setup done  - DOMAIN: %s", DOMAIN)
    async_add_entities(temp_sensors, update_before_add=True)
    async_add_entities(moisture_sensors, update_before_add=True)
    async_add_entities(flow_sensors, update_before_add=True)
    


async def async_setup_platform(
    hass: HomeAssistantType,  # pylint: disable=unused-argument
    config: ConfigType,
    async_add_entities: collections.abc.Callable,
    discovery_info: Optional[
        DiscoveryInfoType
    ] = None,  # pylint: disable=unused-argument
) -> None:
    #Set up the sensor platform by adding it into configuration.yaml
    _LOGGER.info("!!!! Create sensor entity")
    
    temp_sensors = MoistureSensor(hass.data[DOMAIN][CONF_COORDINATOR], config[CONF_API_KEY], config[CONF_API_SECRET] , config[CONF_DEVICES] )
    moisture_sensors = MoistureSensor(hass.data[DOMAIN][CONF_COORDINATOR], config[CONF_API_KEY], config[CONF_API_SECRET] , config[CONF_DEVICES] )
    flow_sensors = MoistureSensor(hass.data[DOMAIN][CONF_COORDINATOR], config[CONF_API_KEY], config[CONF_API_SECRET] , config[CONF_DEVICES] )
    async_add_entities([temp_sensors, moisture_sensors, flow_sensors], update_before_add=True)



