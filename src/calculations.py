# File for the processing of the measured Data

# Imports
import ctypes
import time as time
import numpy as np
from numpy.ctypeslib import ndpointer
from scipy.fft import fft, fftshift, fftfreq
from scipy.signal import hann, butter, filtfilt
from scipy import signal
import matplotlib.pyplot as plt
import settings
import pga
import debug
from ctypes import *
import gc
import platform


# Constants
fc = 24e9
c = 3e8
ld = c/fc

# global variables
global globalstartTime
global localStartTime
global TS
global speed_array
speed_array = [0]

# C Functions
if(platform.machine() == 'armv6l'):
    so_file = "./test/adc2_zero1.so" # set the lib
else:
    so_file = "./test/adc2.so" # set the lib
ADC = CDLL(so_file) # open lib
meas = ADC.adc_meas
meas.restype = ctypes.c_uint32 # set output type
meas.argtypes =  [ctypes.c_uint8,
                ctypes.c_uint16,
                ndpointer(ctypes.c_uint16, flags="C_CONTIGUOUS"),
                ndpointer(ctypes.c_uint16, flags="C_CONTIGUOUS")] # set input types

# Initialisation for the calculations
def Init():
    # start timer
    global localStartTime
    localStartTime = time.time()

    # Calculating measuring Parameters
    globalStartTime = time.time()
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
    b,a = butter(10, np.multiply([400, ((settings.Fs/2)-50)], 2*np.pi), btype="band", fs=(settings.Fs*2*np.pi), output='ba', analog=False)
    
    # Plot filter
    if settings.DEBUG == True:
        w,h = signal.freqz(b,a, worN=settings.N_Samp,fs=wFs)
        plt.figure(1)
        plt.clf()
        plt.semilogx(w/(2*np.pi),20*np.log10(abs(h)))
        plt.title('Butterworth filter frequency response')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude [dB]')
        plt.grid(which='both', axis='both')
        plt.margins(0.1)
        plt.axvline(400, color='green') # highpass frequency
        plt.axvline(((settings.Fs/2)-50), color='green') # lowpass frequency
        plt.legend(["Frequency response","Pass Band"])
        plt.savefig("./html/images/Filter.jpg", dpi=150)
        print("Filter plot saved")
    
    # create the window
    global window, window_norm
    window = hann(settings.N_Samp, sym=True)
    window_av = np.average(window)
    window_norm = window/window_av

    # Plot window
    if settings.DEBUG == True:
        plt.figure(2)
        plt.clf()
        plt.plot(window)
        plt.plot(window_norm)
        plt.title("Hanning Window")
        plt.xlabel("Sample Number")
        plt.ylabel("Amplitude")
        plt.legend(["Hanning Window","Normalized Hanning Window"])
        plt.grid()
        plt.savefig("./html/images/Window.jpg", dpi=150)
        print("Window plot saved")
    
        stopTime = time.time()
        print("Init Time:" + str(stopTime-globalStartTime))


