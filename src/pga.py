from numpy import uint8
import smbus2
import settings
import calculations

# constants
PGA_ADDR = 0x22
PGA_REG = 0x09

# file for i2c
i2c = smbus2.SMBus(1)

# variables
global pga_amp
pga_amp = 7

def Init():
	#send empty init
	i2c.write_byte_data(PGA_ADDR,0x00,0x00)

	#send config and start Gain
	i2c.write_byte_data(PGA_ADDR,PGA_REG,uint8(pga_amp))


def adjust_gain(gain_adjust):
	global pga_amp
	if(((pga_amp < 7) and (gain_adjust == 1)) or ((pga_amp > 1) and (gain_adjust == -1))):
		pga_amp = pga_amp + gain_adjust
		i2c.write_byte_data(PGA_ADDR,PGA_REG,uint8(pga_amp))
	
	if(settings.DEBUG == True):
		print("PGA-Level = " + str(pga_amp))