#  add used librarys
import smbus2
import time

# variables
idle_time = 10

i2c = smbus2.SMBus(1)

# i2c address of the I/O expander
io3 = 0x22	# Variable gain I/O

# MCP23008 register address
mcp_conf_reg = 0b00000000
mcp_gpio_reg = 0b00001001

# MCP23008 configuration values
mcp_set_gpio_out = 0b00000000

# translation array between MCP23008 and segment displays
gain = [0b00000000, 0b00000001, 0b00000010, 0b00000011, 0b00000100, 0b00000101, 0b00000110, 0b00000111]

# initialisation and configuration of the I/O expander
i2c.write_byte_data(io3, 0x00, 0x00)	# Configure all pins as output

# write new value to the segment displays
i2c.write_byte_data(io3, mcp_gpio_reg, gain[0])	# set gain to 0

try:
	print("Ctrl C beendet das Programm.")
	time.sleep(idle_time)
	while True:
		i2c.write_byte_data(io3, mcp_gpio_reg, gain[1])	# set gain to i
except KeyboardInterrupt:
	i2c.write_byte_data(io3,0x09,0x00)
	print("\nDas Programm wird beendet...")