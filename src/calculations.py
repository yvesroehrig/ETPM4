# File for the processing of the measured Data

# Imports
import numpy as np
from scipy.fft import fft, fftshift, fftfreq
from scipy.signal import hann, butter, filtfilt, lfilter
from scipy import signal
import matplotlib.pyplot as plt

import settings

# Constants
fc = 24e9
c = 3e8
ld = c/fc

# Initialisation for the calculations
def Init():
    # Calculating measuring Parameters
    global wFs,DT,TS
    wFs = settings.Fs*2*np.pi    # circular sampling frequency
    DT = 1/settings.Fs           # Time per sample
    TS = DT*settings.N_Samp       # Sampling time

    if settings.DEBUG == True:
        print("Number of samples: " + str(settings.N_Samp))
        print("Sampling frequency: " + str(settings.Fs))
        print("circular sampling frequency: " + str(wFs))
        print("Time per sample: " + str(DT))
        print("Sampling Time: " + str(TS))

    # calculate the digital filter
    global b,a
    b,a = butter(10, np.multiply([400, 5000], 2*np.pi), btype="band", fs=(settings.Fs*2*np.pi), output='ba', analog=False)
    if settings.DEBUG == True:
        w,h = signal.freqz(b,a, worN=settings.N_Samp,fs=wFs)
        plt.semilogx(w/(2*np.pi),20*np.log10(abs(h)))
        plt.title('Butterworth filter frequency response')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude [dB]')
        plt.grid(which='both', axis='both')
        plt.margins(0, 0.1)
        plt.axvline(400, color='green') # highpass frequency
        plt.axvline(5000, color='green') # lowpass frequency
        plt.legend(["Frequency response","Pass Band"])
        plt.savefig("/home/pi/ETPM4/html/images/Filter.png", dpi=150)
        print("Filter plot saved")
    
    # create the window
    global window
    window = hann(settings.N_Samp, sym=True)
    if settings.DEBUG == True:
        plt.plot(window)
        plt.title("Hanning Window")
        plt.xlabel("Sample Number")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.savefig("/home/pi/ETPM4/html/images/Window.jpg", dpi=150)
        print("Window plot saved")