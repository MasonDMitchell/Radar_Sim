import numpy as np
import math
from target import CornerReflector

#Purpose is to have a customizable RADAR that gets readings from targets in an idealistic scenario
class RadarData:
    def __init__(self):

        #TODO Might want to add these values to init...
        self.numRangebins = 1000
        self.rangebinSize = .01 #(m)
        self.rangebinStart = 2 #Distance at which rangebins begin
        
        #All difference distance values of rangebins
        self.rangebins = np.arange(2,2 + (self.numRangebins*self.rangebinSize),self.rangebinSize)
        self.scanData = np.zeros(self.numRangebins)

        #PulsOn 450 microwatts
        self.powerTransmitted = .00045 #Power of pulse transmitted (watt)

        #Zero gain is lossless antenna
        #Should technically be lossless but 0 makes function = 0
        self.gain = .1 #Antenna gain

        #1.7GHz
        self.radarWavelength = 1700000000 #Radar operating wavelength (lamda) 
        
        #Should technically be lossless but 0 makes function = undefined
        self.losses = 1 #Other losses

        #Radar position [x,y,z] (m)
        self.radarPos = [0,0,0]

    #targets: list of CornerReflector class objects
    #
    #return: list of readings for each rangebin with target returns added
    def get_scan(self,targets):
        self.scanData = np.zeros(self.numRangebins)

        for target in targets:
            powerRecieved, targetDistance = self.scan_target(target)
            index = self.find_nearest(self.rangebins,targetDistance)
            self.scanData[index] = self.scanData[index] + powerRecieved

        return self.scanData


    #Calculated powerRecieved and distance from reflector
    #target: CornerReflector class object
    #
    #return: powerRecieved & targetDistance
    def scan_target(self,target):

        rcs = target.rcs

        #Get the 3D difference between the radar position and target position
        targetDistance = np.subtract(self.radarPos,target.position)
        #Find length of 3D difference (distance from radar to target)
        targetDistance = np.linalg.norm(targetDistance)

        #Calculate power recieved from target based on all factors (watt)
        powerRecieved = (self.powerTransmitted*(self.gain**2)*(self.radarWavelength**2)*rcs)/(((4*np.pi)**3)*(targetDistance**4)*self.losses) #Power of pulse recieved from radar

        return powerRecieved,targetDistance


    #Helper function to find closest rangebin to place readings in
    #array: sorted list of values
    #value: the value you are trying to find the nearest index to
    #
    #return: index of closest value in array to value 
    def find_nearest(self,array,value):
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
            return idx-1
        else:
            return idx

if __name__ == "__main__":

    from plotRTI import plotRTI
    from backprojection import interp_approach
    radar = RadarData()

    target = CornerReflector(.33,radar.radarWavelength,[0,5,0])
    targets = [target]
    
    scans = []
    totalRadarPos = []
    for i in np.arange(0,2,.001):
        totalRadarPos.append([0,0,i])
        radar.radarPos = [i,0,0]
        scans.append(radar.get_scan(targets))

    plotRTI(scans)

    radar_data = [np.array(scans),totalRadarPos,radar.rangebins]
    interp_approach(radar_data,radar_data,[-3,3],[0,6],.2)
