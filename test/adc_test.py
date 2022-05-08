import ctypes
from ctypes import *
import numpy as np
from numpy.ctypeslib import ndpointer
import time

# C Functions
so_file = "./test/adc2.so" # set the lib
ADC = CDLL(so_file) # open lib
meas = ADC.adc_meas
meas.restype = ctypes.c_uint32 # set output type
meas.argtypes =  [ctypes.c_uint8,
                ctypes.c_uint16,
                ndpointer(ctypes.c_uint16, flags="C_CONTIGUOUS"),
                ndpointer(ctypes.c_uint16, flags="C_CONTIGUOUS")] # set input types

I_sig = np.ascontiguousarray(np.empty(1024, dtype=ctypes.c_uint16))
Q_sig = np.ascontiguousarray(np.empty(1024, dtype=ctypes.c_uint16))

while True:
    t_samp = meas(ctypes.c_uint8(0),ctypes.c_uint16(1024),I_sig,Q_sig)
    print(t_samp)
    time.sleep(0.1)