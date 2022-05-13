import matplotlib.pyplot as plt
import numpy as np
import settings

def plot(sig1,sig2,sigName,xLabel,yLabel,title,x_vec=np.linspace(0,settings.N_Samp-1,1)):
    plt.figure(title)
    plt.clf
    plt.plot()