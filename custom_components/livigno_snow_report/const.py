"""Constants for the Livigno Snow Report integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "livigno_snow_report"

# URLs
SNOW_DATA_URL: Final = "https://www.livigno.eu/en/snow-data"
WEBCAM_PANORAMA_URL: Final = "https://webcam.livigno.eu/livigno-pano/1300.jpg"

# Update interval
UPDATE_INTERVAL: Final = timedelta(minutes=30)
WEBCAM_UPDATE_INTERVAL: Final = timedelta(minutes=5)

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
