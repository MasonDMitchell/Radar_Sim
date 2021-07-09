import matplotlib as mpl
import matplotlib.ticker as ticker
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

#dronePos: all of the drone positions in [[x,y,z],[x2,y2,z2], ...] formatting
#targets: all target pos in [[targetx1,targety1,targetz1],[targetx2,targety2,targetz2],...] formatting
#scans: all scans in [scan1,scan2,scan3,...] formatting
#time: float usually passed from drone object, essentially dictating how long the plotting should take
#
#returns: nothing, but plots a continouous loop until window is closed
def plotMission(dronePos,targets,scans,time):
    
    #Get positions of targets
    targetsPos = []
    for target in targets:
        targetsPos.append(target.position)
    
    #Place positions of targets in individual x,y,z lists for easy plotting
    targetsX = []
    targetsY = []
    targetsZ = []
    for target in targetsPos:
        targetsX.append(target[0])
        targetsY.append(target[1])
        targetsZ.append(target[2])

    #Generate figure, and the two subplots with the correct parameters
    fig = plt.figure()
    ax = fig.add_subplot(1,2,1,projection='3d')
    ax2 = fig.add_subplot(1,2,2)

    #Initialize plots for both subplots
    dronePlot, = ax.plot([],[],[],'^',color='red',ms=6)
    targetPlot, = ax.plot([],[],[],'D',ms=6)
    #Initializing includes getting the absolute val of scans because of performance issues
    scans = np.abs(scans)
    im = ax2.imshow(scans,cmap='jet')

    #Set parameters for a good-looking RTI plot
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(len(dronePos)/10))
    ax2.axis('tight')

    #Init function, basically just zero parameters are set.
    def init():
        dronePlot.set_data(np.array([]),np.array([]))
        dronePlot.set_3d_properties(np.array([]))

        targetPlot.set_data(np.array([]),np.array([]))
        targetPlot.set_3d_properties(np.array([]))

        return dronePlot, targetPlot,im
    #Animation function steps through each value of drone pos and plots new pos, targets, and RTI
    def animate(i):
        dronePlot.set_data(dronePos[i][0],dronePos[i][1])
        dronePlot.set_3d_properties(dronePos[i][2])
        targetPlot.set_data(np.array(targetsX),np.array(targetsY))
        targetPlot.set_3d_properties(np.array(targetsZ))
        im.set_array(scans[0:i+1])
        ax2.set_ylim(0,i+1)

        return dronePlot, targetPlot, im,

    #Setting labels and limits for 3D plot
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    
    ax.set_xlim3d([min([min(dronePos[:,0]),min(targetsX)])-1,max([max(dronePos[:,0]),max(targetsX)])+1])
    ax.set_ylim3d([min([min(dronePos[:,1]),min(targetsY)])-1,max([max(dronePos[:,1]),max(targetsY)])+1])
    ax.set_zlim3d([min([min(dronePos[:,2]),min(targetsZ)])-1,max([max(dronePos[:,2]),max(targetsZ)])+1])

    ax.set_title("Drone Mission")

    #Setting labels and inverting axis for RTI plot
    ax2.set_title("Range-Time Intensity")
    ax2.set_xlabel("Range Bins")
    ax2.set_ylabel("Pulse Index")

    ax2.invert_yaxis()

    #Actual animation function, can also be saved to a .gif or .mp4 if desired. Look at matplotlib documentation
    anim = animation.FuncAnimation(fig,animate,blit=False,init_func=init,frames=len(dronePos),interval=(time/len(dronePos)*1000))
    
    #Show image
    plt.show()
