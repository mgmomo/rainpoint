import logging
from datetime import datetime

from homeassistant.core import callback

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass
)

from .api import Rainpoint
from .base_sensor import BaseSensor

_LOGGER = logging.getLogger(__name__)


class LiveSensor(BaseSensor, SensorEntity):
    """
    Representation of a Wiener Smartmeter sensor
    for measuring total increasing energy consumption for a specific zaehlpunkt
    """


    def __init__(self, coordinator,  aki_key: str, api_secret: str, deviceId: str) -> None:
        super().__init__(coordinator, aki_key, api_secret, deviceId)
        self._attr_device_class = SensorDeviceClass.VOLUME

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        #self._attr_is_on = self.coordinator.data[self.idx]["state"]
        _LOGGER.info("Live Sensor - Update Callback")
        self.async_write_ha_state()


    async def async_update(self):
        """
        update sensor
        """
        
        try:
            
            rainpoint = Rainpoint(self.api_key, self.api_secret)
            await self.hass.async_add_executor_job(rainpoint.login)
            
            deviceID = await self.get_deviceId(rainpoint)
            
            self._attr_extra_state_attributes = {'DeviceID':deviceID}
            """
            if self.is_active():
                values = await self.get_consumptions(rainpoint, deviceID)

                
                base_information = await self.get_base_information(smartmeter)
                meter_readings = await self.get_meter_readings(smartmeter)
                # if zaehlpunkt is coincidentally the one returned by /welcome
                if (
                        "zaehlpunkt" in base_information
                        and base_information["zaehlpunkt"] == self.zaehlpunkt
                        and "lastValue" in meter_readings
                ):
                    if (
                            meter_readings["lastValue"] is None
                            or self._state != meter_readings["lastValue"]
                    ):
                        self._state = meter_readings["lastValue"] / 1000
                else:
                    # if not, we'll have to guesstimate (because api is shitty-pom-fritty)
                    # for that zaehlpunkt
                    yesterdays_consumption = await self.get_daily_consumption(
                        smartmeter, before(today())
                    )
                    if (
                            "values" in yesterdays_consumption
                            and "statistics" in yesterdays_consumption
                    ):
                        avg = yesterdays_consumption["statistics"]["average"]
                        yesterdays_sum = sum(
                            (
                                y["value"] if y["value"] is not None else avg
                                for y in yesterdays_consumption["values"]
                            )
                        )
                        if yesterdays_sum > 0:
                            self._state = yesterdays_sum
                    else:
                        _LOGGER.error("Unable to load consumption")
                        _LOGGER.error(
                            "Please file an issue with this error and \
                            (anonymized) payload in github %s %s %s %s",
                            base_information,
                            consumptions,
                            meter_readings,
                            yesterdays_consumption,
                        )
                        return """
            self._available = True
            self._updatets = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        except TimeoutError as e:
            self._available = False
            _LOGGER.warning("Error retrieving data from smart meter api - Timeout: %s" % e)
        except RuntimeError as e:
            self._available = False
            _LOGGER.exception("Error retrieving data from smart meter api - Error: %s" % e)
