# return what season is currently in effect based on the date

import datetime as dt

# define the standard outputs
tSpring = "Spring"
tSummer = "Summer"
tAutumn = "Autumn"
tWinter = "Winter"

# get the definition of seasons which is held in the config file

def Season(oNow,SeasonDef="Astronomical"):
    # SeasonDef - Astronomical for seasons in alignment with the equinoxes / solstaces
    #           - Meteorological for seasons at the start of the months)
    # oNow - the date to check - as a datetime object

    if SeasonDef == "Astronomical":
        Spring = dt.datetime(oNow.year,3,20)
        Summer = dt.datetime(oNow.year,6,21)
        Autumn = dt.datetime(oNow.year,9,23)
        Winter = dt.datetime(oNow.year,12,22)
    else:
        Spring = dt.datetime(oNow.year,3,1)
        Summer = dt.datetime(oNow.year,6,1)
        Autumn = dt.datetime(oNow.year,9,1)
        Winter = dt.datetime(oNow.year,12,1)

    Start = dt.datetime(oNow.year,1,1)
    End = dt.datetime(oNow.year,12,31)

    
    # check which season the months fall in
    
    if Start <= oNow < Spring:
        return tWinter
    elif Spring <= oNow < Summer:
        return tSpring
    elif Summer <= oNow < Autumn:
        return tSummer
    elif Autumn <= oNow < Winter:
        return tAutumn
    elif Winter <= oNow <= End:
        return tWinter
     
