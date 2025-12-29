"""Config flow for Livigno Snow Report integration."""

from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback

from .const import (
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    SNOW_DATA_URL,
    UPDATE_INTERVAL_OPTIONS,
)


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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> LivignoSnowOptionsFlow:
        """Get the options flow for this handler."""
        return LivignoSnowOptionsFlow(config_entry)

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
                    options={CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)},
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=DEFAULT_UPDATE_INTERVAL,
                    ): vol.In(UPDATE_INTERVAL_OPTIONS),
                }
            ),
            errors=errors,
        )


class LivignoSnowOptionsFlow(OptionsFlow):
    """Handle options flow for Livigno Snow Report."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_UPDATE_INTERVAL,
                        default=current_interval,
                    ): vol.In(UPDATE_INTERVAL_OPTIONS),
                }
            ),
        )
