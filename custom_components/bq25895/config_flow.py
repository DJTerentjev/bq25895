"""Config flows for our integration."""
# Base on the code from:
# https://github.com/msp1974/HAIntegrationExamples/blob/main/msp_integration_101_intermediate/

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import (
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import selector


from .bq25895.bq25895 import bq25895
from .coordinator import bq25895Coordinator
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
    
    DEFAULT_ADDR,
    DEFAULT_BUS,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_MIN_BATTERY_VOLTAGE,
    DEFAULT_CHARGE_CURRENT_LIMIT,
    DEFAULT_CHARGE_VOLTAGE_LIMIT,
    DEFAULT_INPUT_CURRENT_LIMIT,
    DEFAULT_PRECHG_CURRENT,
    DEFAULT_RECHARGE_THRESHOLD,
    DEFAULT_TERM_CURRENT,
    DEFAULT_THERMAL_THRESHOLD,
)
_LOGGER = logging.getLogger(__name__)


def step_user_data_schema(data: dict[str, Any] = {CONF_ADDR: DEFAULT_ADDR, CONF_BUS: DEFAULT_BUS, CONF_MIN_BATTERY_VOLTAGE: DEFAULT_MIN_BATTERY_VOLTAGE}) -> Schema:
    """Form STEP_USER_DATA_SCHEMA"""
    _LOGGER.debug(f'config_flow.py:step_user_data_schema: {data}')

    STEP_USER_DATA_SCHEMA = vol.Schema(
        {
            vol.Required(CONF_ADDR, default = data.get(CONF_ADDR)): selector(
                {
                    "select": {
                        "options": ["0x6A", "0x6B"],
                        "mode": "dropdown",
                    }
                }
            ),
            vol.Required(CONF_BUS, default = data.get(CONF_BUS)): selector(
                {
                    "select": {
                        "options": ["1", "2"],
                        "mode": "dropdown",
                    }
                }
            ),
            vol.Required(CONF_MIN_BATTERY_VOLTAGE, default = str(data.get(CONF_MIN_BATTERY_VOLTAGE))): selector(
                                {
                                "number": {
                                    "min": 2.5,
                                    "max": 3.5,
                                    "step": 0.1,
                                    "unit_of_measurement": "V",
                                    "mode": "slider",
                                    }
                                }
                        ),
        }
    )
    return STEP_USER_DATA_SCHEMA


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    try:
        _addr = int(data[CONF_ADDR], 16)
        _bus = int(data[CONF_BUS])
        # Initialise I2C device bq25895
        _bq25895 = bq25895(i2c_bus = _bus, addr = _addr)
        _LOGGER.debug("Validate_input!: %s", _bq25895.is_watchdog_enabled())

#        pass

    except IOError as err:
        raise CannotConnect(f"Can't communicating with I2C: Bus:{data[CONF_ADDR]}, Address:{data[CONF_BUS]} !") from err
    return {"title": DOMAIN}


#async def validate_settings(hass: HomeAssistant, data: dict[str, Any]) -> bool:
#    """Another validation method for our config steps."""
#    return True


