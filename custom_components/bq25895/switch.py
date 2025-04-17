
import logging

import logging
from typing import Any

import logging
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyConfigEntry
from .base import BQ25895Entity
from .coordinator import bq25895Coordinator

from .bq25895.bq25895 import bq25895

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Binary Switch."""

    coordinator: bq25895Coordinator = config_entry.runtime_data.coordinator
    
    switches = [
        ChargeSwitch(coordinator), #device, "state")
    ]
    async_add_entities(switches)

class ChargeSwitch(BQ25895Entity, SwitchEntity):

    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charge"
        self._attr_device_class =  SwitchDeviceClass.SWITCH
        self._bq25895 = bq25895()
        self._attr_available = True
        #self._CoordinatorEntity = coordinator
        #return self._coordinator.data["online"]

    @property
    def is_on(self) -> bool | None:
        """Return if the binary sensor is on."""
        #self.attr_available = True
        return self.coordinator.data["charge"]


    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        try:
            self._bq25895.enable_charger()
            #self._attr_available = True
        except Exception as e:
            pass
            #self._attr_available = False
            #self.debug(f"Can't update: {e}")
            #self._attr_available = False
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        try:
            self._bq25895.disable_charger()
            #self._attr_available = True
        except Exception as e:
            pass
            #self._attr_available = False
            #self.debug(f"Can't update: {e}")
            #self._attr_available = False
        await self.coordinator.async_refresh()
