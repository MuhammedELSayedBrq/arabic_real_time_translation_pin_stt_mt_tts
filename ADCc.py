import machine
import utime

sensor_temp = machine.ADC(27)

while True:
    reading = sensor_temp.read_u16()
    print("ADC value is: ",reading)
    utime.sleep(0.02)
