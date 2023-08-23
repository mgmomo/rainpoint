"""Setup Rainpoint component."""
from datetime import timedelta
from typing import Any
import logging
from .const import (
    CONF_COORDINATOR, 
    CONF_DEVICES
)

from homeassistant import core, config_entries
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.core import DOMAIN
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import Rainpoint



_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: core.HomeAssistant,
        entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data


    coordinator = RainpointDataUpdateCoordinator(hass,  entry=entry)
    hass.data[DOMAIN][CONF_COORDINATOR] = coordinator

    # Forward the setup to the sensor platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True


class RainpointDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Rainpoint API."""

    def __init__(self, hass, entry) -> None:
        """Initialize."""
        _LOGGER.info("Initialize Rainpoint update coordinator")
        
        scan_interval = timedelta(seconds=30)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)
        self.entry_data  = hass.data[DOMAIN][entry.entry_id]

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            _LOGGER.info("Refreshing Rainpoint update coordinator %s " % self.entry_data)
            rainpoint = Rainpoint(self.entry_data['api_key'], self.entry_data['api_secret'])
            await self.hass.async_add_executor_job(rainpoint.login)


            sensors_properties = {}
            sensor_values = {}
            for deviceId in self.entry_data[CONF_DEVICES]:
                result = await  self.hass.async_add_executor_job(rainpoint.getProperties, deviceId)
                
                for i in result:
                    if i['code'] == 'Temp':
                        sensor_values['Temp'] = i['value']
                    if i['code'] == 'Moisure':
                        sensor_values['Moisure'] = i['value']
                    if i['code'] == 'Flow':
                        sensor_values['Flow'] = i['value']
                    if i['code'] == 'BatteryCapacity':
                        sensor_values['BatteryCapacity'] = i['value']
                    if i['code'] == 'WorkStatus':
                        sensor_values['WorkStatus'] = i['value'] 
                    if i['code'] == 'MoisurePowerStatus':
                        sensor_values['MoisurePowerStatus'] = i['value'] 
                    
                    sensors_properties[deviceId] = sensor_values
                
            _LOGGER.warning(sensors_properties)
            return sensors_properties

        except ConfigEntryAuthFailed as exception:
            self._available = False
            _LOGGER.warning("Error retrieving data from Rainpoint api ")
            raise UpdateFailed() from exception
        except Exception as exception:
            raise UpdateFailed() from exception