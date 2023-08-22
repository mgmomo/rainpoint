"""Setup Rainpoint component."""
from datetime import timedelta
from typing import Any
import logging
from .const import CONF_COORDINATOR
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
    """Class to manage fetching data from the Vienna Smartmeter API."""

    def __init__(self, hass, entry) -> None:
        """Initialize."""
        _LOGGER.warning("Initialize Rainpoint update coordinator")
        
        scan_interval = timedelta(seconds=30)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)
        self.entry_data  = hass.data[DOMAIN][entry.entry_id]

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            _LOGGER.warning("Refreshing Rainpoint update coordinator %s " % self.entry_data)
            rainpoint = Rainpoint(self.entry_data['api_key'], self.entry_data['api_secret'])
            return await self.hass.async_add_executor_job(rainpoint.login)

            #await self.client.refresh_token()
            #return True
        except ConfigEntryAuthFailed as exception:
            self._available = False
            _LOGGER.warning("Error retrieving data from smart meter api ")
            raise UpdateFailed() from exception
        except Exception as exception:
            raise UpdateFailed() from exception