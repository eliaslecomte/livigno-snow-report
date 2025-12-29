"""Constants for the Livigno Snow Report integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "livigno_snow_report"

# URLs
SNOW_DATA_URL: Final = "https://www.livigno.eu/en/snow-data"

# Configuration keys
CONF_UPDATE_INTERVAL: Final = "update_interval"

# Update interval options (in minutes)
UPDATE_INTERVAL_OPTIONS: Final = {
    60: "Every hour",
    120: "Every 2 hours",
    180: "Every 3 hours",
    360: "Every 6 hours",
    720: "Every 12 hours",
    1440: "Once a day",
}
DEFAULT_UPDATE_INTERVAL: Final = 120  # 2 hours

# Attribution
ATTRIBUTION: Final = "Data provided by livigno.eu"

# Sensor keys
SENSOR_SNOW_ALTITUDE: Final = "snow_altitude"
SENSOR_SNOW_VILLAGE: Final = "snow_village"
SENSOR_LAST_SNOWFALL_DATE: Final = "last_snowfall_date"
SENSOR_LAST_SNOWFALL_AMOUNT: Final = "last_snowfall_amount"
SENSOR_FRESH_SNOW: Final = "fresh_snow"
SENSOR_CROSS_COUNTRY: Final = "cross_country_skiing"
SENSOR_ALPINE_SKIING: Final = "alpine_skiing"
SENSOR_WINTER_TRAIL: Final = "winter_trail"

# Image keys
IMAGE_PANORAMA: Final = "panorama_webcam"
