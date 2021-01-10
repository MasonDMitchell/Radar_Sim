import numpy as np
import matplotlib.pyplot as plt

def plotRTI(scan):
    plt.figure(0)
    plt.set_cmap('jet')
    plt.imshow(np.abs(scan))
    plt.title('Range-Time Intensity')
    plt.xlabel('Range Bins')
    plt.ylabel('Pulse Index')
    plt.axis('tight')
    ax = plt.gca()
    ax.invert_yaxis()
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('dB')
    plt.show()
