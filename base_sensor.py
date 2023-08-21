import logging
from abc import ABC
from datetime import datetime

from typing import Any, Optional

import traceback

from .api import Rainpoint

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntity,
    ENTITY_ID_FORMAT
)

from homeassistant.util import slugify

from .const import (
    ATTRS_IRRIGATION_CALL,
    ATTRS_BASEINFORMATION_CALL,
)

_LOGGER = logging.getLogger(__name__)


class BaseSensor(SensorEntity, ABC):
    """
    Representation of a Irrigation sensor
    """

    def _icon(self) -> str:
        return "mdi:valve"

    def __init__(self, api_key: str, api_secret, deviceId: str) -> None:  #: str, deviceId: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.deviceId = deviceId
        self._attr_icon = self._icon()
        self._available: bool = True


    @property
    def icon(self) -> str:
        return self._attr_icon

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.deviceId
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
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
