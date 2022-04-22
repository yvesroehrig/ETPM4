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

adc1_ch0_1 = [0] * 1024
adc1_ch0_2 = [0] * 1024

try:
	print("Ctrl C beendet das Programm.")
	while True:

		i2c.write_byte(adc_1, conf_ch0)	# Select chanel 0
		
		start = time.time()
		
		#for i in range(0, 1024, 1):
		adc1_ch0 = map((i2c.read_word_data(adc_1, 0)))
		
		end = time.time()

		adc1_ch0_2 = list(adc1_ch0)

		for i in range(0, 1024, 1):
			adc1_ch0_2[i] = (adc1_ch0_2[i] / ((2**16)-1)) * vref

		print("ADC1 CH0 M1: %4.1fmV" % (adc1_ch0[0]*1000))
		print("ADC1 CH0 M2: %4.1fmV" % (adc1_ch0[500]*1000))
		print("Messzeit: %4.4f" % ((end - start)*1000))

		time.sleep(idle_time)

except KeyboardInterrupt:
	print("\nDas Programm wird beendet...")

