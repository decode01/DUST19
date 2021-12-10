# Written by the entire group - 19
# Almost all the time we worked on this project, we've physically met and peer programmed
# To peer program, we've used VSCODE LIVE SHARING, where we all coded on the same .py file together
# That's why it's quite hard to make a separation of who did what because we all coded together
# and debugged each others' code live.

import random
import time
import sys
import threading
import argparse
import socket


parser = argparse.ArgumentParser()
parser.add_argument('--deviceID')
parser.add_argument('--mode')
parser.add_argument('--port')
parser.add_argument('--emport')
parser.add_argument('--hubIP')
parser.add_argument('--patientIP')
args = parser.parse_args()


output = {}
emergency = True
chub_port =  int(args.port)
chub_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chub_emchannel = False
#em_port =  int(args.emport)


if args.deviceID is None:
    print("Please enter device ID")
    exit(1)
if args.mode is None:
    emergency = False
    
if args.emport is None:
    print("Please specify patient port")
    exit(1)
em_port =  int(args.emport)
if args.patientIP is None:
    print("Please enter patient IP")
patientIP = str(args.patientIP)

# DEEPAYAN
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
            self.dummy_s1 += random.randint(-8,8)*0.005
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
# KEMAL
def instantiate(id,emergency):
    dummy = Dummy(id,emergency)
    return dummy
def init_and_start(dummy):
    #dummy = Dummy(id)
    global output
    while True:
        #time.sleep(1)
        output = dummy.start()
        time.sleep(.1)
        # print(output, end= "   \r")
    #sys.stdout.flush()

# DEEPAYAN / KEMAL
def connectandregistertochub():
    chub_socket.connect((str(args.hubIP), chub_port))
    print (chub_socket.recv(1024).decode())
    l_msg = "H:"+ args.deviceID
    chub_socket.send(l_msg.encode())

connectandregistertochub()
dummy = instantiate(args.deviceID,emergency)
listener = threading.Thread(target=init_and_start,kwargs={'dummy':dummy},daemon=True)
#init_and_start(args.deviceID) #"Pass this to thread and this will output steady steam of values"
listener.start()

#CONTROL LOGIC STARTS from here
def peek(): #gets instance of output
    global output
    return(output)




def emergencycomm(errcode = '',lat = 0, lon = 0):
    l_msg = "EM00:"+str(lat)+','+str(lon)+','+str(args.patientIP) + ','+str(args.emport)
    print(l_msg)
    chub_socket.send(l_msg.encode())
    emergency_channel_activate()

def activeListener(soc = None):
    c, addr = soc.accept()
    print ('Got connection from', addr )
    while True:
        data = c.recv(1024)
        msg = data.decode()
        print('Em Responce: {}\n> '.format(msg), end='')
        if msg == "Reached":
            c.close()
            break

# UNNI
def emergency_channel_activate():
    em_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Emergency communication channel successfully created")
    em_soc.bind((str(args.patientIP), em_port))
    print ("Socket binded to %s" %(em_port))
    em_soc.listen(5)
    print ("Socket is listening")
    try:
        threading.Thread(target=activeListener, kwargs={'soc' : em_soc}, daemon=True).start()
    finally:
        em_soc.close()
    while True:
        pass


# TOM
def send_to_hub():
    #communicate to hub
    #LP - Low Pressure
    #HA - Heart Attack
    #HH - High Insulin
    global chub_emchannel
    initiate_emergency_service = False
    dict = peek()
    code = ''
    if dict["D1"] < 60 and dict["D6"] == "no":
        initiate_emergency_service = True
        print("Low Pressure and fainted")
        code = 'LP'
        #Low Pressure and fainted | dict["D3"] needs to be passed
    if dict["D1"] > 150 and dict["D2"] > 37.5 and dict["D8"]["sys"]  > 150 :
        initiate_emergency_service = True
        print("Heart attack")
        code = 'HA'
        #Heart attack | dict["D3"] needs to be passed
    if dict["D7"] > 0.25:
        # initiate_emergency_service = True
        # print('Insulin high')
        code = 'HH'
        #Sugar High | dict["D3"] needs to be passed
    if initiate_emergency_service and chub_emchannel == False :
        #communicate with hub
        chub_emchannel = True
        print("Inside emergency block")
        emergencycomm(code,dict["D3"]["lat"],dict["D3"]["lon"])
        
    
while True:
    time.sleep(5) #checks for patient condition every 10 seconds . can be changed later
    #print("\n\nOutput after 10 seconds",peek()) #just checking
    send_to_hub()
    #break

#CURRENT THREAD..call peek withing a loop to periodically check
#should be called in a while loop
print("\n Parent thread looking at the output after 20 seconds ",peek(output))
#time.sleep(3)
