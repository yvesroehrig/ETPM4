# This is the main file of the project

#  add used librarys
#import smbus2    # python i2c library for the raspberry pi

# add used files
import display
import calculations
import settings

# test variables
test_value = 12

# create an i2c instance
#i2c = smbus2.SMBus(1)

# initialisation of the system
display.Init()
calculations.Init()

# infined loop
while(1):
    display.Set(test_value)
    display.Dimm(50)

    # Measurement and calculation of speed
    speed = calculations.GetSpeed()
    intspeed = int(speed)
    display.Set(intspeed)