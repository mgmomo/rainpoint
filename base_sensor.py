import logging
#from abc import ABC
from homeassistant.core import callback
from homeassistant.util import slugify

from datetime import datetime

from typing import Any, Optional

import traceback

from .api import Rainpoint

from homeassistant.components.sensor import (
    SensorEntity,
    ENTITY_ID_FORMAT
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)


from .const import (
    DOMAIN,
    CONF_CATEGORY
)

_LOGGER = logging.getLogger(__name__)


class BaseSensor(CoordinatorEntity, SensorEntity): 
    """
    Representation of a Irrigation sensor
    """

    def _icon(self) -> str:
        return "mdi:valve"

    def __init__(self, coordinator, api_key: str, api_secret, deviceId: str, deviceName: str) -> None:  
        super().__init__(coordinator)
        _LOGGER.warning("Base sensor device name  %s" % deviceName)
        self.coordinator = coordinator
        self.api_key = api_key
        self.api_secret = api_secret
        self.deviceId = deviceId
        self.deviceName = deviceName

        self._attr_native_value = int
        self._attr_extra_state_attributes = {}
        self._attr_name = deviceName
        self._attr_icon = self._icon()
    
        
        self.attrs: dict[str, Any] = {}
        self._name: str = deviceName
        self._state: int | str | None = None
        self._available: bool = True
        self._updatets: str | None = None
        
        _LOGGER.debug("Base sensor initialisation %s" % deviceId)

    @property
    def _id(self):
        return ENTITY_ID_FORMAT.format(slugify(self._name).lower())
    
    @property
    def icon(self) -> str :
        return self._attr_icon 
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        if "label" in self._attr_extra_state_attributes:
            return self._attr_extra_state_attributes["label"]
        return self._name
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.deviceId
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:  # pylint: disable=overridden-final-method
        return self._state

    @property
    def device_info(self) -> dict[str, Any]:
        """Return the device_info."""
        _LOGGER.warning("Device Info coordinator data %s" % self.coordinator.data)

        return {
            "name": self.deviceName,
            "identifiers": { (DOMAIN, self.deviceId) },
            "model": CONF_CATEGORY,
            "manufacturer": "Rainpoint",
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        #self._attr_is_on = self.coordinator.data[self.idx]["state"]
        _LOGGER.info("Base Sensor - Update Callback")
        self.async_write_ha_state()

    @staticmethod
    def is_active() -> bool:
        """
        returns active status of rainpoint sensor
        """
        return self._available

    async def get_deviceId(self, rainpoint: Rainpoint) -> dict[str]:
        """
        asynchronously get and parse / deviceID response
        """
        devices = await self.hass.async_add_executor_job(rainpoint.devices)
        if devices is None or len(devices) == 0:
            raise RuntimeError(f"Cannot access Zaehlpunkt {self.deviceId}")
        deviceList = [
            z for z in devices if z == self.deviceId
        ]
        _LOGGER.info("Rainpoint get device ids: %s" % deviceList)
        
        if len(deviceList) == 0:
            raise RuntimeError(f"Rainpoint Device {self.deviceId} not found")
        else:
            return (
                deviceList
                if len(deviceList) > 0
                else None
            )

    @staticmethod
    async def async_update(self):
        """
        update sensor
        """
        pass


