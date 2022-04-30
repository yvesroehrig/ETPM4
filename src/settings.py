# global parameters
from socket import TCP_NODELAY
from wsgiref.simple_server import demo_app


DEBUG			= True	# Debug on/off
DEMO			= True	# Demo on/off
Fs				= 14000	# Sampling frequency
N_Samp			= 1024	# Number of Samples
Filt_ord		= 10	# Order of the digital filter

# Display settings
FLASH_TIME		= 1		# Flashing time in seconds when speed exceeded
PWM_PIN			= 12	# referece at gpio pinout diagram
PWM_FREQUENCY	= 500	# Hz
