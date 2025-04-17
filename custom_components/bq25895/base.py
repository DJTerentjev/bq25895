"""Base entity which all other entity platform classes can inherit.

As all entity types have a common set of properties, you can
create a base entity like this and inherit it in all your entity platforms.

This just makes your code more efficient and is totally optional.

See each entity platform (ie sensor.py, switch.py) for how this is inheritted
and what additional properties and methods you need to add for each entity type.

"""

import logging
from typing import Any

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import bq25895Coordinator

_LOGGER = logging.getLogger(__name__)


class BQ25895Entity(CoordinatorEntity):
    """BQ25895 base entity."""

#    coordinator: bq25895Coordinator = config_entry.runtime_data.coordinator
    coordinator: bq25895Coordinator
    _attr_has_entity_name = True

    def __init__(self, coordinator: bq25895Coordinator) -> None:
        """Initialise entity."""
        #self._coordinator = coordinator
        super().__init__(coordinator)
#        self._device_id = coordinator.id_prefix
        _LOGGER.debug("Coordinator name: %s", coordinator.name)
        self._attr_device_info = DeviceInfo(
            identifiers = {(DOMAIN, DOMAIN)},
            name = DOMAIN,  #coordinator.name,
            manufacturer = "Texas Instruments",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        # This method is called by your DataUpdateCoordinator when a successful update runs.
        self.async_write_ha_state()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name.replace("_", " ").title()

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return self._name

    async def async_update(self):
        await self.coordinator.async_request_refresh()
