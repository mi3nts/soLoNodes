from ina219 import INA219
from ina219 import DeviceRangeError
import odroid_wiringpi as wpi
wpi.wiringPiSetup()



SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2


def read():

    batteryLevelRaw = wpi.analogRead(29)
    print(batteryLevelRaw)
    ina = INA219(SHUNT_OHMS, busnum=1)
    ina.configure()
    print(ina._i2c)

    ina2 = INA219(SHUNT_OHMS, address=0x41, busnum=1)
    ina2.configure()
    print(ina2._i2c)

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        print("Current overflow")


    print("Bus Voltage: %.3f V" % ina2.voltage())
    try:
        print("Bus Current: %.3f mA" % ina2.current())
        print("Power: %.3f mW" % ina2.power())
        print("Shunt voltage: %.3f mV" % ina2.shunt_voltage())
    except DeviceRangeError as e:
        print("Current overflow")



if __name__ == "__main__":
    read()

