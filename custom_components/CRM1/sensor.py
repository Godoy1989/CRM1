from homeassistant.components.sensor import SensorEntity
from homeassistant.const import POWER_KILO_WATT
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import asyncio
import logging
from datetime import timedelta

from .api import EdistribucionAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    username = entry.data["username"]
    password = entry.data["password"]
    gecko_driver_path = entry.data["gecko_driver_path"]
    firefox_binary_path = entry.data["firefox_binary_path"]

    update_interval = timedelta(minutes=entry.options.get("update_interval", 30))

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="e-Distribución",
        update_method=lambda: EdistribucionAPI(username, password, gecko_driver_path, firefox_binary_path).get_instant_power(),
        update_interval=update_interval
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([EdistribucionSensor(coordinator)], True)

class EdistribucionSensor(SensorEntity):
    def __init__(self, coordinator):
        self._attr_name = "e-Distribución Potencia Instantánea"
        self._attr_unique_id = "edistribucion_instant_power"
        self._attr_native_unit_of_measurement = POWER_KILO_WATT
        self._attr_icon = "mdi:flash"
        self.coordinator = coordinator

    @property
    def native_value(self):
        return self.coordinator.data

    async def async_update(self):
        await self.coordinator.async_request_refresh()