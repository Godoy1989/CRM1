"""Config flow for e-Distribución."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .eds.connector import EdsConnector
from .const import DOMAIN

class EdistribucionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for e-Distribución."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            try:
                eds_connector = EdsConnector(username, password)
                await self.hass.async_add_executor_job(eds_connector.login)
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "invalid_auth"

            if not errors:
                return self.async_create_entry(title=username, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )