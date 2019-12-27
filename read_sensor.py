#!/usr/bin/env python3

import sys
import Adafruit_DHT
from time import sleep
from datetime import datetime



# define function for printing results
def print_result(time, humidity, temperature):
    if humidity is not None and temperature is not None:
        # format time string
        time_pretty = time.strftime('%Y-%m-%d %H:%M:%S')

        print('Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time_pretty, temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)



# Parse command line parameters.
if len(sys.argv) == 2 and (2 <= int(sys.argv[1]) <=10):
    sleep_duration = int(sys.argv[1])
else:
    print('Usage: read_sensor.py 2')
    print('Explanation: read from sensor every two seconds. The second paramter needs to be >=2 & <=10')
    sys.exit(1)



# sensor type and the pin to which the sensor is connected are hard coded since they don't change
sensor = Adafruit_DHT.AM2302
pin = 4

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        time = datetime.now()

        print_result(time, humidity, temperature)

        sleep(sleep_duration)
except KeyboardInterrupt:
    sys.exit(0)
