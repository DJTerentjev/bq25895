"""DataUpdateCoordinator for our integration."""

import logging
from typing import Any 
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_SCAN_INTERVAL,
)

from .const import (
    DOMAIN,

    CONF_ADDR,
    CONF_BUS,
    CONF_MIN_BATTERY_VOLTAGE,
    CONF_CHARGE_CURRENT_LIMIT,
    CONF_CHARGE_VOLTAGE_LIMIT,
    CONF_INPUT_CURRENT_LIMIT,
    CONF_PRECHG_CURRENT,
    CONF_RECHARGE_THRESHOLD,
    CONF_TERM_CURRENT,
    CONF_THERMAL_THRESHOLD,

    DEFAULT_SCAN_INTERVAL,
    DEFAULT_CHARGE_CURRENT_LIMIT,
    DEFAULT_CHARGE_VOLTAGE_LIMIT,
    DEFAULT_INPUT_CURRENT_LIMIT,
    DEFAULT_PRECHG_CURRENT,
    DEFAULT_RECHARGE_THRESHOLD,
    DEFAULT_TERM_CURRENT,
    DEFAULT_THERMAL_THRESHOLD,
)

from homeassistant.core import DOMAIN, HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed


from .bq25895.bq25895 import bq25895

_LOGGER = logging.getLogger(__name__)

