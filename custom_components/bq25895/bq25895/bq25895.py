
import smbus2 as smbus
from .bq2589x_reg import *
import math

class bq25895():

    def __init__(self, i2c_bus=1, addr=0x6A):
        self.bus = smbus.SMBus(i2c_bus)
        self.addr = addr

    def update_bits(self, reg, mask, data):
        tmp = self.bus.read_byte_data(self.addr, reg)
        tmp &= ~mask
        tmp |= data & mask
        return self.bus.write_byte_data(self.addr, reg, tmp)

    def getBus_voltage_mV(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_11)
        val =  BQ2589X_VBUSV_BASE + ((data & BQ2589X_VBUSV_MASK) >> BQ2589X_VBUSV_SHIFT) * BQ2589X_VBUSV_LSB
        return val

    def getCharging_status(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_0B)
        data &= BQ2589X_CHRG_STAT_MASK
        data >>= BQ2589X_CHRG_STAT_SHIFT
        match data:
            case 0:
                val = BQ2589X_CHRG_STAT_00
            case 1:
                val = BQ2589X_CHRG_STAT_01
            case 2:
                val = BQ2589X_CHRG_STAT_02
            case 3:
                val = BQ2589X_CHRG_STAT_03
            case _:
                val = BQ2589X_CHRG_STAT_XX
        return val
        
    def getBattery_voltage_mV(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_0E)
        val =  (BQ2589X_BATV_BASE + ((data & BQ2589X_BATV_MASK) >> BQ2589X_BATV_SHIFT) * BQ2589X_BATV_LSB)
        return val

    def getSystem_voltage_mV(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_0F)
        val =  (BQ2589X_SYSV_BASE + ((data & BQ2589X_SYSV_MASK) >> BQ2589X_SYSV_SHIFT) * BQ2589X_SYSV_LSB)
        return val

    def getMin_system_voltage_mV(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_03)
        val = (BQ2589X_SYS_MINV_BASE + ((data & BQ2589X_SYS_MINV_MASK) >> BQ2589X_SYS_MINV_SHIFT) * BQ2589X_SYS_MINV_LSB)
        return val

    def setMin_system_voltage_mV(self, data = 3000):
        tmp = round((data - BQ2589X_SYS_MINV_BASE) / BQ2589X_SYS_MINV_LSB)
        self.update_bits(BQ2589X_REG_03, BQ2589X_SYS_MINV_MASK, tmp << BQ2589X_SYS_MINV_SHIFT)
        return

    def getCharge_current_mA(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_12)
        val =  (BQ2589X_ICHGR_BASE + ((data & BQ2589X_ICHGR_MASK) >> BQ2589X_ICHGR_SHIFT) * BQ2589X_ICHGR_LSB)
        return val

    def getCharge_current_limit_mA(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_04)
        val =  (BQ2589X_ICHG_BASE + ((data & BQ2589X_ICHG_MASK) >> BQ2589X_ICHG_SHIFT) * BQ2589X_ICHG_LSB)
        return val
        
    def setCharge_current_limit_mA(self, data = 512):
        tmp = round((data - BQ2589X_ICHG_BASE) / BQ2589X_ICHG_LSB)
        self.update_bits(BQ2589X_REG_04, BQ2589X_ICHG_MASK, tmp << BQ2589X_ICHG_SHIFT)
        return

    def getCharge_voltage_limit_mV(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_06)
        val =  (BQ2589X_VREG_BASE + ((data & BQ2589X_VREG_MASK) >> BQ2589X_VREG_SHIFT) * BQ2589X_VREG_LSB)
        return val

    def setCharge_voltage_limit_mV(self, data = 4096):
        tmp = round((data - BQ2589X_VREG_BASE) / BQ2589X_VREG_LSB)
        self.update_bits(BQ2589X_REG_06, BQ2589X_VREG_MASK, tmp << BQ2589X_VREG_SHIFT)
        return

    def getInput_IDPM_limit_mA(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_13)
        val =  (BQ2589X_IDPM_LIM_BASE + ((data & BQ2589X_IDPM_LIM_MASK) >> BQ2589X_IDPM_LIM_SHIFT) * BQ2589X_IDPM_LIM_LSB)
        return val

    def setInput_IDPM_limit_mA(self, data = 2000):
        tmp = round((data - BQ2589X_IDPM_LIM_BASE) / BQ2589X_IDPM_LIM_LSB)
        self.update_bits(BQ2589X_REG_13, BQ2589X_IDPM_LIM_MASK, tmp << BQ2589X_IDPM_LIM_SHIFT)
        return

    def getInput_current_limit_mA(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_00)
        val =  (BQ2589X_IINLIM_BASE + ((data & BQ2589X_IINLIM_MASK) >> BQ2589X_IINLIM_SHIFT) * BQ2589X_IINLIM_LSB)
        return val

    def setInput_current_limit_mA(self, data = 2000):
        tmp = round((data - BQ2589X_IINLIM_BASE) / BQ2589X_IINLIM_LSB)
        self.update_bits(BQ2589X_REG_00, BQ2589X_IINLIM_MASK, tmp << BQ2589X_IINLIM_SHIFT)
        return


    def getPrechg_current_mA(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_05)
        val =  (BQ2589X_IPRECHG_BASE + ((data & BQ2589X_IPRECHG_MASK) >> BQ2589X_IPRECHG_SHIFT) * BQ2589X_IPRECHG_LSB)
        return val

    def setPrechg_current_mA(self, data = 128):
        tmp = round((data - BQ2589X_IPRECHG_BASE) / BQ2589X_IPRECHG_LSB)
        self.update_bits(BQ2589X_REG_05, BQ2589X_IPRECHG_MASK, tmp << BQ2589X_IPRECHG_SHIFT)
        return

    def getTerm_current_mA(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_05)
        val =  (BQ2589X_ITERM_BASE + ((data & BQ2589X_ITERM_MASK) >> BQ2589X_ITERM_SHIFT) * BQ2589X_ITERM_LSB)
        return val

    def setTerm_current_mA(self, data = 128):
        tmp = round((data - BQ2589X_ITERM_BASE) / BQ2589X_ITERM_LSB)
        self.update_bits(BQ2589X_REG_05, BQ2589X_ITERM_MASK, tmp << BQ2589X_ITERM_SHIFT)
        return

    def getRecharge_threshold_mV(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_06)
        data &= BQ2589X_VRECHG_MASK
        data >>= BQ2589X_VRECHG_SHIFT
        if (data):
            val = 200
        else: 
            val = 100
        return val

    def setRecharge_threshold_mV(self, data = 100):
        if (data == 200):
            tmp = BQ2589X_VRECHG_200MV
        else:
            tmp = BQ2589X_VRECHG_100MV
        self.update_bits(BQ2589X_REG_06, BQ2589X_VRECHG_MASK, tmp << BQ2589X_VRECHG_SHIFT)
        return

    def getFault_status(self, fault_type):
        val = 0
        tmp1 = 255
        tmp2 = 255
        
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_0C)
        match fault_type:
            case 7:
                tmp1 = BQ2589X_FAULT_WDT_MASK
                tmp2 = BQ2589X_FAULT_WDT_SHIFT
            case 6:
                tmp1 = BQ2589X_FAULT_BOOST_MASK
                tmp2 = BQ2589X_FAULT_BOOST_SHIFT
            case 4:
                tmp1 = BQ2589X_FAULT_CHRG_MASK
                tmp2 = BQ2589X_FAULT_CHRG_SHIFT
            case 3:
                tmp1 = BQ2589X_FAULT_BAT_MASK
                tmp2 = BQ2589X_FAULT_BAT_SHIFT
            case 0:
                tmp1 = BQ2589X_FAULT_NTC_MASK
                tmp2 = BQ2589X_FAULT_NTC_SHIFT

        val &= tmp1
        val >>= tmp2
        return val

    def getTemperature(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_10)
        tmp = (BQ2589X_TSPCT_BASE + ((data & BQ2589X_TSPCT_MASK) >> BQ2589X_TSPCT_SHIFT) * BQ2589X_TSPCT_LSB)
        VTS = 5.0 * tmp / 100.0
        RP  = ( VTS * 5230.0 ) / ( 5.0 - VTS )
        NTC = ( RP * 30100.0 ) / ( 30100.0 - RP )
        val = NTC / 10000.0
        val = math.log(val)
        val /= 3950.0
        val += 1.0 / 298.15
        val = 1.0 / val
        val -= 273.25
        #val = temp
        return val

    def getThermal_threshold(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_08)
        tmp = (data & BQ2589X_TREG_MASK) >> BQ2589X_TREG_SHIFT;
        match tmp:
            case 1:
                val = 80
            case 2: 
                val = 100
            case 3: 
                val = 120
            case _: 
                val = 60
        return val

    def setThermal_threshold(self, data = 120):
        match data:
            case 60:
                tmp = BQ2589X_TREG_60C
            case 80: 
                tmp = BQ2589X_TREG_80C
            case 100: 
                tmp = BQ2589X_TREG_100C
            case _: 
                tmp = BQ2589X_TREG_120C
        self.update_bits(BQ2589X_REG_08, BQ2589X_TREG_MASK, tmp << BQ2589X_TREG_SHIFT)
        return

    def reset_chip(self):
        tmp = BQ2589X_RESET << BQ2589X_RESET_SHIFT
        self.update_bits(BQ2589X_REG_14, BQ2589X_RESET_MASK, tmp)
        return
        

    def adc_start(self, oneshot = 0):
        '''* ADC Conversion Start Control
           * 0 – ADC conversion not active (default).
           * 1 – Start ADC Conversion
           * This bit is read-only when CONV_RATE = 1. The bit stays high during
           * ADC conversion and during input source detection.
           *
           * ADC Conversion Rate Selection
           * 0 – Oneshot ADC conversion (default)
           * 1 – Start 1s Continuous Conversion'''
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_02)
        if (((data & BQ2589X_CONV_RATE_MASK) >> BQ2589X_CONV_RATE_SHIFT) == BQ2589X_ADC_CONTINUE_ENABLE):
            return BQ2589X_OK
        
        if (oneshot):
            self.update_bits(BQ2589X_REG_02, BQ2589X_CONV_START_MASK, BQ2589X_CONV_START << BQ2589X_CONV_START_SHIFT)
        else:
            self.update_bits(BQ2589X_REG_02, BQ2589X_CONV_RATE_MASK, BQ2589X_ADC_CONTINUE_ENABLE << BQ2589X_CONV_RATE_SHIFT)
        return

    def adc_stop(self):
        self.update_bits(BQ2589X_REG_02, BQ2589X_CONV_RATE_MASK, BQ2589X_ADC_CONTINUE_DISABLE << BQ2589X_CONV_RATE_SHIFT)
        return

    def is_watchdog_enabled(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_07)
        data &= BQ2589X_WDT_MASK;
        data >>= BQ2589X_WDT_SHIFT;
        return data

    def disable_watchdog(self):
        self.update_bits(BQ2589X_REG_07, BQ2589X_WDT_MASK, BQ2589X_WDT_DISABLE << BQ2589X_WDT_SHIFT)
        return

    def enable_watchdog(self):
        self.update_bits(BQ2589X_REG_07, BQ2589X_WDT_MASK, BQ2589X_WDT_40S << BQ2589X_WDT_SHIFT)
        return

    def reset_watchdog(self):
        self.update_bits(BQ2589X_REG_03, BQ2589X_WDT_RESET_MASK, BQ2589X_WDT_RESET << BQ2589X_WDT_RESET_SHIFT)
        return

    def exit_ship_mode(self):
        self.update_bits(BQ2589X_REG_09, BQ2589X_BATFET_DIS_MASK, BQ2589X_BATFET_ON << BQ2589X_BATFET_DIS_SHIFT)
        return

    def enter_ship_mode(self):
        self.update_bits(BQ2589X_REG_09, BQ2589X_BATFET_DIS_MASK, BQ2589X_BATFET_OFF << BQ2589X_BATFET_DIS_SHIFT)
        return

    def is_charger_enabled(self):
        data = self.bus.read_byte_data(self.addr, BQ2589X_REG_03)
        data &= BQ2589X_CHG_CONFIG_MASK;
        data >>= BQ2589X_CHG_CONFIG_SHIFT;
        return data

    def enable_charger(self):
        self.update_bits(BQ2589X_REG_03, BQ2589X_CHG_CONFIG_MASK, BQ2589X_CHG_ENABLE << BQ2589X_CHG_CONFIG_SHIFT)
        return

    def disable_charger(self):
        self.update_bits(BQ2589X_REG_03, BQ2589X_CHG_CONFIG_MASK, BQ2589X_CHG_DISABLE << BQ2589X_CHG_CONFIG_SHIFT)
        return
