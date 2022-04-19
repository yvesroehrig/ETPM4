# This is the main file of the project

#  add used librarys
#import smbus2    # python i2c library for the raspberry pi

# add used files
import display
import calculations

# global parameters
DEBUG       = True  # Debug on/of
Fs          = 14000 # Sampling frequency
N_Samp      = 512   # Number of Samples
Filt_ord    = 10    # Order of the digital filter

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