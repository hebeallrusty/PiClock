
print("Loading modules")
# standard libraries
import datetime as dt
import time as tm
import math


# installed libraries
import bme280
import smbus2

# custom libraries
import Config
import Sun
from Moon import MoonTime,Phase,JulianDay
from Season import Season
from Seg import disp, add_dot, dispupdate
import TimeCalc
import BST

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

# Season Dict
SeasonDict = {'Spring':0,'Summer':1,'Autumn':2,'Winter':3}

# Moon phases - moon phase code will only give the 4 cardinal phases, however we want to display all 8
Phases = {'New Moon':0, 'Waxing Crescent':1, 'First Quarter': 2, 'Waxing Gibbous':3, 'Full Moon': 4, 'Waning Gibbous':5,'Last Quarter':6,'Waning Crescent':7}
# the in-between phases are discovered by comparing today's day with the day that the phases occur in the lunation. Where there is a change in sign (i.e. today < phase day becomes today > phase day (and today != phase day), we know the moon is between phases and therefore we move the phase on a half - that's what the Half_phase dict does. The key is the maximal phase, the value is the half phase before that cardinal phase)
Half_phase = {'New Moon': 'Waning Crescent', 'First Quarter': 'Waxing Crescent', 'Full Moon': 'Waxing Gibbous','Last Quarter':'Waning Crescent'}

