# This is the main file of the project

#  add used librarys
#import smbus2    # python i2c library for the raspberry pi

# add used files
import display
import button
#import calculations
import settings
import time

# test variables
test_value = 65

# create an i2c instance
#i2c = smbus2.SMBus(1)

try:
	# initialisation of the system
	display.Init()
	button.Init()
	#calculations.Init()

	display.Dimm(100, False)
	display.Test()
	time.sleep(2)

	# infined loop
	while(1):
		# Measurement and calculation of speed
		# speed = calculations.GetSpeed()
		# intspeed = int(speed)

		# get button state
		button.GetInput()

		# display measured speed at display
		display.Set(test_value)

		if(button.GetSpeedLimit() < test_value):
			display.Dimm(50, True)
		else:
			display.Dimm(50, False)

		time.sleep(0.5)

except KeyboardInterrupt:
	display.Deinit()
	print("\nDas Programm wird beendet...")