import numpy as np
#Trihedral corner reflector
class CornerReflector:
    #sideLengths: Size of edges of corner reflector (m)
    #radarWavelength: Pulse wavelength of radar (Hz)
    #Position: [X,Y,Z] data of reflector (m)
    def __init__(self,sideLengths,radarWavelength,position):
       self.rcs = (12*np.pi*(sideLengths**4))/(radarWavelength**2) #Target radar cross section (sigma)
       self.position = position
       return
