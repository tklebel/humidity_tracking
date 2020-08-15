import psycopg2
import board
import adafruit_dht
from datetime import datetime
from time import sleep

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def connect_db():
    with open('db_credentials.txt') as file:
        params = file.read()

    connection = psycopg2.connect(params)
    
    return connection

# define function for printing results
def format_result(time, humidity, temperature):
    if humidity is not None and temperature is not None:
        # format time string
        time_pretty = time.strftime('%Y-%m-%d %H:%M:%S')

        return 'Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time_pretty, temperature, humidity)
    else:
        return 'Failed to get reading.'


def read_sensor():
    try:
        dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        time = datetime.now()

        return (time, temperature, humidity)
    except RuntimeError:
        logger.info('We got no reading, trying again.')

        sleep(2)
        return read_sensor()


def get_data():
    time, temperature, humidity = read_sensor()

    if humidity is not None and temperature is not None:
        return (time, humidity, temperature)
    else:
        logger.info('We got no reading, but ``humidity = ' + str(humidity) + ' & temp = ' + str(temperature) + '`` , trying again.')
        sleep(2) # sleep for two seconds before re-trying
        return get_data()


def create_logger(file):
    # set up logging for debugging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler(file)

    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler
    logger.addHandler(fh)

    return logger
