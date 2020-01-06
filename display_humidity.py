#!/usr/bin/env python3

import sys
import Adafruit_DHT
import logging
from time import sleep
from functions import get_data
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD



# set sleep duration for test purposes
sleep_duration = 30

# set up logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()


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
lcd.clear()         # clear the display in case something was not removed before


def main():
    while True:
        time, humidity, temperature = get_data()

        # display measurements on display
        lcd.setCursor(0,0)  # set cursor position. this needs to be here, otherwise the display keeps old output
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
        clear_display()

