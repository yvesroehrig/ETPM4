#  add used librarys
import smbus2
import time

# variables
idle_time = 1

i2c = smbus2.SMBus(1)

# i2c address of the button I/O expander
buttons = 0x23	# button I/O expander

# MCP23008 register address
mcp_conf_reg = 0b00000000
mcp_gpio_reg = 0b00001001

# MCP23008 configuration values
mcp_set_gpio_in = 0b11111111 # Configure all pins as input

i2c.write_byte_data(buttons, mcp_conf_reg, mcp_set_gpio_in)	# Configure all pins as output

try:
	print("Ctrl C beendet das Programm.")
	while True:
		a = i2c.read_byte_data(buttons, mcp_gpio_reg)
		print(a)
		time.sleep(idle_time)
except KeyboardInterrupt:
	print("\nDas Programm wird beendet...")