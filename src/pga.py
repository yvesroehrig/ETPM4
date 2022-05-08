import smbus2
import settings
import calculations

# constants
PGA_ADDR = 0x22
PGA_REG = 0x09

# file for i2c
i2c = smbus2.SMBus(1)

def Init():
    #send empty init
    i2c.write_byte_data(PGA_ADDR,0x00,0x00)

    #send config and start Gain
    i2c.write_byte_data(PGA_ADDR,PGA_REG,0x03)


def adjust_gain():
    I_sig = calculations.I_sig
    Q_sig = calculations.Q_sig