"""Image platform for Livigno Snow Report webcam."""

from __future__ import annotations

from datetime import timedelta
import logging

import aiohttp

from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import (
    ATTRIBUTION,
    DOMAIN,
    IMAGE_PANORAMA,
    PANOMAX_WEBCAM_URL,
)

_LOGGER = logging.getLogger(__name__)

# Panomax updates every few minutes, cache for 5 minutes
WEBCAM_CACHE_DURATION = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Livigno webcam image entity based on a config entry."""
    async_add_entities([LivignoPanoramaImage(hass)])


class LivignoPanoramaImage(ImageEntity):
    """Representation of the Livigno 360° panorama webcam."""

    _attr_has_entity_name = True
    _attr_translation_key = IMAGE_PANORAMA
    _attr_attribution = ATTRIBUTION

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the image entity."""
        super().__init__(hass)
        self._attr_unique_id = f"{DOMAIN}_{IMAGE_PANORAMA}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": "Livigno Snow Report",
            "manufacturer": "Livigno.eu",
            "model": "Snow Data",
            "entry_type": "service",
        }
        self._cached_image: bytes | None = None
        self._last_fetch: dt_util.dt.datetime | None = None

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        now = dt_util.utcnow()

        # Return cached image if still fresh
        if (
            self._cached_image is not None
            and self._last_fetch is not None
            and (now - self._last_fetch) < WEBCAM_CACHE_DURATION
        ):
            return self._cached_image

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    PANOMAX_WEBCAM_URL,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        self._cached_image = await response.read()
                        self._last_fetch = now
                        self._attr_image_last_updated = now
                        return self._cached_image
                    _LOGGER.warning(
                        "Failed to fetch webcam image: HTTP %s", response.status
                    )
        except aiohttp.ClientError as err:
            _LOGGER.warning("Error fetching webcam image: %s", err)

        return self._cached_image
