# global parameters
from socket import TCP_NODELAY
from wsgiref.simple_server import demo_app

DEBUG       = False  # Debug on/off
DEMO        = False  # Demo on/off
Fs          = 9000 # Sampling frequency
N_Samp      = 1024   # Number of Samples
Filt_ord    = 10    # Order of the digital filter
f_band_low  = 400  # Lower frequency for bandpass
f_band_high = Fs/2 # Higher frequency for bandpass at half 

# Display settings
FLASH_TIME		= 1		# Flashing time in seconds when speed exceeded
PWM_PIN			= 12	# referece at gpio pinout diagram
PWM_FREQUENCY	= 500	# Hz
