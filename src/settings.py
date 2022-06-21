# global parameters
DEBUG       = True     # Debug on/off
DEMO        = False     # Demo on/off
SPEED_GRAPH = True      # Speed graph on/off
Fs          = 9000      # Sampling frequency
N_Samp      = 1024      # Number of Samples for the FFT
N_Samp_I_B  = 100       # Number of Samples for the current and brightness measurement
Filt_ord    = 10        # Order of the digital filter
f_band_low  = 400       # Lower frequency for bandpass
fft_thershold = 0.01    # Thershold for the FFT
min_sig_pga = 200       # When signal peak to peak is below this value the amplification gets increased
max_sig_pga = 4000      # Amplitude for clipping
img_res     = 150       # resulution of plots in dpi

# Display settings
FLASH_TIME		= 1		# Flashing time in seconds when speed exceeded
PWM_PIN			= 12	# referece at gpio pinout diagram
PWM_FREQUENCY	= 200	# Hz
TEST_SLEEP_TIME = 0.8   # s
