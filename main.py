from sense_hat import SenseHat
from time import sleep
from datetime import datetime
from math import sqrt
from numpy import std
from scipy.signal import find_peaks

class SamplePoint:
    def __init__(self, x, y, z):
        self.x = x * 9.8
        self.y = y * 9.8
        self.z = z * 9.8
        self.mag = 0
        self.magNoG = 0
     
class WalkingSession:
    
    def __init__(self):
        self.samplepoints = [] # creates a new empty list
        self.mean = 0
        self.minPeakHeight = 0
        self.peaks = []    # creates a new empty list
        self.steps = 0
        self.type =  0
        self.starttime = 0
        self.stoptime = 0
        self.duration = 0
        self.calories = 0        

sense = SenseHat()

e = (0, 0, 0)
w = (255, 255, 255)

sense.clear()

sessions = []
NumSessions = 0

state = 0

while True:
    if(state == 1):
        # getting data from accelerometer
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']
        
        #appending a new SamplePoint to the WalkingSession
        sessions[NumSessions-1].samplepoints.append(SamplePoint(x, y, z))
  
    for event in sense.stick.get_events():
    # Check whether the joystick was pressed
        if event.action == "pressed":
        
            # Checking direction
            if event.direction == "up":
                sense.show_letter("U")      # Up arrow
            elif event.direction == "down":
                sense.show_letter("D")      # Down arrow
            elif event.direction == "left": 
                sense.show_letter("L")      # Left arrow
            elif event.direction == "right":
                sense.show_letter("R")      # Right arrow
            elif event.direction == "middle":
                sense.show_letter("M")      # Enter key
                if(state == 1):
                    state = 0
                    
                    for i in sessions[NumSessions-1].samplepoints:
                        i.mag = sqrt(i.x * i.x + i.y * i.y + i.z * i.z)
                    
                    summa = 0
                    num = 0
                    for i in sessions[NumSessions-1].samplepoints:
                        num = num + 1
                        summa = summa + i.mag
                    
                    sessions[NumSessions-1].mean = summa / num
                    
                    magNoGArray = []
                    for i in sessions[NumSessions-1].samplepoints:
                        i.magNoG = i.mag - sessions[NumSessions-1].mean
                        magNoGArray.append(i.magNoG)
                    
                    sessions[NumSessions-1].minPeakHeight = std(magNoGArray)
                    
                    sessions[NumSessions-1].peaks, _ = find_peaks(magNoGArray, height=sessions[NumSessions-1].minPeakHeight, distance=50)
                    
                    print(sessions[NumSessions-1].peaks)
                    sessions[NumSessions-1].steps = sessions[NumSessions-1].peaks.size
                    print(sessions[NumSessions-1].steps)
                    
                    sessions[NumSessions-1].stoptime = datetime.now()
                    sessions[NumSessions-1].duration = sessions[NumSessions-1].stoptime.timestamp() - sessions[NumSessions-1].starttime.timestamp()
                    print("duration =", sessions[NumSessions-1].duration)
                    
                else:
                    state = 1
                    
                    NumSessions += 1;
                    sessions.append(WalkingSession())
                    sessions[NumSessions-1].starttime = datetime.now()
        
        # Wait a while and then clear the screen
        sleep(0.5)
        sense.clear()
