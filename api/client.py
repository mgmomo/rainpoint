"""Contains the Rainpoint API Client."""


import logging
import tinytuya

from .const import CONF_CATEGORY

logger = logging.getLogger(__name__)

class Rainpoint:
    """Rainpoint client."""

    def __init__(self, api_key, api_secret):
        """Access the Rainpoint Cloud API.
            Args:
                api_key (str): Key used for API Login.
                api_secret (str): Secret for API Login.
        """
        #self.api_key = api_key
        #self.api_secret = api_secret
        self.api_key = '4wnv445jkrxcrc8c4eyx'
        self.api_secret = 'ce639d5ebeb44029b0fdbe593e0c58fc'
        self._api_region = "eu"
        self._cloudsession = None
        self._dummy_device = ""
        logger.info("Init Rainpoint %s" % self._cloudsession)
    
    def login(self) -> bool:
        """
        login with credentials 
        """
        self._cloudsession = tinytuya.Cloud(self._api_region, self.api_key, self.api_secret, self._dummy_device)

        devices = self._cloudsession.getdevices(verbose=True)
        if "Error" in devices:
            return False


        logger.info("Tuya Cloud Login - Success" )

        return True
    
    def devices(self):
        """Returns devices for currently logged in user."""
        devices = self._cloudsession.getdevices(verbose=True)
        if "Error" in devices:
            raise Exception("Authentication error")
        
        deviceList = []
        for item in devices['result']:
            #logger.info(item['name'])
            if item['category'] == CONF_CATEGORY:
                deviceList.append(item["id"])
        
        logger.info("Tuya Cloud Request - found  %s devices" % len(deviceList))

        return deviceList
    
    def sensorValues(self, deviceId):
        """Returns response from 'consumptions' endpoint."""

        return 10