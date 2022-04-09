# This file controles the adcs over i2c

# add used librarys
import smbus	# python i2c library for the raspberry pi

# variables

# create an i2c instance when file is in script mode
# if __name__ == "__main__":
	
i2c = smbus.SMBus(1)

# i2c address of the adcs
adc1 = 0b0001000
adc2 = 0b0001010
adc_global = 0b1101011

# LTC2301 register address
mcp_conf_reg = 0b00000000
mcp_gpio_reg = 0b00001001