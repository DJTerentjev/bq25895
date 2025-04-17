"""Binary sensor setup for our Integration."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyConfigEntry
from .base import BQ25895Entity
from .coordinator import bq25895Coordinator

__LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Binary Sensors."""
    # This gets the data update coordinator from hass.data as specified in your __init__.py
    # This gets the data update coordinator from the config entry runtime data as specified in your __init__.py
    coordinator: bq25895Coordinator = config_entry.runtime_data.coordinator

    binary_sensors = [
        ChargerEnabledBinarySensor(coordinator),

    ]

    # Create the binary sensors.
    async_add_entities(binary_sensors)


class ChargerEnabledBinarySensor(BQ25895Entity, BinarySensorEntity):
    """charger enabled binary sensor."""

    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charger enabled"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        return self.coordinator.data["charger_enabled"]
