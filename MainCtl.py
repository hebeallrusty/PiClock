
print("Loading modules")
# standard libraries
import datetime as dt
import time as tm
#import subprocess


# installed libraries
import bme280
import smbus2
#import timed_count

# custom libraries
import Config
from Sun import Sun
from Moon import Moon
from Season import Season
from Seg import disp, add_dot, dispupdate



print("Initilising")
# initialisation of loop


# Get location for sunrise / set times
LOCATION = Config.Location
print(LOCATION)

# get the i2c port
i2c_port = int(Config.I2CPort)

# get bme280 sensor address; address needs to be base16 integer but is stored as string
bme280_address = int(str(Config.BME280),16)

# get addresses of the HT16k33
HT16K33 = Config.HT16K33

# initialise BME280 sensor
bme280_bus = smbus2.SMBus(i2c_port)
bme280_calibration_params = bme280.load_calibration_params(bme280_bus,bme280_address)

# get time and store it to be used throughout the loop to prevent the rare potential where the date changes by the time the loop completes
NOW = dt.datetime.now()

#t_0 = 0
#t_1 = 0

first_run = 1
 
# start a loop update everything
while True:
    
    #t_0 = tm.time()

    # wait for the clock to tick before running the main 
    while dt.datetime.now().second == NOW.second:
        tm.sleep(0.1)
    #t_1 = tm.time()
    #print("elapsed time: ",t_1 - t_0)

    # update time variable otherwise we'll be 1 second behind reality
    NOW = dt.datetime.now()
    

    # only run the once per hour - set up Sunrise / Set etc so that we are not hammering the processor for no good reason. Needs to run once though initially
    if ((NOW.minute == 0) and (NOW.second == 0)) or (first_run == 1):
        
        #print(first_run)
        first_run = 0
            
        today = dt.datetime(NOW.year,NOW.month,NOW.day,tm.daylight,0,0)
        s = Sun(NOW,LOCATION,0)
        m = Moon(NOW)
        sunrise = today + s.Rise()['Official']
        sunset = today + s.Set()['Official']

        civil_start = today + s.Rise()['Civil']
        civil_end = today + s.Set()['Civil']        

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

    hr = [int(x) for x in f"{NOW.hour:02d}"]
    mn = [int(x) for x in f"{NOW.minute:02d}"]
    sc = [int(x) for x in f"{NOW.second:02d}"]

    dy = [int(x) for x in f"{NOW.day:02d}"]
    mt = [int(x) for x in f"{NOW.month:02d}"]
    
    yr = [int(x) for x in f"{NOW.year:02d}"]

    sunrise_hr = [int(x) for x in f"{sunrise.hour:02d}"]
    sunrise_mn = [int(x) for x in f"{sunrise.minute:02d}"]

    sunset_hr =  [int(x) for x in f"{sunset.hour:02d}"]
    sunset_mn =  [int(x) for x in f"{sunset.minute:02d}"]

    civil_start_hr = [int(x) for x in f"{civil_start.hour:02d}"]
    civil_start_mn = [int(x) for x in f"{civil_start.minute:02d}"]

    civil_end_hr =  [int(x) for x in f"{civil_end.hour:02d}"]
    civil_end_mn = [int(x) for x in f"{civil_end.minute:02d}"]
    

    # display loop
    #for i in range(0,2):
    for i in [1,0]:

        # Sensor
        disp(bme_h[i],10+i,0)
        disp(bme_t[i],8+i,0)

        # Sunrise/Set - rotate information on display

        if int(NOW.second) % 8 == 0:
            disp(sunrise_hr[i], 0+i,0)
            disp(sunrise_mn[i], 2+i,0)
            disp(23, 4+i,0)
        elif int(NOW.second) % 8 == 2:
            disp(23, 0+i,0)
            disp(sunset_hr[i], 2+i,0)
            disp(sunset_mn[i], 4+i,0)  
        elif int(NOW.second) % 8 == 4:
            disp(civil_start_hr[i], 0+i,0)
            disp(civil_start_mn[i], 2+i,0)
            disp(23, 4+i,0)        
        elif int(NOW.second) % 8 == 6:
            disp(23, 0+i,0)
            disp(civil_end_hr[i], 2+i,0)
            disp(civil_end_mn[i], 4+i,0)            

        # Time
        disp(hr[i], 0+i,1)
        disp(mn[i], 2+i,1)
        disp(sc[i], 4+i,1)

        # Date
        disp(dy[i], 8+i,1)
        disp(mt[i], 10+i,1)
        disp(yr[i+2], 12+i,1)
    
    # update display once all the buffers are filled
    dispupdate(1)
    dispupdate(0)



