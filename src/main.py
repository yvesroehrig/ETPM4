# This is the main file of the project

# add used librarys
import time

# add used files
import display
import button
import calculations
import settings
import pga

# test variables
test_value = 65
counter = 0

try:
	# initialisation of the system
	display.Init()
	button.Init()
	calculations.Init()
	pga.Init()

  	# display test
	display.Dimm(100, False)
	display.Test()

	# infined loop
	while(1):
		# Measurement and calculation of speed
		speed = calculations.GetSpeed()
		intspeed = int(speed)

        # check for amplifications
		if(speed == 999):
			# set PGA 1 level lower
			pga.adjust_gain(-1)
		elif(speed == -999):
			# set PGA 1 level higher
			pga.adjust_gain(1)
		elif(speed == 0):
			display.Set(intspeed)
			time.sleep(0.25)
		else:
			while(counter < 100):
				# get button state
				button.GetInput()

				# display measured speed at display
				display.Set(intspeed)

				if(button.GetSpeedLimit() < intspeed):
					display.Dimm(100, True)
				else:
					display.Dimm(100, False)

				calculations.get_I_B()
				counter += 1
				time.sleep(1.5/100)
			
			counter = 0

except KeyboardInterrupt:
	display.Deinit()
	print("\nDas Programm wird beendet...")
