import matplotlib as mpl
import matplotlib.ticker as ticker
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


def plotMission(dronePos,targets,scans,time):
    
    #Get positions of targets
    targetsPos = []
    for target in targets:
        targetsPos.append(target.position)

    targetsX = []
    targetsY = []
    targetsZ = []
    for target in targetsPos:
        targetsX.append(target[0])
        targetsY.append(target[1])
        targetsZ.append(target[2])

    fig = plt.figure()
    ax = fig.add_subplot(1,2,1,projection='3d')
    ax2 = fig.add_subplot(1,2,2)

    dronePlot, = ax.plot([],[],[],'^',color='red',ms=6)
    targetPlot, = ax.plot([],[],[],'D',ms=6)
    scans = np.abs(scans)

    im = ax2.imshow(scans,cmap='jet')
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(len(dronePos)/10))
    ax2.axis('tight')
    def init():
        dronePlot.set_data([],[])
        dronePlot.set_3d_properties([])

        targetPlot.set_data([],[])
        targetPlot.set_3d_properties([])

        return dronePlot, targetPlot,im
    def animate(i):
        dronePlot.set_data(dronePos[i][0],dronePos[i][1])
        dronePlot.set_3d_properties(dronePos[i][2])
        targetPlot.set_data(targetsX,targetsY)
        targetPlot.set_3d_properties(targetsZ)
        im.set_array(scans[0:i+1])
        ax2.set_ylim(0,i+1)

        return dronePlot, targetPlot, im,

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    
    ax.set_xlim3d([min([min(dronePos[:,0]),min(targetsX)])-1,max([max(dronePos[:,0]),max(targetsX)])+1])
    ax.set_ylim3d([min([min(dronePos[:,1]),min(targetsY)])-1,max([max(dronePos[:,1]),max(targetsY)])+1])
    ax.set_zlim3d([min([min(dronePos[:,2]),min(targetsZ)])-1,max([max(dronePos[:,2]),max(targetsZ)])+1])

    ax.set_title("Drone Mission")

    ax2.set_title("Range-Time Intensity")
    ax2.set_xlabel("Range Bins")
    ax2.set_ylabel("Pulse Index")

    ax2.invert_yaxis()

    anim = animation.FuncAnimation(fig,animate,blit=False,init_func=init,frames=len(dronePos),interval=(time/len(dronePos)*1000))

    plt.show()
