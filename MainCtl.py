
print("Loading modules")
import datetime as dt
import time as tm
from Sun import Sun
from Moon import Moon
import configparser


print("Initilising")
# initialisation of loop

# Initialise config file for reading
# set up object Config which will all options to be read from file
CONFIG_FILE="Config.ini"
Config = configparser.ConfigParser()
Config.read(CONFIG_FILE)

# Get location for sunrise / set times
LOCATION = [float(Config.get('LOCATION','latitude')),float(Config.get('LOCATION','longitude'))]

print(LOCATION)


while True:
    
    # get time and store it to be used throughout the loop to prevent the rare potential where the date changes by the time the loop completes
    NOW = dt.datetime.now()
    today = dt.datetime(NOW.year,NOW.month,NOW.day,0,0,0)


    s = Sun(NOW,LOCATION,0)
    m = Moon(NOW)
    sunrise = today + s.Rise()['Official']
    sunset = today + s.Set()['Official']
    print("SunRise: ",sunrise.hour,":",sunrise.minute,"; SunSet: ",sunset.hour,":",sunset.minute)
    print("Moon: ",m.MoonPhase())
    print(NOW.strftime('%I:%M:%S %a %d-%m-%y'))
    
    


    tm.sleep(0.5)
