# File for the processing of the measured Data

# Imports
import numpy as np
from scipy.fft import fft
from scipy.signal import hanning
import matplotlib.pyplot as plt

# Demo mode (1=ON/0=OFF)
demo = 1
# Parameter
N_FFT = 256     # Number of measuring points 
FS = 14000      # Sampling frequency
DT = 1/FS       # Time per sample
TS = DT*N_FFT   # Sampling time


if demo == 1:
    # demo signal
    f1 = 200        # Frequency for the demo signal
    w = 2*np.pi*f1  # circular frequency
    A = 0.100
    t = np.linspace(0,TS,256)   # time vector
    y = A*np.sin(w*t) # Signal

    plt.plot(t,y)
    plt.show()
else:
    # Import measurement data
    y = 1


# Multiplying with the hanning window
y_w = y*hanning(256)
FFT=fft(y_w)

if demo == 1:
    plt.plot(FFT,256)
    plt.show()
