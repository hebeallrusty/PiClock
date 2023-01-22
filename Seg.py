import board
#from adafruit_ht16k33.segments import Seg7x4
from adafruit_ht16k33 import matrix
from time import sleep

i2c = board.I2C()

matrix = matrix.Matrix16x8(i2c,address = 0x70)

matrix.fill(0)
matrix.brightness = 0.1


# something isn't right about this code - it works, but not in the way that it should, or that is expected based on the wiring. The matrix may be the wrong way around!!'

def glyph(g):
    # return an tuple with the digits to set as on for the glyph it represents. Not to be called directly, but through a function. It won't explode, but it'll only default producing glyphs that'll work on the first cluster on a cathode, which can hold 2nr'
    if g == 1:
        return (1,2)
    elif g == 2:
        return (0,1,6,4,3)
    elif g == 3:
        return (0,1,6,2,3)
    elif g == 4:
        return (5,6,1,2)
    elif g == 5:
        return (0,5,6,2,3)
    elif g == 6:
        return (0,5,4,3,2,6)
    elif g == 7:
        return (0,1,2)
    elif g == 8:
        return (0,1,2,3,4,5,6)
    elif g == 9:
        return (0,5,6,1,2,3)
    elif g == 0:
        return (0,1,2,3,4,5)
    elif g == 11:
        return (7,)
    else:
        return (0,5,6,4,3)

def antiglyph(g):
    # for blanking out segments that aren't part of the glyph needed so that whole display doesn't need blanking - eliminates blinking where the whole display updates'
    if g == 1:
        return (0,3,4,5,6,7)
    elif g == 2:
        return (2,5,7)
    elif g == 3:
        return (4,5,7)
    elif g == 4:
        return (0,4,3,7)
    elif g == 5:
        return (1,4,7)
    elif g == 6:
        return (1,7)
    elif g == 7:
        return (5,6,4,3,7)
    elif g == 8:
        return (7,)
    elif g == 9:
        return (4,7)
    elif g == 0:
        return (6,7)
    elif g == 11:
        return (1,2,3,4,5,6)
    else:
        return (0,5,6,4,3)
    

def column(c,g):
    # each cathode on the ht16k33 can hold 2nr clusters, (one on A0 - A7;the second on A8 A15. All glyphs are for A0 - A7; this shifts them over to A8 - A15)
    # alter each glyph to suit column 1 or column 2 (A0 - A7 or A8 - A15)
    # c is the cluster - 0 for A0 - A7; 1 for A8 - A15 AKA the column
    # g is the actual glyph to display

    #print(c,":",g)

    # get the glyph to display
    t = glyph(g)
    u = antiglyph(g)

    #print([t,u])

    # glyph needs to be transposed into the correct cluster
    if c == 0:
        return [t,u]
    elif c == 1:
        # each glyph just needs shifted by 8 rows for the second cluster on each cathode
        #print([tuple([z + 8 for z in t]), tuple([x + 8 for x in u])])
        return [tuple([z + 8 for z in t]), tuple([x + 8 for x in u])]
    else:
        return [t,u]

def display(n,coords):
    # n is a 2 digit number as displays are 2 digits. Zero padding will be taken care of.
    # coords should be in the form (r,c) as noted below
    # r is cathode tuple (internal wiring of display has each 2 digit with 2 cathodes which select the left or right segment to display on; each bar of the anode are wired together i.e. bar a for both the left and right digit share one wire) AKA the ROW (0 - 4)
    # c is the anode i.e. the left or right cluster for each cathode AKA the COLUMN (0 - 1)

    (r,c) = coords
    #print(r)
    #print(c)

    # pad the number with zero's and convert to string
    npad = f'{n:02d}'
    
    #empty display - THIS MAY NEED REMOVING WHEN EXTRA DIGITS ARE ADDDED
    #matrix.fill(0)    
    
    #print(npad)
    # iterate over the digits, get the glyph, correct it and then allow it to be displayed
    for i in range(0,2):
        # get the corrected glyph depending on the column
        g = column(c,int(npad[i]))
        # iterate over the glyph bars and display it
        for j in g[0]:
            matrix[2 * r + i, j] = 1
        # blank out those glyph bars that aren't relevant with the antiglyph'
        for j in g[1]:
            matrix[2 * r + i, j] = 0
    # small hack to make the hour / minute decimal points appear    
    matrix[1,7] =1
    matrix[3,7] = 1
    


#display(5,(5,0))
#for i in range(0,8):
#    for j in range(0,17):
#        matrix[j,i]=1
#        sleep(0.1)

#
##
# matrix[c,a] where c = cathode (digit); a = anode (segment)

#matrix[8,0]=1
#matrix[8,1]=1

#while True:
#    display(64,(0,0))
#    #matrix[0,6]=0
#    sleep(0.5)




