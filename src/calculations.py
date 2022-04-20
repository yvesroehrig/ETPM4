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
    
    # Plot filter
    if settings.DEBUG == True:
        w,h = signal.freqz(b,a, worN=settings.N_Samp,fs=wFs)
        plt.figure(1)
        plt.semilogx(w/(2*np.pi),20*np.log10(abs(h)))
        plt.title('Butterworth filter frequency response')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude [dB]')
        plt.grid(which='both', axis='both')
        plt.margins(0, 0.1)
        plt.axvline(400, color='green') # highpass frequency
        plt.axvline(5000, color='green') # lowpass frequency
        plt.legend(["Frequency response","Pass Band"])
        plt.savefig("../html/images/Filter.jpg", dpi=150)
        plt.show()
        print("Filter plot saved")
    
    # create the window
    global window
    window = hann(settings.N_Samp, sym=True)

    # Plot window
    if settings.DEBUG == True:
        plt.figure(2)
        plt.plot(window)
        plt.title("Hanning Window")
        plt.xlabel("Sample Number")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.savefig("../html/images/Window.jpg", dpi=150)
        plt.show()
        print("Window plot saved")

def GetSpeed(I,Q):
    # create time vector
    t = np.linspace(0,TS,settings.N_Samp)

    # Plot input signal
    if settings.DEBUG == True:
        plt.figure(3)
        plt.plot(t,I,t,Q)
        plt.grid()
        plt.title("Input Signal")
        plt.xlabel("Time in s")
        plt.ylabel("Voltage in V")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.savefig("../html/images/Input.jpg",dpi=100)
        print("Input plot saved")

    # calculate DC
    DC_I = 1/settings.N_Samp * np.sum(I)
    DC_Q = 1/settings.N_Samp * np.sum(Q)

    # remove DC
    I = I - DC_I
    Q = Q - DC_Q 

    # Plot DC-free signal
    if settings.DEBUG == True:
        plt.figure(4)
        plt.plot(t,I,t,Q)
        plt.grid()
        plt.title("Input Signal with removed DC")
        plt.xlabel("Time in s")
        plt.ylabel("Voltage in V")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.savefig("../html/images/DC_free_input.jpg",dpi=100)
        print("DC-free plot saved")

def demoSignal():
    # demo signal
    t = np.linspace(0,TS,settings.N_Samp) # time vector

    # main Signal
    f1 = 500                   # Frequency for the demo signal
    w1 = 2*np.pi*f1             # circular frequency
    A1 = 2.500                  # Amplitude
    DC = 2.5                    # DC value
    I1 = A1*np.cos(w1*t) + DC   # Build the signal

    Q1 = A1*-np.sin(w1*t) + DC

    # noise 1
    # 20kHz
    fn1 = 20000                 # Frequency of the noise
    wn1 = 2*np.pi*fn1           # circular frequency
    An1 = 0.100                 # Amplitude
    In1 = An1*np.cos(wn1*t)     # Build the signal

    # noise 2
    # 50Hz
    fn2 = 50
    wn2 = 2*np.pi*fn1
    An2 = 0.100
    In2 = An2*np.cos(wn2*t)

    # Signal
    I = I1 + In1 + In2 # Signal I
    Q = Q1 + In1 + In2 # Signal Q
    # y= I + Q1*1j

    if settings.DEBUG == True:
        # Plot of the Signal
        plt.plot(t,I,t,Q)
        plt.grid()
        plt.title("Input Signal")
        plt.xlabel("Time in s")
        plt.ylabel("Voltage in V")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.savefig("../html/images/Demosignal.jpg",dpi=100)
        plt.show()

    demoSig = np.zeros([settings.N_Samp,2])
    demoSig[:,0] = I
    demoSig[:,1] = Q

    return demoSig
    

# create an i2c instance when file is in script mode
if __name__ == "__main__":
    Init()
    sig = demoSignal()
    GetSpeed(sig[:,0],sig[:,1])
    print("Script finished")