import psycopg2
import Adafruit_DHT
from datetime import datetime
from time import sleep



def connect_db():
    with open('db_credentials.txt') as file:
        params = file.read()

    connection = psycopg2.connect(params)
    
    return(connection)

# define function for printing results
def format_result(time, humidity, temperature):
    if humidity is not None and temperature is not None:
        # format time string
        time_pretty = time.strftime('%Y-%m-%d %H:%M:%S')

        return('Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time_pretty, temperature, humidity))
    else:
        return('Failed to get reading.')

def get_data():
    # sensor type and the pin to which the sensor is connected are hard coded since they don't change
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
    time = datetime.now()

    if humidity is not None and temperature is not None:
        return (time, humidity, temperature)
    else:
        print("We got no reading, but ``humidity = " + str(humidity) + " & temp = " + str(temperature) + "`` , trying again.")
        sleep(2) # sleep for two seconds before re-trying
        get_data()