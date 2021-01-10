import numpy as np
from scipy import interpolate

class Drone:
    def __init__(self,waypointPositions,waypointSpeeds,numSteps):
        self.waypointPositions = waypointPositions #m
        self.waypointSpeeds = waypointSpeeds #m/s
        
        self.numSteps = numSteps #This is somewhat accurate. It's the resolution essentially

        #Calculating the time it should take to finish each segment of the set of waypoints
        self.waypointTimes = []
        for i in range(1,len(self.waypointPositions)):
            distance = np.linalg.norm(np.subtract(self.waypointPositions[i],self.waypointPositions[i-1]))
            waypointTime = distance / self.waypointSpeeds[i-1]
            self.waypointTimes.append(waypointTime)
       
        #Sum of all of the waypoint times is the total time of the mission
        self.totalTime = np.sum(self.waypointTimes)

    def interpolate(self):
        self.totalPos = []
        for i in range(1,len(self.waypointPositions)):
            
            #Determine how fast each XYZ component should go to follow m/s desired
            posDiff = np.subtract(self.waypointPositions[i],self.waypointPositions[i-1]) #Find difference of pos
            normPosDiff = np.linalg.norm(posDiff) #3D Length of pos diff
            speedMultVals = posDiff / normPosDiff #Pos diff in unit vector terms
            xyzSpeeds = self.waypointSpeeds[i-1] * speedMultVals #Speeds that each component needs to go

            X = [self.waypointPositions[i-1][0],self.waypointPositions[i][0]] #X values of waypoints
            Y = [self.waypointPositions[i-1][1],self.waypointPositions[i][1]] #Y values of waypoints
            Z = [self.waypointPositions[i-1][2],self.waypointPositions[i][2]] #Z values of waypoints
            
            #Scipy linear interpolation objects of X,Y & Z values
            fx = interpolate.interp1d([0,1],X)
            fy = interpolate.interp1d([0,1],Y)
            fz = interpolate.interp1d([0,1],Z)
    
            #Calculating number of steps based on total time and waypoint time
            numSteps = self.numSteps * (self.waypointTimes[i-1] / self.totalTime)

            #Linear interpolation
            newX = fx(np.linspace(0,1,num=int(numSteps)))
            newY = fy(np.linspace(0,1,num=int(numSteps)))
            newZ = fz(np.linspace(0,1,num=int(numSteps)))

            #Put in [X,Y,Z] format
            for ii in range(len(newX)):
                self.totalPos.append([newX[ii],newY[ii],newZ[ii]])
            print("Finished waypoint " + str(i-1) + "-" + str(i) + " at step number: " + str(len(self.totalPos)))
        #TODO Maybe add something if amount of scans needs to be exact
        return np.array(self.totalPos)

if __name__ == "__main__":
    waypoints = [[0,0,0],[0,0,5],[5,0,5],[0,0,5],[0,0,0]] #m
    speeds = [1,2,2,1] #m/s
    numSteps = 4200
    x = Drone(waypoints,speeds,numSteps)

    pos = x.interpolate()
