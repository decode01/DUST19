import numpy as np
import random
import time
import sys
import threading
import argparse
from pydub import AudioSegment
from pydub.playback import play
from math import sin, cos, sqrt, atan2, radians




parser = argparse.ArgumentParser()
parser.add_argument('--deviceID')
#parser.add_argument('--mode') "mode not required
args = parser.parse_args()


output = {}
patient_allocated = False # change this to true for the GPS logic to start working
patient_gps = {}


if args.deviceID is None:
    print("Please enter device ID")
    exit(1)
    
class Dummy:
    def __init__(self,id,patient_allocated):
        self.id = id
        self.patient_allocated = patient_allocated
        self.dummy_s1 = {"lat": round((53.1912 + random.randint(1,4)*0.7),4), "lon": round(-6.1406 - random.randint(1,4)*0.7,4)}
        self.dummy_s2 = random.randint(60,90) #random value between 60 percent and 90 percent
        self.dummy_s3 = 25 # considering an optimal temperature for the AC
        self.dummy_s4 = { "o2" : True , "bp" : True}
        self.dummy_s5 = { "ecg" : True , "defib" : True}
        self.dummy_s6 = "yes"
        self.dummy_s7 = False
        self.dummy_s8 = None
        self.list = [ "low " , "med ", "high"]
        #self.output = {}
        
        #self.fuel_start = fuel_start
    def playsound(self):
        sound = AudioSegment.from_wav('ami_copsirene.wav')
    
        play(sound)
        time.sleep(5)
    def gps(self,patient_allocated,patient_gps):

        if patient_allocated is True and bool(patient_gps):
            if (patient_gps["lat"] == self.dummy_s1["lat"]) or (abs( patient_gps["lat"] - self.dummy_s1["lat"]) < 0.005 ):
                pass
            elif patient_gps["lat"] > self.dummy_s1["lat"]:
                self.dummy_s1["lat"] += 0.005
            else:
                self.dummy_s1["lat"] -= 0.005
                
            if (patient_gps["lon"] == self.dummy_s1["lon"] ) or abs( patient_gps["lon"] - self.dummy_s1["lon"]) < 0.005:
                pass
            elif patient_gps["lon"] > self.dummy_s1["lon"]:
                self.dummy_s1["lon"] += 0.005
            else:
                self.dummy_s1["lon"] -= 0.005
        
        else:
            self.dummy_s1["lat"] += 0.0001
            self.dummy_s1["lon"] -= 0.0001
        self.dummy_s1["lat"] = round(self.dummy_s1["lat"],4)
        self.dummy_s1["lon"] = round(self.dummy_s1["lon"],4)
        #self.ful_start -= 0.01
        return self.dummy_s1
  
    def fuel(self,patient_allocated):
        self.dummy_s2 -= 0.25
        return round(self.dummy_s2,2)
    
    def ac(self,patient_allocated):
        return round(self.dummy_s3 + random.randint(-2,2),2)
   
    def vital(self,patient_allocated):
        num = int(self.id)
        if num % 2 == 0:
            self.dummy_s4["bp"] = False
        return self.dummy_s4
   
    def ecg(self,patient_allocated):
        num = int(self.id)
        if num % 2 == 0:
            self.dummy_s5["ecg"] = False
        return self.dummy_s5
   
    def microphone(self,patient_allocated):
        #keeping it yes for the moment
        return self.dummy_s6

    def siren(self,patient_allocated):
        if patient_allocated is True and bool(patient_gps):
            self.dummy_s7 = True
            sound = threading.Thread(target = self.playsound,daemon=True)
            sound.start()
        return self.dummy_s7
  
    def radar(self,patient_allocated): #considering it to be a proximity sensor
        if patient_allocated is False:
            # fewer traffic
            self.dummy_s8 = random.randint(7,10)
        else:
            self.dummy_s8 = random.randint(2,6)
       
        return self.dummy_s8
  

    def start(self):
        #output = {}
        global patient_allocated
        global patient_gps
        output["ID"] = self.id
        output["D1"] = self.gps(patient_allocated, patient_gps)
        output["D2"] = self.fuel(patient_allocated)
        output["D3"] = self.ac(patient_allocated)
        output["D4"] = self.vital(patient_allocated)
        output["D5"] = self.ecg(patient_allocated)
        output["D6"] = self.microphone(patient_allocated)
        output["D7"] = self.siren(patient_allocated)
        output["D8"] = self.radar(patient_allocated)
        
        return output

def instantiate(id,patient_allocated):
    dummy = Dummy(id,patient_allocated)
    return dummy
def init_and_start(dummy):
    #dummy = Dummy(id)
    global output
    while True:
        #time.sleep(1)
        output = dummy.start()
        time.sleep(1)
        print(output, end= "   \r")
    #sys.stdout.flush()
    

    
dummy = instantiate(args.deviceID,patient_allocated)
listener = threading.Thread(target=init_and_start,kwargs={'dummy':dummy},daemon=True)
#init_and_start(args.deviceID) #"Pass this to thread and this will output steady steam of values"
listener.start()


#CONTROL LOGIC STARTS from here
def peek(output): #gets instance of output
    return(output)
#lets test
time.sleep(20) 
#siren will start after 20 seconds, ( for test purposes)
#daemon <true/false>?
patient_allocated = True
patient_gps = { "lat":53 , "lon" : -6}
#Now ambulance will start moving towards the target
time.sleep(50)

def check_feasibility(ambulance_lat, ambulance_long):
    dict = peek()
    eta = calculate_distance(ambulance_lat, ambulance_long, dict["D1"]["patient_gps"]["lat"], dict["D1"]["patient_gps"]["long"])
    if dict["D2"] > 50 and dict["D4"]["o2"] and dict["D4"]["bp"] and dict["D5"]["ecg"] and dict["D5"]["defib"]:
        print(eta)
        #connection true
    else :
        pass
        #No connection return false


def calculate_distance(ambulance_lat, ambulance_long, human_lat, human_long) :
    dlon = ambulance_long - human_long
    dlat = ambulance_lat - human_lat
    distance = sqrt(dlon**2 + dlat**2)
    #Assuming average speed of 60 km/hr
    time = distance/60
    print("ETA:", time)
    return time

while True:
    time.sleep(10)
    check_feasibility()

#CURRENT THREAD..call peek withing a loop to periodically check
#should be called in a while loop
#print("\n Parent thread looking at the output after 20 seconds ",peek(output))
#time.sleep(3)
