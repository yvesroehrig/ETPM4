#  add used librarys
import smbus2
import RPi.GPIO as GPIO
#import numpy as np
import settings
import time

# global variables
global toggle
toggle = False
global isvalue
isvalue = 0
global reftime
reftime = 0

# variables
#pwm_pin = 12 # referece at gpio pinout diagram
#pwm_frequency = 500	# Hz

# setup GPIO for pwm
GPIO.setmode(GPIO.BCM)
GPIO.setup(settings.PWM_PIN, GPIO.OUT)

p = GPIO.PWM(settings.PWM_PIN, settings.PWM_FREQUENCY)
p.start(0)

# create an i2c instance when file is in script mode
#if __name__ == "__main__":

i2c = smbus2.SMBus(1)

# i2c address of the seven segment displays
display_10e0 = 0x21	# 1s digit
display_10e1 = 0x20	# 10s digit

# MCP23008 register address
mcp_conf_reg = 0b00000000
mcp_gpio_reg = 0b00001001

# MCP23008 configuration values
mcp_set_gpio_out = 0b00000000

# translation array between MCP23008 and segment displays
segment = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110, 0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111]

# seperation of the decimals
def Digit(number, digit):
	temp = number % (digit * 10)
	return int(temp / digit)

# initialisation and configuration of the I/O expander
def Init():
	i2c.write_byte_data(display_10e0, 0x00, 0x00)	# Configure all pins as output
	i2c.write_byte_data(display_10e1, 0x00, 0x00)	# Configure all pins as output

# set all outputs high to test each segment
def Test():
	i2c.write_byte_data(display_10e0, mcp_gpio_reg, 0xFF)	# set all outputs high
	i2c.write_byte_data(display_10e1, mcp_gpio_reg, 0xFF)	# set all outputs high

# write new value to the segment displays
def Set(set_value):
	global isvalue
	# write the current value only on the displays if it differs from the previous one
	if(isvalue != set_value):
		i2c.write_byte_data(display_10e0, mcp_gpio_reg, segment[Digit(set_value, 1)])	# display value on the 10e0 digit
		i2c.write_byte_data(display_10e1, mcp_gpio_reg, segment[Digit(set_value, 10)])	# display value on the 10e1 digit
		isvalue = set_value

# dimm the segments
def Dimm(dimm, flash=False):
	global toggle
	global reftime
	if(flash):
		# toggle display on and off
		if(toggle):
			if((time.time() - reftime) >= settings.FLASH_TIME):
				p.ChangeDutyCycle(0)
				reftime = time.time()
				toggle = not toggle
		else:
			if((time.time() - reftime) >= settings.FLASH_TIME):
				p.ChangeDutyCycle(dimm)
				reftime = time.time()
				toggle = not toggle

	else:
		p.ChangeDutyCycle(dimm)

def AmbientLightControl(adcValue):
	maxPWMvalue = 100 # in %
	maxADCvalue = 4500 # in mV

	# segment to ambient light linear
	PWMvalue = (maxPWMvalue/maxADCvalue)*adcValue

	# segment to ambient light exponential
	# PWMvalue = maxPWMvalue * (1 - np.exp(-(1/maxADCvalue)*adcValue))

	return PWMvalue
