
print("Loading modules")
# standard libraries
import datetime as dt
import time as tm
import configparser

# installed libraries
import bme280
import smbus2

# custom libraries
from Sun import Sun
from Moon import Moon



print("Initilising")
# initialisation of loop

# Initialise config file for reading
# set up object Config which will all options to be read from file
CONFIG_FILE="Config.ini"
Config = configparser.ConfigParser()
Config.read(CONFIG_FILE)

# Get location for sunrise / set times
LOCATION = [float(Config.get('LOCATION','latitude')),float(Config.get('LOCATION','longitude'))]

# get the i2c port
i2c_port = int(Config.get('I2C','Port'))

# get bme280 sensor address; address needs to be base16 integer but is stored as string
bme280_address = int(Config.get('I2C','BME280'),16)


# initialise BME280 sensor
bme280_bus = smbus2.SMBus(i2c_port)
bme280_calibration_params = bme280.load_calibration_params(bme280_bus,bme280_address)


# start a loop update everything
while True:
    
    # get time and store it to be used throughout the loop to prevent the rare potential where the date changes by the time the loop completes
    NOW = dt.datetime.now()
    today = dt.datetime(NOW.year,NOW.month,NOW.day,0,0,0)


    s = Sun(NOW,LOCATION,0)
    m = Moon(NOW)
    sunrise = today + s.Rise()['Official']
    sunset = today + s.Set()['Official']
    print("SunRise: ",f'{sunrise.hour:02d}',":",f'{sunrise.minute:02d}',"; SunSet: ",f'{sunset.hour:02d}',":",f'{sunset.minute:02d}')
    print("Moon: ",m.MoonPhase())
    bme280_data = bme280.sample(bme280_bus,bme280_address,bme280_calibration_params)
    print("Temp: ",round(bme280_data.temperature,1), "deg Humidity: ", round(bme280_data.humidity,0), "% Pressure: ",round(bme280_data.pressure,0))
    print(NOW.strftime('%H:%M:%S %a %d-%m-%y'))
    
    


    tm.sleep(0.5)
