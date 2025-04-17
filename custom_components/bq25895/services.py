import voluptuous as vol


from homeassistant.config_entries import ConfigEntry
#from homeassistant.const import ATTR_DEVICE_ID, ATTR_NAME
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse, callback
from homeassistant.exceptions import HomeAssistantError
#import homeassistant.helpers.device_registry as dr


from .const import DOMAIN
from .coordinator import bq25895Coordinator

from .bq25895.bq25895 import bq25895


#BQ2589X_ICHG_BASE->CHARGE_CURRENT_LIMIT, def=2.048, min=0, max=4.096, step=0.064
#self._bq25895.setCharge_current_limit_mA(tmp)
CHARGE_CURRENT_LIMIT_SCHEMA = vol.Schema(
    {
        vol.Required("charge_current_limit"): vol.All(vol.Coerce(float), vol.Range(min=0, max=4.096)),
    }
)

#BQ2589X_VREG_BASE->CHARGE_VOLTAGE_LIMIT, def=4.208, min=3.840, max=4.608, step=0.016
#self._bq25895.setCharge_voltage_limit_mV(tmp)
CHARGE_VOLTAGE_LIMIT_SCHEMA = vol.Schema(
    {
        vol.Required("charge_voltage_limit"): vol.All(vol.Coerce(float), vol.Range(min=3.840, max=4.608)),
    }
)

#BQ2589X_IINLIM_BASE->INPUT_CURRENT_LIMIT, def=0.5, min=0.1, max=3.250, step=0.05
#self._bq25895.setInput_current_limit_mA(tmp)
INPUT_CURRENT_LIMIT_SCHEMA = vol.Schema(
    {
        vol.Required("input_current_limit"): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=3.250)),
    }
)

#BQ2589X_IPRECHG_BASE->PRECHG_CURRENT, def=0.256, min=0.064, max=1.024, step=0.064
#self._bq25895.setPrechg_current_mA(tmp)
PRECHG_CURRENT_SCHEMA = vol.Schema(
    {
        vol.Required("prechg_current"): vol.All(vol.Coerce(float), vol.Range(min=0.064, max=1.024)),
    }
)

#BQ2589X_VRECHG_MASK->RECHARGE_THRESHOLD, def=100, value=100, value=200
#self._bq25895.setRecharge_threshold_mV(tmp)
RECHARGE_THRESHOLD_SCHEMA = vol.Schema(
    {
        vol.Required("recharge_threshold"): vol.All(int, vol.Any(100, 200))
    }
)



#BQ2589X_TREG_MASK->THERMAL_THRESHOLD, def=120, value=60, value=80, value=100, value=120
#self._bq25895.setThermal_threshold(tmp)
THERMAL_THRESHOLD_SCHEMA = vol.Schema(
    {
        vol.Required("thermal_threshold"): vol.All(int, vol.Any(60, 80, 100, 120))
    }
)

#BQ2589X_ITERM_BASE->TERM_CURRENT, def=0.128, min=0.064, max=1.024, step=0.064
#self._bq25895.setTerm_current_mA(tmp)
TERM_CURRENT_SCHEMA = vol.Schema(
    {
        vol.Required("term_current"): vol.All(vol.Coerce(float), vol.Range(min=0.064, max=1.024)),
    }
)


class BQ25895ServicesSetup:
    """Class to handle Integration Services."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        
        """Initialise services."""
        self.hass = hass
        self.config_entry = config_entry
        self.coordinator: bq25895Coordinator = config_entry.runtime_data.coordinator
        self._bq25895 = bq25895()
        self.setup_services()
        
        #super().__init__(self.coordinator)
        
    def setup_services(self) -> None:
        """Initialise the services in Hass."""
        
        self.hass.services.async_register(
            DOMAIN,
            "enter_ship_mode",
            self.enter_ship_mode,
        )
        self.hass.services.async_register(
            DOMAIN,
            "exit_ship_mode",
            self.exit_ship_mode,
        )

        
        self.hass.services.async_register(
            DOMAIN,
            "set_charge_current_limit",
            self.set_charge_current_limit,
            schema=CHARGE_CURRENT_LIMIT_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "set_charge_voltage_limit",
            self.set_charge_voltage_limit,
            schema=CHARGE_VOLTAGE_LIMIT_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "set_input_current_limit",
            self.set_input_current_limit,
            schema=INPUT_CURRENT_LIMIT_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "set_prechg_current",
            self.set_prechg_current,
            schema=PRECHG_CURRENT_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "set_recharge_threshold",
            self.set_recharge_threshold,
            schema=RECHARGE_THRESHOLD_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "set_term_current",
            self.set_term_current,
            schema=TERM_CURRENT_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "set_thermal_threshold",
            self.set_thermal_threshold,
            schema=THERMAL_THRESHOLD_SCHEMA,
        )


        
        
    async def enter_ship_mode(self, service_call: ServiceCall) -> None:
        self._bq25895.disable_charger()
        await self.coordinator.async_refresh()

    async def exit_ship_mode(self, service_call: ServiceCall) -> None:
        self._bq25895.enable_charger()
        await self.coordinator.async_refresh()

    async def set_charge_current_limit(self, service_call: ServiceCall) -> None:
        tmp = round ((service_call.data["charge_current_limit"])*1000)
        self._bq25895.setCharge_current_limit_mA(tmp)
        await self.coordinator.async_refresh()

    async def set_charge_voltage_limit(self, service_call: ServiceCall) -> None:
        tmp = round ((service_call.data["charge_voltage_limit"])*1000)
        self._bq25895.setCharge_voltage_limit_mV(tmp)
        await self.coordinator.async_refresh()

    async def set_recharge_threshold(self, service_call: ServiceCall) -> None:
        tmp = round (service_call.data["recharge_threshold"])
        self._bq25895.setRecharge_threshold_mV(tmp)
        await self.coordinator.async_refresh()

    async def set_prechg_current(self, service_call: ServiceCall) -> None:
        tmp = round ((service_call.data["prechg_current"])*1000)
        self._bq25895.setPrechg_current_mA(tmp)
        await self.coordinator.async_refresh()

    async def set_term_current(self, service_call: ServiceCall) -> None:
        tmp = round ((service_call.data["term_current"])*1000)
        self._bq25895.setTerm_current_mA(tmp)
        await self.coordinator.async_refresh()

    async def set_thermal_threshold(self, service_call: ServiceCall) -> None:
        tmp = service_call.data["thermal_threshold"]
        self._bq25895.setThermal_threshold(tmp)
        await self.coordinator.async_refresh()

    async def set_input_current_limit(self, service_call: ServiceCall) -> None:
        tmp = round ((service_call.data["input_current_limit"])*1000)
        self._bq25895.setInput_current_limit_mA(tmp)
        await self.coordinator.async_refresh()
