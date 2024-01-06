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
    SegMatrix[i].brightness = 0.1
    SegMatrix[i].show()

# switch on everything    
#for i in [0,1]:
#    for j in range(0,16):
#        for k in range (0,8):
#            SegMatrix[i][j,k] = 1
#            SegMatrix[i].show()
            #sleep(0.05)

for i in range(4,16):
    for j in range(0,8):
        print(i,j)
        SegMatrix[0][i,j] = 1
        SegMatrix[0].show()
        sleep(0.5)

#SegMatrix[0][11,2] = 1
#SegMatrix[0].show()

# (8,0) is Day of week
# (9,0) is Season
# (10,0) is Sun/Moon
# (11,0) is TimeZone
# (11,2) is Temp/Humid/Press
# (12,0) is Moon Phase

