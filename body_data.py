import numpy as np
import random
import time
import sys
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--deviceID')
parser.add_argument('--mode')
args = parser.parse_args()


output = {}
emergency = True

if args.deviceID is None:
    print("Please enter device ID")
    exit(1)
if args.mode is None:
    emergency = False
    
class Dummy:
    def __init__(self,id,emergency):
        self.id = id
        self.emergency = emergency
        self.dummy_s1 = 70
        self.dummy_s2 = 35.9
        self.dummy_s3 = {"lat": 53.1912, "lon":-6.1406}
        self.dummy_s4 = 95
        self.dummy_s5 = None
        self.dummy_s6 = "yes"
        self.dummy_s7 = 15
        self.dummy_s8 = {"sys": 110, "dia": 68}
        self.list = [ "low " , "med ", "high"]
        #self.output = {}
        
        #self.fuel_start = fuel_start
    def heart(self,emergency):
        #can be fuel/heartbeat
        if emergency is True:
            if self.dummy_s1 < 90:
                self.dummy_s1 += 2
            elif self.dummy_s1 < 120:
                self.dummy_s1 += 3
            elif self.dummy_s1 < 150:
                self.dummy_s1 +=2
            else:
                self.dummy_s1 += random.randint(-8,8)*0.005
        else:
            self.dummy_s1 = random.randint(-3,10)
        #self.ful_start -= 0.01
        return int(self.dummy_s1)
    #Temperature increases after Heart rate crosses 100
    def temperature(self,emergency):
        if emergency is False:
            self.dummy_s2 = round(random.randint(37,38)*1.01,2)#*1.1
        else:
            if (( 38 - self.dummy_s2 ) > 0.1) and self.dummy_s1>100:
                self.dummy_s2 += 0.1
        return round(self.dummy_s2,2)
    
    #Patient stops moving and shows fixed GPS after temperature crosses 37 degree C
    def gps(self,emergency):
        if emergency is False:
            lan = random.randint(-3,0) * 0.001
            lon = random.randint(-3,0) * 0.001
        else:
            lan = random.randint(0,3) * 0.001
            lon = random.randint(0,3) * 0.001
        if self.dummy_s2 < 37:
            self.dummy_s3["lat"] += lan
            self.dummy_s3["lon"] += lon
            
        self.dummy_s3["lat"] = round(self.dummy_s3["lat"],4)
        self.dummy_s3["lon"] = round(self.dummy_s3["lon"],4)
        return self.dummy_s3
    #SPO2 is changed randomly
    def spo2(self,emergency):
        self.dummy_s4 += random.randint(-8,8)*0.005
        self.dummy_s4 = round(self.dummy_s4,3)
        return self.dummy_s4
    #Stress generally fixed at medium..changes to high after temperature crosses 37
    def stress(self,emergency):
        #self.dummy_s5 = random.randint(12,16)
        self.dummy_s5 = self.list[1]
        if emergency is True:
            if self.dummy_s2 > 37:
                self.dummy_s5 = self.list[2]
        return self.dummy_s5
    #Motion will turn to no when temperature crosses 37 and heartbeat crosses 140
    def motion(self,emergency):
        if emergency is True and self.dummy_s2 > 37 and self.dummy_s1 > 140:
            self.dummy_s6 = "no"#*1.1
        return self.dummy_s6
    #insultin content randomly varied
    def insulin(self,emergency):
        self.dummy_s7 += random.randint(-8,8)*0.005
        self.dummy_s7 = round(self.dummy_s7,3)
        return self.dummy_s7
    #pressure increases linearly after heartbeat crosses 100
    def bloodpressure(self,emergency):
        if emergency is False:
            self.dummy_s8["sys"] += random.randint(-8,10) * 0.05
            self.dummy_s8["dia"] += random.randint(-4,6) * 0.05
        else:
            if self.dummy_s8["sys"] < 160 and self.dummy_s1 > 100:
                self.dummy_s8["sys"] += random.randint(3,5)
                self.dummy_s8["dia"] += random.randint(3,5)
            else:
                self.dummy_s8["sys"] += random.randint(-8,10) * 0.05
                self.dummy_s8["dia"] += random.randint(-4,6) * 0.05
        self.dummy_s8["sys"] = int(self.dummy_s8["sys"])
        self.dummy_s8["dia"] = int(self.dummy_s8["dia"])
       
        return self.dummy_s8
  

    def start(self):
        #output = {}
        output["ID"] = self.id
        output["D1"] = self.heart(emergency)
        output["D2"] = self.temperature(emergency)
        output["D3"] = self.gps(emergency)
        output["D4"] = self.spo2(emergency)
        output["D5"] = self.stress(emergency)
        output["D6"] = self.motion(emergency)
        output["D7"] = self.insulin(emergency)
        output["D8"] = self.bloodpressure(emergency)
        
        return output

def instantiate(id,emergency):
    dummy = Dummy(id,emergency)
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
    

    
dummy = instantiate(args.deviceID,emergency)
listener = threading.Thread(target=init_and_start,kwargs={'dummy':dummy},daemon=True)
#init_and_start(args.deviceID) #"Pass this to thread and this will output steady steam of values"
listener.start()


#CONTROL LOGIC STARTS from here
def peek(output): #gets instance of output
    return(output)
time.sleep(50)


#CURRENT THREAD..call peek withing a loop to periodically check
#should be called in a while loop
print("\n Parent thread looking at the output after 20 seconds ",peek(output))
#time.sleep(3)
