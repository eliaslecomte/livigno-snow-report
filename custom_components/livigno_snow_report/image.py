"""Image platform for Livigno Snow Report webcam."""

from __future__ import annotations

from datetime import datetime
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
    WEBCAM_PANORAMA_URL,
    WEBCAM_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


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
        self._last_fetch: datetime | None = None

    @property
    def image_url(self) -> str:
        """Return the URL of the image."""
        # Add timestamp to prevent caching
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"{WEBCAM_PANORAMA_URL}?{timestamp}"

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        now = dt_util.utcnow()

        # Return cached image if it's still fresh
        if (
            self._cached_image is not None
            and self._last_fetch is not None
            and (now - self._last_fetch) < WEBCAM_UPDATE_INTERVAL
        ):
            return self._cached_image

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.image_url,
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
