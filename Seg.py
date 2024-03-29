import board

from adafruit_ht16k33 import matrix
from time import sleep

import Config

i2c = board.I2C()

# create the object which is the matrix of segments
SegMatrix = []

# iterate through all the HT16K33's in the config, and add them to a list of objects to interact with
for i in Config.HT16K33:
    SegMatrix.append(matrix.Matrix16x8(i2c,address = int(str(i),16), auto_write = False))

# clear current display and set brightness to 100%
for i in range(0,len(SegMatrix)):
    SegMatrix[i].fill(0)
    SegMatrix[i].brightness = 0.05
    

def glyph(g):
    # return an tuple with the digits to set as on for the glyph it represents. Not to be called directly, but through a function. It won't explode, but just don't do it
    # returns [glyph segments, antiglyph segments for blanking]
    #
    # glyphs are 0 for the top seg going clockwise with 7 as the decimal point. 
    # THESE ARE GLYPH INDEXS for clarity
    
    if g == 1: # 1
        return [(1,2),(0,3,4,5,6,7)]
    elif g == 2: # 2
        return [(0,1,6,4,3),(2,5,7)]
    elif g == 3: # 3
        return [(0,1,6,2,3),(4,5,7)]
    elif g == 4: # 4
        return [(5,6,1,2),(0,4,3,7)]
    elif g == 5: # 5
        return [(0,5,6,2,3),(1,4,7)]
    elif g == 6: # 6
        return [(0,5,4,3,2,6),(1,7)]
    elif g == 7: # 7
        return [(0,1,2),(5,6,4,3,7)]
    elif g == 8: # 8
        return [(0,1,2,3,4,5,6),(7,)]
    elif g == 9: # 9
        return [(0,5,6,1,2,3),(4,7)]
    elif g == 0: # 0
        return [(0,1,2,3,4,5),(6,7)]
    elif g == 11: # .
        return [(7,),(1,2,3,4,5,6)]
    elif g == 12: # [blank / space]
        return [(),(0,1,2,3,4,5,6,7)]
    elif g == 13: # b
        return [(5,4,3,2,6),(0,1,7)]
    elif g == 14: # t
        return [(5,4,3,6),(0,1,2,7)]
    elif g == 15: # I
        return [(4,5),(0,1,2,3,6,7)]
    elif g == 16: # n
        return [(2,4,6),(0,1,3,5,7)]
    elif g == 17: # s
        return [(0,5,6,2,3),(1,4,7)]
    elif g == 18: # d
        return [(1,2,3,4,6),(0,5,7)]
    elif g == 19: # c
        return [(0,3,4,5),(1,2,6,7)]
    elif g == 20: # e
        return [(0,5,6,1,4,3),(2,7)]
    elif g == 21: # r
        return [(4,6),(0,1,2,3,5,7)]
    elif g == 22: # o
        return [(6,2,3,4),(0,1,5,7)]
    elif g == 23: # -
        return[(6,),(0,1,2,3,4,5,7)]
    elif g == 24: # add dot to existing
        return[(7,),()]
    elif g == 25: # end bar |
        return[(1,2),(0,3,4,5,6,7)]
    elif g == 26: # -|
        return[(1,2,6),(0,3,4,5,7)]
    elif g == 27: # |-
        return[(4,5,6),(0,1,2,3,7)]

    else: # return an E
        return [(0,5,6,4,3),(1,2,7)]

def disp(d, bank, addr,gen=[(0,0,0,0,0,0,0,0),()]):
    # plot a glyph based on index d and display it on the bank noted,
    # gen is (if relevant) a generic glyph to operate the LEDs; d == 99 for this mode

    if d != 99:
        # get the glyphs and anti-glyphs for digit g
        g,a = glyph(d)
    else:
        g,a = gen

    #print(g,a)
    # glyphs to light
    for i in g:
        #print("on:",i)
        SegMatrix[addr][bank,i] = 1
        
    # glyphs to blank off
    for i in a:
        #print("off:",i)
        SegMatrix[addr][bank,i] = 0

def gendisp(addr,):
    SegMatrix[addr][x,y] = state

def add_dot(bank,addr):
    SegMatrix[addr][bank,7] = 1

def dispupdate(addr):
    SegMatrix[addr].show()