class bq25895Coordinator(DataUpdateCoordinator):
    """bq25895 coordinator."""

    data: list[dict[str, Any]]

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize coordinator."""
        self.name = config_entry.unique_id
        # Register an update listener to handle option changes
        config_entry.async_on_unload(config_entry.add_update_listener(self.update_listener))
        
        # Set variables from values entered in config flow setup
        self._addr_str = config_entry.data[CONF_ADDR]
        self._addr = int(config_entry.data[CONF_ADDR], 16) 
        self._bus = int(config_entry.data[CONF_BUS])
        self._MinBatteryVoltage = float(config_entry.data[CONF_MIN_BATTERY_VOLTAGE])
        # set variables from options.  You need a default here in case options have not been set
        self.poll_interval = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        self._recharge_threshold = int(config_entry.options.get(
            CONF_RECHARGE_THRESHOLD, DEFAULT_RECHARGE_THRESHOLD
        ))
        self._thermal_threshold = int(config_entry.options.get(
            CONF_THERMAL_THRESHOLD, DEFAULT_THERMAL_THRESHOLD
        ))
        self._charge_current_limit = float(config_entry.options.get(
            CONF_CHARGE_CURRENT_LIMIT, DEFAULT_CHARGE_CURRENT_LIMIT
        ))
        self._charge_voltage_limit = float(config_entry.options.get(
            CONF_CHARGE_VOLTAGE_LIMIT, DEFAULT_CHARGE_VOLTAGE_LIMIT
        ))
        self._input_current_limit = float(config_entry.options.get(
            CONF_INPUT_CURRENT_LIMIT, DEFAULT_INPUT_CURRENT_LIMIT
        ))
        self._prechg_current = float(config_entry.options.get(
            CONF_PRECHG_CURRENT, DEFAULT_PRECHG_CURRENT
        ))
        self._term_current = float(config_entry.options.get(
            CONF_TERM_CURRENT, DEFAULT_TERM_CURRENT
        ))



        # Initialise I2C device bq25895
        self.device_setup () #hass, config_entry 
        # Initialise DataUpdateCoordinator
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            # Method to call on every update interval.
            update_method=self.async_update_data,
            # Polling interval.
            update_interval=timedelta(seconds=self.poll_interval),
        )



            
    def device_setup(self) -> None: #, hass: HomeAssistant, config_entry: ConfigEntry
        """Apply user options to device bq25895."""

        # Initialise I2C device bq25895
        _LOGGER.debug("Initialise: %s", self.name)
        self._bq25895 = bq25895(i2c_bus=self._bus, addr=self._addr)
        # Apply initial options to device bq25895

        try:
            self._bq25895.reset_chip()
            self._bq25895.adc_stop()
            self._bq25895.adc_start(0)
            self._bq25895.disable_watchdog()
            self._bq25895.setRecharge_threshold_mV(self._recharge_threshold)
            self._bq25895.setThermal_threshold(self._thermal_threshold)
            self._bq25895.setCharge_current_limit_mA(round(1000* self._charge_current_limit))
            self._bq25895.setCharge_voltage_limit_mV(round(1000* self._charge_voltage_limit))
            self._bq25895.setInput_current_limit_mA(round(1000* self._input_current_limit))
            self._bq25895.setPrechg_current_mA(round(1000* self._prechg_current))
            self._bq25895.setTerm_current_mA(round(1000* self._term_current))
            _LOGGER.debug("%s options updated!", self.name)
        except IOError as err:
            raise UpdateFailed(f"Error communicating with I2C: Bus:{self._bus}, Address:{self._addr_str} !") from err
        except Exception as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err
    
    async def update_listener(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Handle options updates and apply it to device bq25895."""
        #_LOGGER.warning("Option updated!")
        #_LOGGER.error("Options updated!")
        #self.device_setup (hass, config_entry)
        pass
        
        
    async def async_update_data(self):
        """Fetch data from device bq25895."""
        # Get data from device bq25895
        try:
            is_watchdog_enabled = self._bq25895.is_watchdog_enabled()
            # If watchdog_enabled (bq25895 was reset) re-initialise I2C device bq25895
            if is_watchdog_enabled:
                self.device_setup ()
            bus_voltage = self._bq25895.getBus_voltage_mV()#My
            charging_status = self._bq25895.getCharging_status()#My
            battery_voltage = self._bq25895.getBattery_voltage_mV()#My
            charge_current = self._bq25895.getCharge_current_mA()#My
            charge_current_limit = self._bq25895.getCharge_current_limit_mA()#My
            charge_voltage_limit = self._bq25895.getCharge_voltage_limit_mV()
            input_curren_limit = self._bq25895.getInput_current_limit_mA()
            prechg_current = self._bq25895.getPrechg_current_mA()
            term_current = self._bq25895.getTerm_current_mA()
            recharge_threshold = self._bq25895.getRecharge_threshold_mV()
            battery_fault = self._bq25895.getFault_status(3)
            charge_fault = self._bq25895.getFault_status(4)
            ntc_fault = self._bq25895.getFault_status(0)
            temperature = self._bq25895.getTemperature()
            thermal_threshold = self._bq25895.getThermal_threshold()
            charger_enabled = self._bq25895.is_charger_enabled()
            
            my_test = self._bq25895.getMin_system_voltage_mV()

        except IOError as err:
            raise UpdateFailed(f"Error communicating with bq25895: Bus:{self._bus}, Address:{self._addr_str} !") from err
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
            
            

        # What is returned here is stored in self.data by the DataUpdateCoordinator
        data ={
            "min_batttery_voltage": self._MinBatteryVoltage, #my_test, #self.hass.states.get("sensor.bq25895_charge_voltage_limit").state, #
            "bus_voltage": round (bus_voltage/1000, 3), # My
            "charging_status": charging_status,
            "battery_voltage": round (battery_voltage/1000, 3),
            "charge_current" : round (charge_current/1000, 3),
            "charge_current_limit" : round (charge_current_limit/1000, 3),
            "charge_voltage_limit" : round (charge_voltage_limit/1000, 3),
            "input_curren_limit" : round (input_curren_limit/1000, 3),
            "prechg_current" : round (prechg_current/1000, 3),
            "term_current" :  round (term_current/1000, 3),
            "recharge_threshold" : round (recharge_threshold),
            "battery_fault" : round (battery_fault),
            "charge_fault" : round (charge_fault),
            "ntc_fault" : round (ntc_fault),
            "temperature": round (temperature, 1),
            "thermal_threshold": round (thermal_threshold),
            "charger_enabled" : charger_enabled,
            "charge": charger_enabled,
              }
        return data


