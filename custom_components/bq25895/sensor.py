"""Sensor setup for our Integration.

Here we use a different method to define some of our entity classes.
As, in our example, so much is common, we use our base entity class to define
many properties, then our base sensor class to define the property to get the
value of the sensor.

As such, for all our other sensor types, we can just set the _attr_ value to
keep our code small and easily readable.  You can do this for all entity properties(attributes)
if you so wish, or mix and match to suit.
"""

from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyConfigEntry
from .base import BQ25895Entity
from .coordinator import bq25895Coordinator
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    #UnitOfEnergy,
    #UnitOfPower,
    #UnitOfTime,
    UnitOfTemperature,
)

_LOGGER = logging.getLogger(__name__)




async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Sensors."""
    # This gets the data update coordinator from the config entry runtime data as specified in your __init__.py
    coordinator: bq25895Coordinator = config_entry.runtime_data.coordinator

    sensors = [
        #VoltageSensor(coordinator),
        #CurrentSensor(coordinator),
        #PowerSensor(coordinator),
        #SocSensor(coordinator),
        #RemainingCapacitySensor(coordinator),
        #RemainingTimeSensor(coordinator),
        # My
        MinBattteryVoltageSensor(coordinator),
        BusVoltageSensor(coordinator),
        ChargingStatusSensor(coordinator),
        BatteryVoltageSensor (coordinator),
        ChargeCurrentSensor (coordinator),
        ChargeCurrentLimitSensor (coordinator),
        ChargeVoltageLimitSensor (coordinator),
        InputCurrenLimitSensor (coordinator),
        PrechgCurrentSensor (coordinator),
        TermCurrentSensor (coordinator),
        RechargeThresholdSensor (coordinator),
        BatteryFaultSensor (coordinator),
        ChargeFaultSensor (coordinator),
        NtcFaultSensor (coordinator),
        TemperatureSensor (coordinator),
        ThermalThresholdSensor (coordinator),
    ]

    async_add_entities(sensors)


#class BQ25895Sensor(BQ25895Entity, SensorEntity):
#    """Base sensor."""
#
#    def __init__(self, coordinator: bq25895Coordinator) -> None:
#        super().__init__(coordinator)
#        
#        
#        
class MinBattteryVoltageSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Min Batttery Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.VOLTAGE

    @property
    def native_value(self):
        return self.coordinator.data["min_batttery_voltage"]

class BusVoltageSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Bus Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.VOLTAGE

    @property
    def native_value(self):
        return self.coordinator.data["bus_voltage"]

class ChargingStatusSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charging status"
        self._attr_device_class = SensorDeviceClass.ENUM

    @property
    def native_value(self):
        return self.coordinator.data["charging_status"]

class BatteryVoltageSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Battery voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.VOLTAGE

    @property
    def native_value(self):
        return self.coordinator.data["battery_voltage"]

class ChargeCurrentSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charge current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def native_value(self):
        return self.coordinator.data["charge_current"]

class ChargeCurrentLimitSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charge current limit"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def native_value(self):
        return self.coordinator.data["charge_current_limit"]

class ChargeVoltageLimitSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charge voltage limit"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.VOLTAGE

    @property
    def native_value(self):
        return self.coordinator.data["charge_voltage_limit"]

class InputCurrenLimitSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Input curren limit"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def native_value(self):
        return self.coordinator.data["input_curren_limit"]
        
class PrechgCurrentSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Prechg current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def native_value(self):
        return self.coordinator.data["prechg_current"]
        
class TermCurrentSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Term current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_suggested_display_precision = 3
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def native_value(self):
        return self.coordinator.data["term_current"]

class RechargeThresholdSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Recharge threshold"
        self._attr_native_unit_of_measurement = "mV" #UnitOfElectricCurrent.MILLIVOLT
        self._attr_suggested_display_precision = 0
        self._attr_device_class = SensorDeviceClass.VOLTAGE

    @property
    def native_value(self):
        return self.coordinator.data["recharge_threshold"]

class BatteryFaultSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Battery fault"
        self._attr_device_class = SensorDeviceClass.ENUM
        

    @property
    def native_value(self):
        return self.coordinator.data["battery_fault"]

class ChargeFaultSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charge fault"
        self._attr_device_class = SensorDeviceClass.ENUM

    @property
    def native_value(self):
        return self.coordinator.data["charge_fault"]

class NtcFaultSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "NTC fault"
        self._attr_device_class = SensorDeviceClass.ENUM

    @property
    def native_value(self):
        return self.coordinator.data["ntc_fault"]

class TemperatureSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_suggested_display_precision = 1
        self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def native_value(self):
        return self.coordinator.data["temperature"]

class ThermalThresholdSensor(BQ25895Entity, SensorEntity):
    def __init__(self, coordinator: bq25895Coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Thermal threshold"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_suggested_display_precision = 0
        self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def native_value(self):
        return self.coordinator.data["thermal_threshold"]
