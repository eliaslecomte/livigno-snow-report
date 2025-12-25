"""Image platform for Livigno Snow Report webcam."""

from __future__ import annotations

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
)
from .coordinator import LivignoSnowCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Livigno webcam image entity based on a config entry."""
    coordinator: LivignoSnowCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LivignoPanoramaImage(hass, coordinator)])


class LivignoPanoramaImage(ImageEntity):
    """Representation of the Livigno 360° panorama webcam."""

    _attr_has_entity_name = True
    _attr_translation_key = IMAGE_PANORAMA
    _attr_attribution = ATTRIBUTION

    def __init__(self, hass: HomeAssistant, coordinator: LivignoSnowCoordinator) -> None:
        """Initialize the image entity."""
        super().__init__(hass)
        self._coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{IMAGE_PANORAMA}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": "Livigno Snow Report",
            "manufacturer": "Livigno.eu",
            "model": "Snow Data",
            "entry_type": "service",
        }
        self._cached_image: bytes | None = None
        self._cached_url: str | None = None

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        webcam_url = self._coordinator.data.webcam_panorama_url if self._coordinator.data else None

        if not webcam_url:
            _LOGGER.warning("No webcam URL available from coordinator")
            return self._cached_image

        # Only fetch if URL changed (new image available)
        if webcam_url == self._cached_url and self._cached_image is not None:
            return self._cached_image

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    webcam_url,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        self._cached_image = await response.read()
                        self._cached_url = webcam_url
                        self._attr_image_last_updated = dt_util.utcnow()
                        return self._cached_image
                    _LOGGER.warning(
                        "Failed to fetch webcam image: HTTP %s", response.status
                    )
        except aiohttp.ClientError as err:
            _LOGGER.warning("Error fetching webcam image: %s", err)

        return self._cached_image
