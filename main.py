from target import CornerReflector
from plotRTI import plotRTI
from backprojection import interp_approach
from drone import Drone
from simple_radar import RadarData
from plot_mission import plotMission
import numpy as np

waypoints = [[0,0,2],[5,0,2]]
speeds = [5]
numSteps = 100

drone = Drone(waypoints,speeds,numSteps)
dronePos = drone.interpolate()
radar = RadarData()

target = CornerReflector(.33,radar.radarWavelength,[2.5,3,0])
target2 = CornerReflector(.33,radar.radarWavelength,[2.5,5,0])
targets = [target,target2]

WrongRadarPosition = []
scans = []
for position in dronePos:
    WrongRadarPosition.append([position[1],position[2],position[0]])

    radar.radarPos = position
    scans.append(radar.get_scan(targets))
plotRTI(scans)

plotMission(dronePos,targets,scans,drone.totalTime)

radar_data = [np.array(scans),WrongRadarPosition,radar.rangebins]
interp_approach(radar_data,radar_data,[0,5],[0,6],.1)
