# add used librarys
import smbus2
import time

# variables
idle_time = 3
vref = 2.5

i2c = smbus2.SMBus(1)

# i2c address of the ADCs
adc_1 = 0x08
adc_2 = 0x09
adc_global = 0x6B

# LTC2305 configuration values
conf_ch0 = 0x80 # Configure analog mux to chanel 0
conf_ch1 = 0xC0 # Configure analog mux to chanel 1

try:
	print("Ctrl C beendet das Programm.")
	while True:

		# ADC1 CH0
		i2c.write_byte(adc_1, conf_ch0)	# Select chanel 0
		adc1_ch0 = (i2c.read_word_data(adc_1, 0) / ((2**16)-1)) * vref
		#adc1_ch0 = i2c.read_word_data(adc_1, 0xC0) / ((2**16)-1)

		# ADC1 CH1
		i2c.write_byte(adc_1, conf_ch1)	# Select chanel 1
		adc1_ch1 = (i2c.read_word_data(adc_1, 0) / ((2**16)-1)) * vref

		# ADC1 CH0
		i2c.write_byte(adc_2, conf_ch0)	# Select chanel 0
		adc2_ch0 = (i2c.read_word_data(adc_2, 0) / ((2**16)-1)) * vref

		# ADC2 CH1
		i2c.write_byte(adc_2, conf_ch1)	# Select chanel 1
		adc2_ch1 = (i2c.read_word_data(adc_2, 0) / ((2**16)-1)) * vref
		
		print("ADC1 CH0: %4.1fmV" % (adc1_ch0*1000))
		print("ADC1 CH1: %4.1fmV" % (adc1_ch1*1000))
		print("ADC2 CH0: %4.1fmV" % (adc2_ch0*1000))
		print("ADC2 CH1: %4.1fmV\n" % (adc2_ch1*1000))

		time.sleep(idle_time)

except KeyboardInterrupt:
	print("\nDas Programm wird beendet...")

