"""Sensor platform for e-Distribución."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    POWER_KILO_WATT,
    ENERGY_KILO_WATT_HOUR,
    TIME_DAYS,
    PERCENTAGE,
    CURRENCY_EURO,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSOR_TYPES = {
    "power": ("Potencia", POWER_KILO_WATT),
    "energy_total": ("Contador", ENERGY_KILO_WATT_HOUR),
    "cycle_current": ("Ciclo actual", ENERGY_KILO_WATT_HOUR),
}

class EdistribucionSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._type = sensor_type
        self._attr_name = SENSOR_TYPES[sensor_type][0]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type][1]

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._type)