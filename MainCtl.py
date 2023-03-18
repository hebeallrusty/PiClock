
print("Loading modules")
# standard libraries
import datetime as dt
import time as tm
import configparser


# installed libraries
import bme280
import smbus2
#import timed_count

# custom libraries
from Sun import Sun
from Moon import Moon
from Season import Season
from Seg import disp, add_dot


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

# get time and store it to be used throughout the loop to prevent the rare potential where the date changes by the time the loop completes
NOW = dt.datetime.now()

#t_0 = 0
#t_1 = 0


 
# start a loop update everything
while True:
    
#    t_1 = tm.time()

#    print("elapsed time: ",t_1 - t_0)

    while NOW.second == dt.datetime.now().second:
        tm.sleep(0.1)
#    t_0 = tm.time()
    


    if NOW.minute == 0:
        # only run the once per hour
        if NOW.second == 0:
            print("Sun / moon calcs")    
            today = dt.datetime(NOW.year,NOW.month,NOW.day,0,0,0)
            s = Sun(NOW,LOCATION,0)
            m = Moon(NOW)
            sunrise = today + s.Rise()['Official']
            sunset = today + s.Set()['Official']
            #print("SunRise: ",f'{sunrise.hour:02d}',":",f'{sunrise.minute:02d}',"; SunSet: ",f'{sunset.hour:02d}',":",f'{sunset.minute:02d}')
            #print("Moon: ",m.MoonPhase())
            #print(Season(NOW))

    
    # get sensor data
    bme280_data = bme280.sample(bme280_bus,bme280_address,bme280_calibration_params)
    #print("Temp: ",round(bme280_data.temperature,1), "deg Humidity: ", round(bme280_data.humidity,0), "% Pressure: ",round(bme280_data.pressure,0))

    #print(NOW.strftime('%H:%M:%S %a %d-%m-%y'))
    

    # to display it, they need to be in a zero-padded list so that the digits can be iterated over
    bme_t = [int(x) for x in f"{int(round(bme280_data.temperature,0)):02d}"]
    bme_h = [int(x) for x in f"{int(round(bme280_data.humidity,0)):02d}"]

    # update time variable
    NOW = dt.datetime.now()

    hr = [int(x) for x in f"{NOW.hour:02d}"]
    mn = [int(x) for x in f"{NOW.minute:02d}"]
    sc = [int(x) for x in f"{NOW.second:02d}"]

    # display loop
    for i in range(0,2):
        # Sensor
        disp(bme_h[i],10+i)
        disp(bme_t[i],8+i)

        # Time
        disp(hr[i], 0+i)
        disp(mn[i], 2+i)
        disp(sc[i], 4+i)

    # add dots to the display
    #add_dot(1)
    #add_dot(3)       



