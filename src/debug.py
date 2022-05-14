import matplotlib.pyplot as plt
import numpy as np
import settings
import calculations

def plot(sig1,sig2,sigName1: str,sigName2: str,xLabel: str,yLabel: str,title: str,x_vec=np.linspace(0,settings.N_Samp-1,settings.N_Samp)):
    directory = "./html/images/"
    imgType = '.jpg'

    plt.figure(title)
    plt.clf
    plt.plot(x_vec,sig1,x_vec,sig2)
    plt.legend([str(sigName1),str(sigName2)])
    plt.title(str(title))
    plt.xlabel(str(xLabel))
    plt.ylabel(str(yLabel))
    plt.savefig(directory + title + imgType,dpi=150)

    print(title + " plot saved")


if __name__ == '__main__':

    calculations.Init()
    sig1, sig2 = calculations.demoSignal()

    plot(sig1,sig2,"Signal 1", "Signal 2","Time in s","Amplitude in mV","Debug Test")