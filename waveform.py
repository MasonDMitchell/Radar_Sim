#Constants
SPEED_OF_LIGHT = 299792458 #Speed of light (m/s)

class rectangularWave:
    def __init__(RANGE_RES,MAX_RANGE):

        #?? AMPLITUDE

        PROP_SPEED = SPEED_OF_LIGHT #Propogation Speed

        PULSE_BW = PROP_SPEED / (2*RANGE_RES) #Pulse Bandwidth

        PULSE_WIDTH = 1 / PULSE_BW #Pulse Width

        PRF = PROP_SPEED / (2*MAX_RANGE) #Pulse Repetition Frequency

        FS = 2*PULSE_BW #Sampling Rate

    def plot():
        amp = 1

        

        return 

if __name__ == "__main__":

    #Params
    RANGE_RES = .1 #Range resolution (m)
    MAX_RANGE = 20 #Largest seeing distance (m)
