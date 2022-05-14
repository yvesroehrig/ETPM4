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
		brightness, current = calculations.get_I_B()
		brightness = int(brightness)
		current = int(current)

		# get button state
		button.GetInput()

        # check for amplifications
		if(speed == 999):
			# set PGA 1 level lower
			pga.adjust_gain(-1)
		elif(speed == -999):
			# set PGA 1 level higher
			pga.adjust_gain(1)
		else:
			# display measured speed at display
			display.Set(intspeed)

			if(button.GetSpeedLimit() < intspeed):
				display.Dimm(50, True)
			else:
				display.Dimm(50, False)

			time.sleep(1)
			print("Brightness:\t%4d" % (brightness))
			print("Current:\t%4d" % (current))

except KeyboardInterrupt:
	display.Deinit()
	print("\nDas Programm wird beendet...")
