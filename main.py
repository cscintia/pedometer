import time
import threading
import mysql.connector
from sense_hat import SenseHat
from datetime import datetime
from math import sqrt
from numpy import std
from scipy.signal import find_peaks

OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  # 2
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  # 3
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  # 4
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  # 5
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  # 6
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  # 7
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  # 8
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1]  # 9

# Displays a single digit (0-9)
def show_digit(val, xd, yd, r, g, b):
  offset = val * 15
  for p in range(offset, offset + 15):
    xt = p % 3
    yt = (p-offset) // 3
    sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

# Displays a two-digits positive number (0-99)
def show_number(val, r, g, b):
  abs_val = abs(val)
  tens = abs_val // 10
  units = abs_val % 10
  if abs_val > 9: show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
  show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)
  
# Displays a point (non-blocker)
def show_point():
    while True:
        if MenuState == 2:
            sense.show_letter(".", [255, 0, 0])
            time.sleep(0.5) #Wait a while and then clear the screen
            sense.clear()
        time.sleep(0.5)

# Displays the actual type (non-blocker)
def show_type():
    while True:
        if MenuState == 1:
            sense.show_letter(SessionType, [255, 227, 2])
            time.sleep(0.5) #Wait a while and then clear the screen
            sense.clear()
        time.sleep(0.5)
        
# Displays the actual weight (non-blocker)
def show_weight():
    while True:
        if MenuState == 0:
            show_number(PersonWeight, 255, 227, 2)
            time.sleep(0.5) #Wait a while and then clear the screen
            sense.clear()
        time.sleep(0.5)

# Class for storing accelerometer data
class SamplePoint:
    def __init__(self, x, y, z):
        self.x = x * 9.8
        self.y = y * 9.8
        self.z = z * 9.8
        self.mag = 0
        self.magNoG = 0
     
# Class for storing session data     
class WalkingSession:
    def __init__(self):
        self.samplepoints = [] # creates a new empty list
        self.mean = 0
        self.minPeakHeight = 0
        self.peaks = []    # creates a new empty list
        self.steps = 0
        self.type =  "W"
        self.starttime = 0
        self.stoptime = 0
        self.duration = 0
        self.met = 0
        self.weight = 0
        self.calories = 0        

sense = SenseHat()

sense.clear()

sessions = []
NumSessions = 0
PersonWeight = 70
SessionType = "W"

MenuState = 0
SessionState = 0

t0 = threading.Thread(target=show_weight)
t1 = threading.Thread(target=show_type)
t2 = threading.Thread(target=show_point)
t0.start()
t1.start()
t2.start()

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="raspberry",
  database="pedometer"
)

while True:
    
    # User input about their weight
    if MenuState == 0 :
        for event in sense.stick.get_events():
            # Check whether the joystick was pressed
            if event.action == "pressed":
                # Checking direction
                if event.direction == "up":
                    if PersonWeight < 99:
                        PersonWeight = PersonWeight + 1 # Up arrow
                elif event.direction == "down":
                    if PersonWeight > 1:
                        PersonWeight = PersonWeight - 1 # Down arrow
                elif event.direction == "middle":
                    MenuState = 1
                  
                  
    # User input about the type of the next session (W=Walking, J=Jogging, R=Running)
    elif MenuState == 1 :
        for event in sense.stick.get_events():
            # Check whether the joystick was pressed
            if event.action == "pressed":
                # Checking direction
                if event.direction == "up":
                    if SessionType == "W":
                        SessionType = "J" # Up arrow
                    elif SessionType == "J" or SessionType == "R":
                        SessionType = "R" # Up arrow
                elif event.direction == "down":
                    if SessionType == "W" or SessionType == "J":
                        SessionType = "W" # Down arrow
                    elif SessionType == "R":
                        SessionType = "J" # Down arrow
                elif event.direction == "middle":
                    MenuState = 2
                    NumSessions += 1;
                    sessions.append(WalkingSession())
                    sessions[NumSessions-1].starttime = datetime.now()
                    sessions[NumSessions-1].type = SessionType
                    if SessionType == "W":
                        sessions[NumSessions-1].met = 3.0
                    elif SessionType == "J":
                        sessions[NumSessions-1].met = 8.8
                    elif SessionType == "R":
                        sessions[NumSessions-1].met = 11.2  
                    sessions[NumSessions-1].weight = PersonWeight
                    
    
    # Session is in progress
    elif MenuState == 2 :    
        for event in sense.stick.get_events():
            # Check whether the joystick was pressed
            if event.action == "pressed":
                # Checking direction
                if event.direction == "middle":
                    MenuState = 1

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
                    
                    sessions[NumSessions-1].peaks, _ = find_peaks(magNoGArray, height=sessions[NumSessions-1].minPeakHeight, distance=30)
                    
                    print(sessions[NumSessions-1].peaks)
                    sessions[NumSessions-1].steps = sessions[NumSessions-1].peaks.size
                    print(sessions[NumSessions-1].steps)
                    
                    sessions[NumSessions-1].stoptime = datetime.now()
                    sessions[NumSessions-1].duration = sessions[NumSessions-1].stoptime.timestamp() - sessions[NumSessions-1].starttime.timestamp()
                    print("duration =", sessions[NumSessions-1].duration)
                    
                    hour = sessions[NumSessions-1].duration / 3600
                    sessions[NumSessions-1].calories = sessions[NumSessions-1].met * sessions[NumSessions-1].weight * hour
                    
                    mycursor = mydb.cursor()

                    sql = "INSERT INTO WalkingSession (Type, Mean, StartTime, StopTime, Duration, CountofSteps, MET, Weight, Calories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (sessions[NumSessions-1].type, str(sessions[NumSessions-1].mean), str(sessions[NumSessions-1].starttime), str(sessions[NumSessions-1].stoptime), str(sessions[NumSessions-1].duration), str(sessions[NumSessions-1].steps), str(sessions[NumSessions-1].met), str(sessions[NumSessions-1].weight), str(sessions[NumSessions-1].calories))
                    mycursor.execute(sql, val)

                    mydb.commit()
                    
        
        # getting data from accelerometer
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']  
        z = acceleration['z']
        
        #appending a new SamplePoint to the WalkingSession
        sessions[NumSessions-1].samplepoints.append(SamplePoint(x, y, z))    