first_run = 1
c = 0 # this is needed for the display counter
 
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
    

    # only run the once per day - set up Sunrise / Set etc so that we are not hammering the processor for no good reason. Needs to run once though initially
    if ((NOW.minute == 0) and (NOW.second == 0) and (NOW.hour == 0)) or (first_run == 1): # everything under here runs once per hour, or on the initial run
        
        #print(first_run)
        first_run = 0 # reset the flag for the initial run
            
        # display season

        SeasonLight = SeasonDict[Season(NOW)]
        SeasonBlanking = []

        for i in range(0,8):
            if SeasonLight != i:
                SeasonBlanking.append(i)

        disp(99,9,0,[(SeasonLight,),tuple(SeasonBlanking)])

        # get the sun times in a dict
        sun = Sun.SunTimes(NOW.year,NOW.month,NOW.day,LOCATION[0],LOCATION[1])

        # set the sun times into various variables
        sunrise = TimeCalc.Hrs(sun['Official'][0])
        sunset = TimeCalc.Hrs(sun['Official'][1])

        civil_start = TimeCalc.Hrs(sun['Civil'][0])
        civil_end = TimeCalc.Hrs(sun['Civil'][1])

        solar_day = TimeCalc.Hrs(sun['Official'][1] - sun['Official'][0])
        
        # tomorrow could be another month or year - so add a day within the datetime object
        TOMORROW = NOW + dt.timedelta(days=+1)
        
        sun_tomorrow = Sun.SunTimes(TOMORROW.year,TOMORROW.month,TOMORROW.day,LOCATION[0],LOCATION[1])

        night_length = TimeCalc.Hrs((sun_tomorrow['Official'][0] + 24) - sun['Official'][1])

        print(night_length)

        solar_noon = TimeCalc.Hrs((sun['Official'][1] + sun['Official'][0])/2)

        moon_time_rise = MoonTime(NOW.year,NOW.month,NOW.day,LOCATION[0],-LOCATION[1],"Rise")

        moon_time_set = MoonTime(NOW.year,NOW.month,NOW.day,LOCATION[0],-LOCATION[1],"Set")


        # moonphase
        moon_phases = Phase(NOW.year + (NOW.day / 365))
    
        #print(moon_phases)        

        # convert phases to JulianDays - this makes it easier to compare against the moon phase times
        JD_moon_phase = []
        for i in moon_phases:
            moon_phases[i] = JulianDay(moon_phases[i][0],moon_phases[i][1],moon_phases[i][2])
        
        # order the phases as they could be in the wrong cronological order - remember, phases are cyclical    
        ordered_phases = {k:v for k,v in sorted(moon_phases.items(), key = lambda item: item[1])}

        #print(ordered_phases)
        
        # convert today's date to Julian day
        JD_today = JulianDay(NOW.year,NOW.month,NOW.day)
        
        #print(JD_today)

        # iterate through each phase and compare it, they are in order, so where we get a change of logic (> then <, we have found the phase between the cardinal phases)

        for i in ordered_phases:
            #print(i)
            if JD_today == ordered_phases[i]: # day is equal to a cardinal phase
                phase = i
            elif JD_today > ordered_phases[i]: # phase is in the future
                pass
            else: # phase is in the past; 
                phase = Half_phase[i]

        #print(phase)     


        MoonLight = Phases[phase]
        MoonBlanking = []

        for i in range(0,8):
            if MoonLight != i:
                MoonBlanking.append(i)

        disp(99,12,0,[(MoonLight,),tuple(MoonBlanking)])
            

        #if JD_today == 

        #print(moon_time_rise)

    #######################################
    ## everything below runs every second
    
    # get sensor data
    bme280_data = bme280.sample(bme280_bus,bme280_address,bme280_calibration_params)
    #print("Temp: ",round(bme280_data.temperature,1), "deg Humidity: ", round(bme280_data.humidity,0), "% Pressure: ",round(bme280_data.pressure,0))

    #print(NOW.strftime('%H:%M:%S %a %d-%m-%y'))
    

    # to display it, they need to be in a zero-padded list so that the digits can be iterated over

    temperature = bme280_data.temperature
    humidity = bme280_data.humidity

    bme_t = [int(x) for x in f"{int(math.trunc(temperature)):02d}"]
    #print(temperature)
    # get decimals
    temperature_decimals = math.trunc((temperature - math.trunc(temperature))*100)
    #print(temperature_decimals)
    bme_tdec = [int(x) for x in f"{int(temperature_decimals):02d}"]

    #print(bme_tdec)

    bme_h = [int(x) for x in f"{int(math.trunc(humidity)):02d}"]

    humidity_decimals = math.trunc((humidity - math.trunc(humidity))*100)
    bme_hdec = [int(x) for x in f"{int(humidity_decimals):02d}"]

    
    bme_p = [int(x) for x in f"{int(round(bme280_data.pressure,0)):04d}"]
    #print(bme_p)


    hr = [int(x) for x in f"{NOW.hour:02d}"]
    mn = [int(x) for x in f"{NOW.minute:02d}"]
    sc = [int(x) for x in f"{NOW.second:02d}"]

    dy = [int(x) for x in f"{NOW.day:02d}"]
    mt = [int(x) for x in f"{NOW.month:02d}"]
    
    yr = [int(x) for x in f"{NOW.year:02d}"]

    sunrise_hr = [int(x) for x in f"{sunrise[0]:02d}"]
    sunrise_mn = [int(x) for x in f"{sunrise[1]:02d}"]

    sunset_hr =  [int(x) for x in f"{sunset[0]:02d}"]
    sunset_mn =  [int(x) for x in f"{sunset[1]:02d}"]

    civil_start_hr = [int(x) for x in f"{civil_start[0]:02d}"]
    civil_start_mn = [int(x) for x in f"{civil_start[1]:02d}"]

    civil_end_hr =  [int(x) for x in f"{civil_end[0]:02d}"]
    civil_end_mn = [int(x) for x in f"{civil_end[1]:02d}"]

    solar_noon_hr = [int(x) for x in f"{solar_noon[0]:02d}"]
    solar_noon_mn = [int(x) for x in f"{solar_noon[1]:02d}"]

    #print(solar_noon_mn)

    solar_day_hr = [int(x) for x in f"{solar_day[0]:02d}"]
    solar_day_mn = [int(x) for x in f"{solar_day[1]:02d}"]

    night_hr = [int(x) for x in f"{night_length[0]:02d}"]
    night_mn = [int(x) for x in f"{night_length[1]:02d}"]

    # moon times - these may not happen in the day, so check and correct for it

    if moon_time_rise == False:
        moon_rise_hr = [23,23]
        moon_rise_mn = [23,23]
    else:
        moon_rise_hr = [int(x) for x in f"{moon_time_rise[0]:02d}"]
        moon_rise_mn = [int(x) for x in f"{moon_time_rise[1]:02d}"]

    if moon_time_set == False:
        moon_set_hr = [23,23]
        moon_set_mn = [23,23]
    else:
        moon_set_hr = [int(x) for x in f"{moon_time_set[0]:02d}"]
        moon_set_mn = [int(x) for x in f"{moon_time_set[1]:02d}"]

    # update status LEDs

    # day of week
    DoW = NOW.weekday()
    DoWBlanking = []
    

    #create blanking list
    for i in range(0,8):
        if DoW != i:
            DoWBlanking.append(i)

    #print(tuple(DoWBlanking))

    disp(99,8,0,[(DoW,),tuple(DoWBlanking)])
    #disp(99,8,0,[(0,),(1,2,3,4,5,6,7)])

    # GMT / BST
    disp(99,11,0,[(0,),(1,)])
    

    # display loop
    for i in [1,0]:

        # Sunrise/Set - rotate information on display; display for secs each


        # Sun and Moon cycle

        # use a counter as 16 displays doesn't nicely fit into 60 seconds, but does in 240, and 6 fits nicely in 240 too.
        #print("c mod 16:",c % 16,"c:",c)

        if c % 16 == 0:         
            # Dawn --

            # leds
            disp(99,10,0,[(0,),(1,2,3,4,5,6,7)])

            disp(civil_start_hr[i], 0+i,0)
            disp(civil_start_mn[i], 2+i,0)


        elif c % 16 == 2:
            # -- Dusk

            # leds
            disp(99,10,0,[(1,),(0,2,3,4,5,6,7)])

            disp(civil_end_hr[i], 0+i,0)
            disp(civil_end_mn[i], 2+i,0)


        elif c % 16 == 4:
            # -- Sunrise
            # leds
            disp(99,10,0,[(2,),(0,1,3,4,5,6,7)])
          
            disp(sunrise_hr[i], 0+i,0)
            disp(sunrise_mn[i], 2+i,0)


        elif c % 16 == 6:
            # Sunset --

            # leds
            disp(99,10,0,[(3,),(0,1,2,4,5,6,7)])

            disp(sunset_hr[i], 0+i,0)
            disp(sunset_mn[i], 2+i,0)


        elif c % 16 == 8:
            # moonrise
    
            # leds
            disp(99,10,0,[(4,),(0,1,2,3,5,6,7)])

            #placeholder
            disp(moon_rise_hr[i],0+i,0)
            disp(moon_rise_mn[i],2+i,0)

        elif c % 16 == 10:
            # moonset

            # leds
            disp(99,10,0,[(5,),(0,1,2,3,4,6,7)])

            #placeholder
            disp(moon_set_hr[i],0+i,0)
            disp(moon_set_mn[i],2+i,0)
        
        elif c % 16 == 12:
            # - Day length -
            # leds
            disp(99,10,0,[(6,),(0,1,2,3,4,5,7)])

            disp(solar_day_hr[i],0+i,0)
            disp(solar_day_mn[i],2+i,0)

        elif c % 16 == 14:
            #night length
            # leds
            disp(99,10,0,[(7,),(0,1,2,3,4,5,6)])

            disp(night_hr[i],0+i,0)
            disp(night_mn[i],2+i,0)

       
        

        # temperature, humidity and pressure cycle
        if c % 6 == 0:
            disp(bme_t[i], 4+i,0)
            #print(bme_tdec[i])
            add_dot(5,0)
            disp(bme_tdec[i],6+i,0)

            disp(99,11,0,[(2,),(3,4,5,6,7)])

        elif c % 6 == 2:           
            disp(bme_h[i], 4+i,0)
            add_dot(5,0)
            disp(bme_hdec[i],6+i,0)

            disp(99,11,0,[(3,),(2,4,5,6,7)])

        elif c % 6 == 4:

            disp(bme_p[i],4+i,0)
            disp(bme_p[i+2],6+i,0)
            disp(99,11,0,[(4,),(2,3,5,6,7)])     
            
        
        # add blinking dots to time
        if c % 2 == 0:
            add_dot(1,1)
            add_dot(3,1)
            add_dot(5,1)            


        # Time5
        disp(hr[i], 0+i,1)
        disp(mn[i], 2+i,1)
        disp(sc[i], 4+i,1)

        # Date
        disp(dy[i], 8+i,1)
        disp(mt[i], 10+i,1)
        disp(yr[i+2], 12+i,1)

    # add one to the counter, and re-cycle at 240.
    c += 1
    c %= 240 

    # add dots to date, and cycle times
    add_dot(9,1)
    add_dot(11,1)
    add_dot(1,0)
    
    # update display once all the buffers are filled

    dispupdate(1)
    dispupdate(0)



