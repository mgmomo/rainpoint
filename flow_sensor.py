import logging
from datetime import datetime

from homeassistant.core import callback

from homeassistant.const import VOLUME_LITERS

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

from .api import Rainpoint
from .base_sensor import BaseSensor

_LOGGER = logging.getLogger(__name__)


class FlowSensor(BaseSensor, SensorEntity):
    """
    Representation of a Rainpoint sensor
    """

    @staticmethod
    def entityIdent(s: str) -> str:
        return f'{s}_flow'
    
    @staticmethod
    def entityNaming(s: str) -> str:
        return f'{s} Flow'
    
    def __init__(self, coordinator,  aki_key: str, api_secret: str, deviceId: str, deviceName: str) -> None:
        super().__init__(coordinator, aki_key, api_secret, deviceId, deviceName)
        self._attr_device_class = SensorDeviceClass.WATER 
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = VOLUME_LITERS
        self._attr_unit_of_measurement = VOLUME_LITERS

    @property
    def icon(self) -> str:
        return "mdi:waves-arrow-right"
    
    @property
    def _id(self) -> str:
        return FlowSensor.entityIdent(super()._id)
    
    @property
    def name(self) -> str:
        return FlowSensor.entityNaming(super().name)
    

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return FlowSensor.entityIdent(super().unique_id)
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        self._state = self.coordinator.data[self.deviceId]['Flow']
        self._available = True
        self._updatets = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.async_write_ha_state()


    async def async_update(self):
        """
        update sensor
        """
        try:
            
            rainpoint = Rainpoint(self.api_key, self.api_secret)
            await self.hass.async_add_executor_job(rainpoint.login)
            deviceID = await self.get_deviceId(rainpoint)
            """ initial Update"""
            self._state = self.coordinator.data[self.deviceId]['Flow']
            self._attr_extra_state_attributes = {'DeviceID':deviceID}
            self._available = True
            self._updatets = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        except TimeoutError as e:
            self._available = False
            _LOGGER.warning("Error retrieving data from Rainpoint api - Timeout: %s" % e)
        except RuntimeError as e:
            self._available = False
            _LOGGER.exception("Error retrieving data from Rainpoint api - Error: %s" % e)
