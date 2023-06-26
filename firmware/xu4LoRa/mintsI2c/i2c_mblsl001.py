import datetime
from datetime import timedelta
import time
import math

from ina219 import INA219
from ina219 import DeviceRangeError
import odroid_wiringpi as wpi



SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2


# Mints Battery level SoLo nodes
class MBLSL001:

    def __init__(self, busNum,pinNum,resistorGround,resisterHigh):
        
        self.inaSolarOut    =None
        self.inaBatteryOut  =None
        self.batteryPin     = pinNum
        self.batteryFactor  = ((2*1.8)/(4095))*(resisterHigh/resistorGround+1)

        try:
            self.inaSolarOut   = INA219(SHUNT_OHMS, busnum=busNum)
            self.inaBatteryOut = INA219(SHUNT_OHMS, address=0x41, busnum=busNum)
        
        except Exception as e:
            time.sleep(.5)
            print ("Error and type: %s - %s." % (e,type(e)))
            time.sleep(.5)
            print("INAs not found")
            time.sleep(.5)
    
    def initiate(self,retriesIn):
        time.sleep(1)
        try:
            if "Adafruit_GPIO.I2C" in str(self.inaSolarOut._i2c)\
                and \
                    "Adafruit_GPIO.I2C" in str(self.inaBatteryOut._i2c):

                self.inaSolarOut.configure()
                self.inaBatteryOut.configure()
                return True;
        except Exception as e:
            time.sleep(.5)
            print ("Error and type: %s - %s." % (e,type(e)))
            time.sleep(.5)
            print("INAs not configured")
            time.sleep(.5)
            return False

      
    def read(self):
        
        batteryLevelRaw     = wpi.analogRead(self.batteryPin)
        cellVoltage         = batteryLevelRaw*self.batteryFactor
        # Find battery volatage

        solarVoltage        = self.inaSolarOut.voltage()
        solarCurrent        = self.inaSolarOut.current()
        solarPower          = self.inaSolarOut.power()
        solarShuntVoltage   = self.inaSolarOut.shunt_voltage()

        batteryVoltage      = self.inaBatteryOut.voltage()
        batteryCurrent      = self.inaBatteryOut.current()
        batteryPower        = self.inaBatteryOut.power()
        batteryShuntVoltage = self.inaBatteryOut.shunt_voltage()        

        return [batteryLevelRaw,cellVoltage,\
                solarVoltage,solarCurrent,solarPower,solarShuntVoltage,\
                batteryVoltage,batteryCurrent,batteryPower,batteryShuntVoltage];


