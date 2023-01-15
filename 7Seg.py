import board
from adafruit_ht16k33.segments import Seg7x4
from time import sleep

i2c = board.I2C()
display = Seg7x4(i2c,address = 0x70)

for i in range(0,2):
    for j in range(0,10):
        display[i]=str(j)
        sleep(0.5)

display[0]=' '
display[1]=' '
#display.set_digit_raw(1,0b10000000)

