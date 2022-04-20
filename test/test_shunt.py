"""	This file is used to test the shunt IC. 
	The buttons 1,2 and 3 change the gain at the shunt processing IC."""

#  add used librarys
import smbus2
import time

# variables
idle_time = 0.5
btn1 = 0b00000001
btn2 = 0b00000010
btn3 = 0b00000100

i2c = smbus2.SMBus(1)

# i2c address of the I/O expander
io3 = 0x22	# shunt I/O expander
io4 = 0x23	# button I/O expander

# MCP23008 register address
mcp_conf_reg = 0b00000000
mcp_gpio_reg = 0b00001001

# MCP23008 configuration values
mcp_set_gpio_out = 0b00000000 # Configure all pins as output
mcp_set_gpio_in = 0b11111111 # Configure all pins as input

# translation array between MCP23008 and shunt processing
shunt_gain = [0b00000000, 0b00001000, 0b00010000, 0b00011000]

# initialisation and configuration of the I/O expander
i2c.write_byte_data(io3, mcp_conf_reg, mcp_set_gpio_out)	# Configure all pins as output
i2c.write_byte_data(io4, mcp_conf_reg, mcp_set_gpio_in)	# Configure all pins as output

# write initial gain value
i2c.write_byte_data(io3, mcp_gpio_reg, shunt_gain[0])	# set gain to 0

try:
	print("Ctrl C beendet das Programm.")
	while True:
		a = i2c.read_byte_data(io4, mcp_gpio_reg)
		if (a & btn1) == btn1:
			i2c.write_byte_data(io3, mcp_gpio_reg, shunt_gain[1])	# set gain to 1
			print("Shunt gain set to 1")
		elif (a & btn2) == btn2:
			i2c.write_byte_data(io3, mcp_gpio_reg, shunt_gain[2])	# set gain to 2
			print("Shunt gain set to 2")
		elif (a & btn3) == btn3:
			i2c.write_byte_data(io3, mcp_gpio_reg, shunt_gain[3])	# set gain to 3
			print("Shunt gain set to 3")
		
		time.sleep(idle_time)

except KeyboardInterrupt:
	i2c.write_byte_data(io3, mcp_gpio_reg, 0x00)
	print("\nDas Programm wird beendet...")