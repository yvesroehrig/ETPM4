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
	time.sleep(2)

	# infined loop
	while(1):
    # Measurement and calculation of speed
    speed = calculations.GetSpeed()
    intspeed = int(speed)

		# get button state
		button.GetInput()

		# display measured speed at display
		display.Set(intspeed)

		if(button.GetSpeedLimit() < intspeed):
			display.Dimm(50, True)
		else:
			display.Dimm(50, False)

		time.sleep(1)

except KeyboardInterrupt:
	display.Deinit()
	print("\nDas Programm wird beendet...")
