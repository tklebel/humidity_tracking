#!/usr/bin/env python3

import sys
import Adafruit_DHT
from time import sleep
from datetime import datetime
from functions import connect_db


# setup db connection
con = connect_db()
cursor = con.cursor()

# set sleep duration for test purposes
sleep_duration = 30

# define function for printing results
def print_result(time, humidity, temperature):
    if humidity is not None and temperature is not None:
        # format time string
        time_pretty = time.strftime('%Y-%m-%d %H:%M:%S')

        print('Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time_pretty, temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)

def write_to_db(cursor, time, humidity, temperature):

    insert_sql = """INSERT INTO humidity_data
                    VALUES (%s, %s, %s);"""

    cursor.execute(insert_sql, (time, humidity, temperature))

    con.commit()

def cleanup_db():
    con.close()
    cursor.close()
    print("Database connections closed")



# sensor type and the pin to which the sensor is connected are hard coded since they don't change
sensor = Adafruit_DHT.AM2302
pin = 4

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        time = datetime.now()

        write_to_db(cursor, time, humidity, temperature)

        sleep(sleep_duration)
except KeyboardInterrupt:
    cleanup_db()
    sys.exit(0)
