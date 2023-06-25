import datetime
from datetime import timedelta
import logging
import smbus2
import struct
import time
import bme280
import math
import time
from pa1010d import PA1010D

class PAI101D_:

    def __init__(self, i2c_dev,debugIn):
        
        self.gps = PA1010D()
        self.gps._i2c = i2c_dev

    def initiate(self):
        try:
            ready = None
            result = self.gps.update()
            print(result)

            print(self.gps.read_sentence())

            print("Reading only RMC and GGA Commands")
            self.gps.send_command("PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

            print("Sending to Power Save Mode")
            self.gps.send_command("$PMTK161,0*28")

            time.sleep(1)
            return True   
        except OSError:
            return False
            pass
    
      
    def read(self):
        measurement = bme280.sample(self.i2c, self.i2c_addr, self.calibration_params)
        if measurement is not None:
            temperature = measurement.temperature
            pressure    = measurement.pressure
            humidity    = measurement.humidity
            A = (100*pressure) / 101325;
            B = 1 / 5.25588
            C = pow(A, B)
            C = 1.0 - C
            altitude = C / 0.0000225577
            dewPoint = 243.04 * (math.log(humidity/100.0) + ((17.625 * temperature)/(243.04 + temperature)))/(17.625 - math.log(humidity/100.0) - ((17.625 * temperature)/(243.04 + temperature)));
            time.sleep(1)
            # Units temperature C, Pressure milliBar, Humidity %, Altitude m
            return [temperature,pressure,humidity,dewPoint,altitude];
        
        else:
            time.sleep(1)
            print("BME280 Measurments not read")
            return [];