def GetSpeed():
    # start time measurement
    global localStartTime
    localStartTime = time.time()

    # global I_sig, Q_sig
    global I_sig, Q_sig
    I_sig = np.ascontiguousarray(np.empty(settings.N_Samp, dtype=ctypes.c_uint16))
    Q_sig = np.ascontiguousarray(np.empty(settings.N_Samp, dtype=ctypes.c_uint16))

    # start measurement
    t_samp = meas(ctypes.c_uint8(0),ctypes.c_uint16(settings.N_Samp),I_sig,Q_sig)

    # check for clipping
    if(((np.amax(I_sig) == 4095) or (np.amax(Q_sig) == 4095)) and (pga.pga_amp > 1)):
        if(settings.DEBUG == True):
            print("Clipping detected")
        return 999

    # check if the signal is to low
    if((np.ptp(I_sig) < settings.min_sig_pga) and (np.ptp(Q_sig) < settings.min_sig_pga) and (pga.pga_amp < 7)):
        if(settings.DEBUG == True):
            print("Low signal detected")
        return -999

    # create time vector
    t = np.linspace(0,(t_samp/1e6), settings.N_Samp)

    # Demo Signal
    if settings.DEMO == True:
        I_sig, Q_sig = demoSignal()
        t = np.linspace(0,TS,settings.N_Samp)
    # Plot input signal
    if settings.DEBUG == True:
        plt.figure(3)
        plt.clf()
        plt.plot(t,I_sig,t,Q_sig)
        plt.grid()
        plt.title("Input Signal")
        plt.xlabel("Time in s")
        plt.ylabel("Voltage in mV")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.savefig("./html/images/Input.jpg",dpi=150)
        print("Input plot saved")

    # calculate DC
    DC_I = 1/settings.N_Samp * np.sum(I_sig)
    DC_Q = 1/settings.N_Samp * np.sum(Q_sig)

    # remove DC
    I_sig = I_sig - DC_I
    Q_sig = Q_sig - DC_Q 

    # Plot DC-free signal
    if settings.DEBUG == True:
        plt.figure(4)
        plt.clf()
        plt.plot(t,I_sig,t,Q_sig)
        plt.grid()
        plt.title("Input Signal with removed DC")
        plt.xlabel("Time in s")
        plt.ylabel("Voltage in V")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.savefig("./html/images/DC_free_input.jpg",dpi=150)
        print("DC-free plot saved")

    # convert from mV to V
    I_sig = I_sig/1000
    Q_sig = Q_sig/1000

    # Filter the signal
    I_filt = filtfilt(b,a,I_sig)
    Q_filt = filtfilt(b,a,Q_sig)

    if settings.DEBUG == True:
        plt.figure(5)
        plt.clf()
        plt.plot(t,I_filt,t,Q_filt)
        plt.grid()
        plt.title("Filtered Signals")
        plt.xlabel("Time in s")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.savefig("./html/images/Filtered_Signals.jpg", dpi=150)
        print("Filtered plot saved")

    # Apply the Window
    I_filt = I_filt*window_norm
    Q_filt = Q_filt*window_norm

    if settings.DEBUG == True:
        # apply the Window
        plt.figure(6)
        plt.clf()
        I_filt = np.multiply(window,I_filt)
        Q_filt = np.multiply(window,Q_filt) 
        plt.plot(t,I_filt,t,Q_filt)
        plt.title("Filtered and windowed Signal")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.grid()
        plt.savefig("./html/images/filtered_windowed.jpg", dpi=150)
        print("Windowed Signal saved")

    # Combining I and Q signal
    z_t = I_filt + Q_filt * 1j

    # Perform the FFT
    z_f = fftshift(fft(z_t,norm='forward'))

    # Perform the FFT-shift
    if settings.DEMO == False:
        x_f = fftshift(fftfreq(settings.N_Samp,((t_samp/1e6)/settings.N_Samp)))
    if settings.DEMO == True:
        x_f = fftshift(fftfreq(settings.N_Samp,DT))

    # Calculate absolute valus
    z_f_abs = np.abs(z_f)

    # round noise
    z_f_abs[z_f_abs < settings.fft_thershold] = 0

    if settings.DEBUG == True:
        # Plot the FFT
        plt.figure(7)
        plt.clf()
        plt.plot(x_f,z_f_abs,'*')
        plt.grid()
        plt.title("FFT")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("|Signal|")
        plt.savefig("./html/images/FFT.jpg",dpi=150)
        print("FFT plot saved")

    # calculate speed
    n_max = np.argmax(z_f_abs[0:int((settings.N_Samp/2)-1)])
    max_f = x_f[n_max-1]
    if(settings.DEBUG == True): 
        print("n Max: " + str(n_max) + "; max f:" + str(max_f))
        
    if(n_max == 0):
        v = 0
    else:
        v = -3.6*max_f/2*ld

    print("Measured Speed: "+ str(v))

    # speed array
    global speed_array
    speed_array.append(v)
    if settings.SPEED_GRAPH == True:
        plt.figure(8)
        plt.clf()
        plt.plot(speed_array,'*')
        plt.grid()
        plt.title("Measured Speeds")
        plt.savefig("./html/images/Speed_graph.jpg",dpi=150)

    # stop time measurement and print
    stopTime = time.time()
    print("Measurement and Calculation Time:" + str(stopTime-localStartTime))

    # Garbage collector
    gc.collect()

    return v
    

def demoSignal():
    global TS
    # demo signal
    t = np.linspace(0,TS,settings.N_Samp) # time vector

    # main Signal
    f1 = 1000                   # Frequency for the demo signal
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
    wn2 = 2*np.pi*fn2
    An2 = 0.100
    In2 = An2*np.cos(wn2*t)

    # Signal
    I = 1000*(I1 + In1 + In2) # Signal I
    Q = 1000*(Q1 + In1 + In2) # Signal Q
    # y= I + Q1*1j

    if settings.DEBUG == True:
        # Plot of the Signal
        plt.figure(200)
        plt.clf()
        plt.plot(t,I,t,Q)
        plt.grid()
        plt.title("Input Signal")
        plt.xlabel("Time in s")
        plt.ylabel("Voltage in V")
        plt.legend(["I-Signal", "Q-Singal"])
        plt.savefig("./html/images/Demosignal.jpg",dpi=100)

    demoSig = np.zeros([settings.N_Samp,2])
    demoSig[:,0] = I
    demoSig[:,1] = Q

    return I,Q

def get_I_B(Samp):
    brightness = np.ascontiguousarray(np.empty(settings.N_Samp, dtype=ctypes.c_uint16))
    current = np.ascontiguousarray(np.empty(settings.N_Samp, dtype=ctypes.c_uint16))

    time = meas(ctypes.c_uint8(1),ctypes.c_uint16(settings.N_Samp_I_B,brightness,current))

    t = np.linspace(0,time,time/settings.N_Samp_I_B)

    if(settings.DEBUG == True):
        plt.figure(300)
        plt.clf()
        plt.plot(t,brightness,t,current)
        plt.grid()
        plt.title("Brightness and Current measurement data")
        plt.legend(["Brightness","Current"])
        plt.savefig("./html/images/B_C_data.jpg",dpi=150)
    
    return np.average(brightness),np.average(current)

    

if __name__ == "__main__":
    Init()
    while(1):
        GetSpeed()
    
