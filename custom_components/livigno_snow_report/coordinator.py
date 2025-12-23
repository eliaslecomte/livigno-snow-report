"""DataUpdateCoordinator for Livigno Snow Report."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import date
from typing import Any

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    SENSOR_ALPINE_SKIING,
    SENSOR_CROSS_COUNTRY,
    SENSOR_FRESH_SNOW,
    SENSOR_LAST_SNOWFALL_AMOUNT,
    SENSOR_LAST_SNOWFALL_DATE,
    SENSOR_SNOW_ALTITUDE,
    SENSOR_SNOW_VILLAGE,
    SENSOR_WINTER_TRAIL,
    SNOW_DATA_URL,
    UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class LivignoSnowData:
    """Data class for Livigno snow report data."""

    snow_altitude: float | None = None
    snow_village: float | None = None
    last_snowfall_date: date | None = None
    last_snowfall_amount: float | None = None
    fresh_snow: float | None = None
    cross_country_skiing: float | None = None
    alpine_skiing: float | None = None
    winter_trail: float | None = None


class LivignoSnowCoordinator(DataUpdateCoordinator[LivignoSnowData]):
    """Coordinator to fetch Livigno snow data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self._session: aiohttp.ClientSession | None = None

    async def _async_update_data(self) -> LivignoSnowData:
        """Fetch data from the Livigno snow data page."""
        try:
            if self._session is None:
                self._session = aiohttp.ClientSession()

            async with self._session.get(SNOW_DATA_URL, timeout=aiohttp.ClientTimeout(total=30)) as response:
                response.raise_for_status()
                html = await response.text()

            return self._parse_snow_data(html)

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching data from {SNOW_DATA_URL}: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Error parsing snow data: {err}") from err

    def _parse_snow_data(self, html: str) -> LivignoSnowData:
        """Parse the HTML and extract snow data."""
        soup = BeautifulSoup(html, "lxml")
        data = LivignoSnowData()

        rows = soup.find_all("div", class_="snow-data-row")

        for row in rows:
            label_elem = row.find("p", class_="label")
            data_elem = row.find("p", class_="data")

            if not label_elem or not data_elem:
                continue

            label = label_elem.get_text(strip=True).lower()
            value = data_elem.get_text(strip=True)

            if "snow in altitude" in label:
                data.snow_altitude = self._parse_cm_value(value)
            elif "snow in the village" in label:
                data.snow_village = self._parse_cm_value(value)
            elif "last snowfall" in label:
                data.last_snowfall_date = self._parse_date_from_label(label_elem.get_text(strip=True))
                data.last_snowfall_amount = self._parse_cm_value(value)
            elif "fresh snow" in label:
                data.fresh_snow = self._parse_cm_value(value)
            elif "cross-country" in label:
                data.cross_country_skiing = self._parse_km_value(value)
            elif "alpine skiing" in label:
                data.alpine_skiing = self._parse_km_value(value)
            elif "winter trail" in label:
                data.winter_trail = self._parse_km_value(value)

        _LOGGER.debug("Parsed Livigno snow data: %s", data)
        return data

    def _parse_cm_value(self, value: str) -> float | None:
        """Parse a cm value like '45 cm' to float."""
        match = re.search(r"([\d,\.]+)\s*cm", value, re.IGNORECASE)
        if match:
            num_str = match.group(1).replace(",", ".")
            try:
                return float(num_str)
            except ValueError:
                return None
        return None

    def _parse_km_value(self, value: str) -> float | None:
        """Parse a km value like '98 km' or '5,5' to float."""
        # First try to match with 'km' suffix
        match = re.search(r"([\d,\.]+)\s*km?", value, re.IGNORECASE)
        if match:
            num_str = match.group(1).replace(",", ".")
            try:
                return float(num_str)
            except ValueError:
                return None
        # Try to match just a number (for values like "5,5")
        match = re.search(r"([\d,\.]+)", value)
        if match:
            num_str = match.group(1).replace(",", ".")
            try:
                return float(num_str)
            except ValueError:
                return None
        return None

    def _parse_date_from_label(self, label: str) -> date | None:
        """Parse date from label like 'Last snowfall 17.12.2025'."""
        match = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", label)
        if match:
            try:
                day = int(match.group(1))
                month = int(match.group(2))
                year = int(match.group(3))
                return date(year, month, day)
            except ValueError:
                return None
        return None

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator and close the session."""
        if self._session:
            await self._session.close()
            self._session = None
