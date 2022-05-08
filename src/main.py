# This is the main file of the project

#  add used librarys
#import smbus2    # python i2c library for the raspberry pi

# add used files
import display
import calculations
import settings
import time

# test variables
test_value = 12

# initialisation of the system
display.Init()
calculations.Init()

# initial values
display.Set(test_value)

# infined loop
while(1):
    # get adc data

    # get button state

    # display measured speed at display
    time.sleep(0.1)

    # Measurement and calculation of speed
    speed = calculations.GetSpeed()
    intspeed = int(speed)
    print(intspeed)
    display.Set(intspeed)
    display.Dimm(50, True)

    
    time.sleep(1)
