"""Constants for rainpoint."""
# Base component constants
NAME = "Rainpoint irrigation"
DOMAIN = "rainpoint"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.2"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_API_KEY = "api_key"
CONF_API_SECRET = "api_secret"


CONF_DEVICES = "tuya_devices"




ATTRS_IRRIGATION_CALL = [
    ("zaehlpunktnummer", "zaehlpunktnummer"),
    ("customLabel", "label"),
]


ATTRS_BASEINFORMATION_CALL = [
    ("deviceId", "deviceId"),
]

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
A custom, unofficial integration to access Rainpoint Cloud Values.

-------------------------------------------------------------------
"""