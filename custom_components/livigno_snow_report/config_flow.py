"""Config flow for Livigno Snow Report integration."""

from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, SNOW_DATA_URL


async def validate_connection(hass: HomeAssistant) -> bool:
    """Validate that we can connect to the Livigno website."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SNOW_DATA_URL,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                return response.status == 200
    except aiohttp.ClientError:
        return False


class LivignoSnowConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Livigno Snow Report."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        # Check if already configured
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            # Validate connection
            if await validate_connection(self.hass):
                return self.async_create_entry(
                    title="Livigno Snow Report",
                    data={},
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            errors=errors,
        )
