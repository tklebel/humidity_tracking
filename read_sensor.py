#!/usr/bin/env python3

import sys
import Adafruit_DHT
import logging
from time import sleep
from functions import connect_db, get_data, create_logger


# setup db connection
con = connect_db()
cursor = con.cursor()

# set sleep duration for test purposes
sleep_duration = 30

# set up logging for debugging
logger = create_logger('read_sensor.log')


# function for writing results to database
def write_to_db(cursor, time, humidity, temperature):

    insert_sql = """INSERT INTO humidity_data
                    VALUES (%s, %s, %s);"""

    cursor.execute(insert_sql, (time, humidity, temperature))

    con.commit()

def cleanup_db():
    con.close()
    cursor.close()
    logger.info("Database connections closed.")

def main():
    logger.info(f'Reading data and writing to database every {sleep_duration} seconds.')
    while True:
        time, humidity, temperature = get_data()

        write_to_db(cursor, time, humidity, temperature)

        sleep(sleep_duration)


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        logger.info('Terminating...')
        cleanup_db()

