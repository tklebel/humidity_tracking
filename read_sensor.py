#!/usr/bin/env python3

import sys
import Adafruit_DHT
from time import sleep
from datetime import datetime
from functions import connect_db
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD



# setup db connection
con = connect_db()
cursor = con.cursor()

# set sleep duration for test purposes
sleep_duration = 30

# sensor type and the pin to which the sensor is connected are hard coded since they don't change
sensor = Adafruit_DHT.AM2302
pin = 4

# function for writing results to database
def write_to_db(cursor, time, humidity, temperature):

    insert_sql = """INSERT INTO humidity_data
                    VALUES (%s, %s, %s);"""

    cursor.execute(insert_sql, (time, humidity, temperature))

    con.commit()

def cleanup_db():
    con.close()
    cursor.close()
    print("Database connections closed.")

def clear_display():
    lcd.clear()
    print("Display cleared.")


## setup display stuff (copied from example from freenove) #########
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
mcp.output(3,1)     # turn on LCD backlight (set second param to 0 for no backlight)
lcd.begin(16,2)     # set number of LCD lines and columns
lcd.setCursor(0,0)  # set cursor position

def main():
    print("Reading data and writing to database every", sleep_duration, "seconds.")
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        time = datetime.now()

        write_to_db(cursor, time, humidity, temperature)

        # display measurements on display

        lcd.message('Temp={0:0.1f}*C\n'.format(temperature))
        lcd.message('Humidity={0:0.1f}%'.format(humidity))

        sleep(sleep_duration)


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        print('\nTerminating...')
        cleanup_db()
        clear_display()

