from target import CornerReflector
from plotRTI import plotRTI
from backprojection import interp_approach
from drone import Drone
from simple_radar import RadarData
from plot_mission import plotMission
import numpy as np

#Create waypoints [x,y,z] (m) for drone to initially start, and then move to
waypoints = [[0,0,2],[5,0,2]]

#Set speeds for drone to go between waypoints. Length should be 1 less than # of waypoints 
speeds = [2]

#Size of list of drone positions given back, essentially the resolution of the whole program
#NOTE Is not always accurate, due to some rounding this number may be off by a few 
numSteps = 100

#Create the drone object
drone = Drone(waypoints,speeds,numSteps)
#Get the list of drone positions
dronePos = drone.interpolate()
#Create radar object
radar = RadarData()

#Generate the targets for the scene
target = CornerReflector(sideLengths=.33,
                         radarWavelength = radar.radarWavelength,
                         position = [2.5,3,0])
target2 = CornerReflector(sideLengths=.33,
                          radarWavelength = radar.radarWavelength,
                          position = [2.5,5,0])

#Create list of targets, this is what gets passed into the radar object
targets = [target,target2]

#WrongRadarPosition is created due to the backprojection code assuming the position data is formatted differently than it is in this simulation
WrongRadarPosition = [] #List of drone positions [y,z,x]

#All of the rangebins in a time-dependent list [scan1,scan2,scan3,scan4,....]
scans = []

#Run for each 'step' or number of drone positions
for position in dronePos:
    #Get the wrong position
    WrongRadarPosition.append([position[1],position[2],position[0]])

    #Set the radar pos to what the drone has moved to
    radar.radarPos = position
    #Get the scan from that position based on all of the targets
    scans.append(radar.get_scan(targets))

#Plot a standalone RTI graph using the plotRTI file
plotRTI(scans)

#Plot 3D simulation of drone & targets, as well as a 'live' RTI plot
plotMission(dronePos,targets,scans,drone.totalTime)

#Put all data in a format that is readable by the standardized backprojection code
radar_data = [np.array(scans),WrongRadarPosition,radar.rangebins]

#Perform backprojection using interpolated shifts, and show resulting plot
interp_approach(radar_data,radar_data,[0,5],[0,6],.1)
