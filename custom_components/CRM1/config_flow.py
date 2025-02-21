from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.typing import DiscoveryInfoType
import voluptuous as vol

from .const import DOMAIN

class EdistribucionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="e-Distribución", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("gecko_driver_path"): str,
                vol.Required("firefox_binary_path"): str
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EdistribucionOptionsFlowHandler(config_entry)

class EdistribucionOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("update_interval", default=30): int  # Intervalo de actualización en minutos
            })
        )