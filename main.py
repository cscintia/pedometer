class WalkingSession:
    
    def __init__(self):
        self.x = []    # creates a new empty list
        self.y = []    # creates a new empty list
        self.z = []    # creates a new empty list
        self.mag = []    # creates a new empty list
        self.mean = 0
        self.minPeakHeight = 0
        self.magNoG = []    # creates a new empty list
        self.peaks = []    # creates a new empty list
        self.steps = 0

    def add_x(self, x):
        self.x.append(x)
        
    def add_y(self, y):
        self.y.append(y)
        
    def add_z(self, z):
        self.z.append(z)
    
    def myfunc(void):
        print("Hello")
        
from sense_hat import SenseHat
from time import sleep
from math import sqrt
from numpy import std
from scipy.signal import find_peaks
sense = SenseHat()

e = (0, 0, 0)
w = (255, 255, 255)

sense.clear()

sessions = []
NumSessions = 0


state = 0

while True:
    if(state == 1):
  
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']
        sessions[NumSessions-1].add_x(x*9.8)
        sessions[NumSessions-1].add_y(y*9.8)
        sessions[NumSessions-1].add_z(z*9.8)
  
    for event in sense.stick.get_events():
    # Check if the joystick was pressed
        if event.action == "pressed":
        
            # Check which direction
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
                    #print(sessions[NumSessions-1].x)
                    #print(sessions[NumSessions-1].y)
                    #print(sessions[NumSessions-1].z)
                    
                    for (i,j,k) in zip(sessions[NumSessions-1].x, sessions[NumSessions-1].y, sessions[NumSessions-1].z):
                        sessions[NumSessions-1].mag.append(sqrt(i * i + j * j + k * k))
                    
                    #print(sessions[NumSessions-1].mag)
                    
                    summ = 0
                    numb = 0
                    for i in sessions[NumSessions-1].mag:
                        numb = numb + 1
                        summ = summ + i
                    
                    sessions[NumSessions-1].mean = summ / numb
                    print(sessions[NumSessions-1].mean)
                    
                    for i in sessions[NumSessions-1].mag:
                        sessions[NumSessions-1].magNoG.append(i - sessions[NumSessions-1].mean)
                    #print(sessions[NumSessions-1].magNoG)
                    
                    sessions[NumSessions-1].minPeakHeight = std(sessions[NumSessions-1].magNoG)
                    print(sessions[NumSessions-1].minPeakHeight)
                    
                    #for i in sessions[NumSessions-1].magNoG:
                    #    if i >= sessions[NumSessions-1].minPeakHeight:
                    #        sessions[NumSessions-1].peaks.append(sessions[NumSessions-1].magNoG)
                    #        sessions[NumSessions-1].steps = sessions[NumSessions-1].steps + 1
                    
                    sessions[NumSessions-1].peaks, _ = find_peaks(sessions[NumSessions-1].magNoG, height=sessions[NumSessions-1].minPeakHeight, distance=50)
                    
                    print(sessions[NumSessions-1].peaks)
                    sessions[NumSessions-1].steps = sessions[NumSessions-1].peaks.size
                    print(sessions[NumSessions-1].steps)
                    
                else:
                    state = 1
                    
                    NumSessions += 1;
                    sessions.append(WalkingSession())
                    
                    
                    
                    sessions[NumSessions-1].myfunc()

                    #print(NumSessions)
        
        # Wait a while and then clear the screen
        sleep(0.5)
        sense.clear()
