from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2


def read():
    ina = INA219(SHUNT_OHMS, busnum=1)
    ina.configure()

    ina2 = INA219(SHUNT_OHMS, address=0x41, busnum=1)
    ina2.configure()

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

