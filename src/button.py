#  add used librarys
import smbus2
import settings

# global variables
global button; button = [0,0,0,0,0,0,0,0]
global speedLimit; speedLimit = 200

# create an i2c instance
i2c = smbus2.SMBus(1)

# i2c address of the button I/O expander
buttons = 0x23

# MCP23008 register address
mcp_conf_reg = 0b00000000
mcp_gpio_reg = 0b00001001

# MCP23008 configuration values
mcp_set_gpio_in = 0b11111111 # Configure all pins as input

def Init():
	i2c.write_byte_data(buttons, mcp_conf_reg, mcp_set_gpio_in)	# Configure all pins as input

def GetInput():
	global button
	input = i2c.read_byte_data(buttons, mcp_gpio_reg)
	for i in range(8):
		button[i] = (input>>i) & 1

def GetSpeedLimit():
	global speedLimit
	global button

	if(button[0]):
		speedLimit = 20
	elif(button[1]):
		speedLimit = 30
	elif(button[2]):
		speedLimit = 50
	elif(button[3]):
		speedLimit = 80

	return speedLimit