import datetime as dt

# calculate if it is BST or GMT - 
# BST starts the last sunday in March (at 1am)and ends the last Sunday in October (at 2am)
# returns True if within this range, and false otherwise

def bst(year,month,day,hour,minute,seconds):

    march = dt.datetime(year,3,31,1,0,0)
    bst_start = march - dt.timedelta(days =(march.weekday()+1)%7)

    october = dt.datetime(year,10,31,2,0,0)
    bst_end = october - dt.timedelta(days = october.weekday()+1%7)

    if bst_start <= dt.datetime(year,month,day,hour,minute,seconds) < bst_end:
        return(True)
    else:
        return(False)

    return(False)
