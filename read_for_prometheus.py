#!/usr/bin/env python3

import sys
import Adafruit_DHT
import logging
from time import sleep
from functions import read_sensor, systemd_logger
from prometheus_client import start_http_server, Gauge



sleep_duration = 5

# set up logging for debugging
logger = systemd_logger()

temp = Gauge('temperature', 'Temperature')
humid = Gauge('humidity', 'Humidity')


def main():
    logger.info(f'Reading data and writing to prometheus every {sleep_duration} seconds.')

    while True:
        time, humidity, temperature = read_sensor()

        if humidity and temperature:
            temp.set(temperature)
            humid.set(humidity)
        else:
            continue

        sleep(sleep_duration)


if __name__=='__main__':
    try:
        start_http_server(8000)
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        logger.info('Terminating...')
