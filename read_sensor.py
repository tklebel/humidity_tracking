#!/usr/bin/env python3

import sys
import Adafruit_DHT
from time import sleep
from datetime import datetime


# Parse command line parameters.
if len(sys.argv) == 2 and int(sys.argv[1]) >=2 and int(sys.argv[1]) <=10:
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
		time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		if humidity is not None and temperature is not None:
			print('Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time, temperature, humidity))
			sleep(sleep_duration)
		else:
			print('Failed to get reading. Try again!')
			sys.exit(1)
except KeyboardInterrupt:
	sys.exit(0)
