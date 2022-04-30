# global parameters
from wsgiref.simple_server import demo_app


DEBUG       = True  # Debug on/off
DEMO        = True  # Demo on/off
Fs          = 9000 # Sampling frequency
N_Samp      = 1024   # Number of Samples
Filt_ord    = 10    # Order of the digital filter
f_band_low  = 400  # Lower frequency for bandpass
f_band_high = Fs/2 # Higher frequency for bandpass at half 