class bq25895ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Integration."""

    VERSION = 1
    _input_data: dict[str, Any]
    _title: str

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return bq25895OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step.

        Called when you initiate adding an integration via the UI
        """

        errors: dict[str, str] = {}

        STEP_USER_DATA_SCHEMA = step_user_data_schema() # Default values

        if user_input is not None:
            # The form has been filled in and submitted, so process the data provided.
            try:
                _LOGGER.debug("Validate that the setup data")#My
                # ----------------------------------------------------------------------------
                # Validate that the setup data is valid and if not handle errors.
                # You can do any validation you want or no validation on each step.
                # The errors["base"] values match the values in your strings.json and translation files.
                # ----------------------------------------------------------------------------
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
#            except InvalidAuth:
#                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if "base" not in errors:
                # Validation was successful, so proceed to the next step.

                # ----------------------------------------------------------------------------
                # Setting our unique id here just because we have the info at this stage to do that
                # and it will abort early on in the process if alreay setup.
                # You can put this in any step however.
                # ----------------------------------------------------------------------------
                await self.async_set_unique_id(info.get("title"))
                self._abort_if_unique_id_configured()

                # Set our title variable here for use later
                self._title = info["title"]

                # ----------------------------------------------------------------------------
                # You need to save the input data to a class variable as you go through each step
                # to ensure it is accessible across all steps.
                # ----------------------------------------------------------------------------
                self._input_data = user_input

                # Call the next step
                #return await self.async_step_settings()
                return self.async_create_entry(title=self._title, data=self._input_data)

        # Show initial form.
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            last_step=True,  # Adding last_step True/False decides whether form shows Next or Submit buttons

        )



    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add reconfigure step to allow to reconfigure a config entry.

        This methid displays a reconfigure option in the integration and is
        different to options.
        It can be used to reconfigure any of the data submitted when first installed.
        This is optional and can be removed if you do not want to allow reconfiguration.
        """
        errors: dict[str, str] = {}
        config_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )

        RECONFIGURE_DATA_SCHEMA = step_user_data_schema(config_entry.data)


        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
#            except InvalidAuth:
#                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    config_entry,
                    unique_id=config_entry.unique_id,
                    data={**config_entry.data, **user_input},
                    reason="reconfigure_successful",
                )
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=RECONFIGURE_DATA_SCHEMA,
            errors=errors,
        )


class bq25895OptionsFlowHandler(OptionsFlow):
    """Handles the options flow.

    Here we use an initial menu to select different options forms,
    and show how to use api data to populate a selector.
    """

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Handle options flow.

        Display an options menu
        option ids relate to step function name
        Also need to be in strings.json and translation files.
        """

        return await self.async_step_options()

    async def async_step_options(self, user_input=None):
        """Handle menu options flow."""
        if user_input is not None:
            options = self.config_entry.options | user_input
            return self.async_create_entry(title="", data=options)

        # ----------------------------------------------------------------------------
        # It is recommended to prepopulate options fields with default values if
        # available.
        # These will be the same default values you use on your coordinator for
        # setting variable values if the option has not been set.
        # ----------------------------------------------------------------------------
        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                ): (vol.All(vol.Coerce(int), vol.Clamp(min=10))),
                vol.Required(
                    CONF_RECHARGE_THRESHOLD,
                    #description={"suggested_value": self.options.get(CONF_RECHARGE_THRESHOLD, DEFAULT_RECHARGE_THRESHOLD)}
                    default = str(self.options.get(CONF_RECHARGE_THRESHOLD, DEFAULT_RECHARGE_THRESHOLD))
                ): selector(
                    {
                    "select": {
                        "options": ["100", "200"],
                        "mode": "dropdown",
                        #"translation_key": CONF_RECHARGE_THRESHOLD,
                        }
                    }
                ),
                vol.Required(
                    CONF_THERMAL_THRESHOLD,
                    #description={"suggested_value": self.options.get(CONF_RECHARGE_THRESHOLD, DEFAULT_RECHARGE_THRESHOLD)}
                    default = str(self.options.get(CONF_THERMAL_THRESHOLD, DEFAULT_THERMAL_THRESHOLD))
                ): selector(
                    {
                    "select": {
                        "options": ["60", "80", "100", "120"],
                        "mode": "dropdown",
                        #"translation_key": CONF_RECHARGE_THRESHOLD,
                        }
                    }
                ),
                vol.Required(
                    CONF_CHARGE_CURRENT_LIMIT,
                    #description={"suggested_value": self.options.get(CONF_CHARGE_CURRENT_LIMIT, DEFAULT_CHARGE_CURRENT_LIMIT)}
                    default = str(self.options.get(CONF_CHARGE_CURRENT_LIMIT, DEFAULT_CHARGE_CURRENT_LIMIT))
                ): selector(
                    {
                    "number": {
                        "min": 0,
                        "max": 4.096,
                        "step": 0.064,
                        "unit_of_measurement": "A",
                        "mode": "slider",
                        }
                    }
                ),
                vol.Required(
                    CONF_CHARGE_VOLTAGE_LIMIT,
                    #description={"suggested_value": self.options.get(CONF_CHARGE_VOLTAGE_LIMIT, DEFAULT_CHARGE_VOLTAGE_LIMIT)}
                    default = str(self.options.get(CONF_CHARGE_VOLTAGE_LIMIT, DEFAULT_CHARGE_VOLTAGE_LIMIT))
                ): selector(
                    {
                    "number": {
                        "min": 3.840,
                        "max": 4.608,
                        "step": 0.064,
                        "unit_of_measurement": "V",
                        "mode": "slider",
                        }
                    }
                ),
                vol.Required(
                    CONF_INPUT_CURRENT_LIMIT,
                    #description={"suggested_value": self.options.get(CONF_INPUT_CURRENT_LIMIT, DEFAULT_INPUT_CURRENT_LIMIT)}
                    default = str(self.options.get(CONF_INPUT_CURRENT_LIMIT, DEFAULT_INPUT_CURRENT_LIMIT))
                ): selector(
                    {
                    "number": {
                        "min": 0.1,
                        "max": 3.250,
                        "step": 0.05,
                        "unit_of_measurement": "A",
                        "mode": "slider",
                        }
                    }
                ),
                vol.Required(
                    CONF_PRECHG_CURRENT,
                    #description={"suggested_value": self.options.get(CONF_TERM_CURRENT, DEFAULT_TERM_CURRENT)}
                    default = str(self.options.get(CONF_PRECHG_CURRENT, DEFAULT_PRECHG_CURRENT))
                ): selector(
                    {
                    "number": {
                        "min": 0.064,
                        "max": 1.024,
                        "step": 0.064,
                        "unit_of_measurement": "A",
                        "mode": "slider",
                        }
                    }
                ),
                vol.Required(
                    CONF_TERM_CURRENT,
                    #description={"suggested_value": self.options.get(CONF_TERM_CURRENT, DEFAULT_TERM_CURRENT)}
                    default = str(self.options.get(CONF_TERM_CURRENT, DEFAULT_TERM_CURRENT))
                ): selector(
                    {
                    "number": {
                        "min": 0.064,
                        "max": 1.024,
                        "step": 0.064,
                        "unit_of_measurement": "A",
                        "mode": "slider",
                        }
                    }
                ),
            }
        )

        return self.async_show_form(step_id="options", data_schema=data_schema)

# vol.Required(CONF_BUS, default = data.get(CONF_BUS)): selector(
class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


#class InvalidAuth(HomeAssistantError):
#    """Error to indicate there is invalid auth."""