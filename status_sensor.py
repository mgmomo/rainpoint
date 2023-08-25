import logging
from datetime import datetime

from homeassistant.core import callback

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity
)

"""
from homeassistant.const import (
    UnitOfTemperature,
)
"""

from .api import Rainpoint
from .base_binary_sensor import BaseBinarySensor

_LOGGER = logging.getLogger(__name__)


class StatusSensor(BaseBinarySensor, BinarySensorEntity):
    """
    Representation of a Rainpoint sensor
    """
    def __init__(self, coordinator,  aki_key: str, api_secret: str, deviceId: str, deviceName: str) -> None:
        super().__init__(coordinator, aki_key, api_secret, deviceId, deviceName)
        self._attr_device_class = BinarySensorDeviceClass.RUNNING
        #self._attr_state_class = SensorStateClass.TOTAL
        #self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        #self._attr_unit_of_measurement = UnitOfTemperature.CELSIUS

    @staticmethod
    def entityIdent(s: str) -> str:
        return f'{s}_status'

    @staticmethod
    def entityNaming(s: str) -> str:
        return f'{s} Status'
    
    """
    @property
    def icon(self) -> str:
        return "mdi:thermometer"
    """


    @property
    def _id(self) -> str:
        return StatusSensor.entityIdent(super()._id)
    
    @property
    def name(self) -> str:
        return StatusSensor.entityNaming(super().name)
    

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return StatusSensor.entityIdent(super().unique_id)

    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        if self.coordinator.data[self.deviceId]['WorkStatus'] == "1":
            self._is_on = True
        else:
            self._is_on = False

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
            if self.coordinator.data[self.deviceId]['WorkStatus'] == "1":
                self._is_on = True
            else:
                self._is_on = False
                
            self._attr_extra_state_attributes = {'DeviceID':deviceID}
            self._available = True
            self._updatets = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        except TimeoutError as e:
            self._available = False
            _LOGGER.warning("Error retrieving data from Rainpoint api - Timeout: %s" % e)
        except RuntimeError as e:
            self._available = False
            _LOGGER.exception("Error retrieving data from Rainpoint api - Error: %s" % e)
