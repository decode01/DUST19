import socket
import threading
from datetime import datetime
import argparse
import time
a_list = []
h_list = []
emergency_dict = {}
pat_count = 0

parser = argparse.ArgumentParser()
parser.add_argument('--port')
parser.add_argument('--deviceIP')
#parser.add_argument('--mode') "mode not required
args = parser.parse_args()
lock = False

if args.port is None:
    print("Please specify port")
    exit(1)

port = int(args.port)

def getAmbulanceDetails(name):
    found = None
    for details in a_list:
        if details.name == name:
            found = details
            break
    return found

def getPatientDetails(name):
    found = None
    for details in h_list:
        if details.name == name:
            found = details
            break
    return found

def getObjectByDetails(name,type):
    if type == 'H':
        return getPatientDetails(name)
    else:
        return getAmbulanceDetails(name)



class EmergencyServiceInNeed:
    def __init__(self,obj,lat,lon,patient_ip,emport):
        self.patient_details = obj
        self.lat = lat
        self.lon = lon
        self.patient_ip = patient_ip
        self.emport = emport
        self.allocatedv = None
        self.time = datetime.now()
        self.available = []
        self.getAvailableVehicle()
        self.responses = 0
        self.inBroadcast()
        self.eta = {}



        
    def inBroadcast(self):
        print("IP-hub",self.patient_ip)
        print("IP emport",self.emport)
        l_msg = "EM00:"+self.patient_details.name + ":" + self.lat + "," + self.lon + "," + self.patient_ip + "," + self.emport
        for v in self.available:
            print("Sending msg to {}".format(v.name))
            v.connector.send(l_msg.encode())

    def getAvailableVehicle(self):
        for v in a_list:
            if v.inuse == False:
                self.available.append(v)
        print("Total available:: {}".format(len(self.available)) )
    
    def assignVehicle(self,a_obj):
        self.allocatedv = a_obj
        l_mg ="EM02:"+self.patient_details.name+":"+self.lat+","+self.lon
        a_obj.connector.send(l_mg.encode())
    
    
    def allocateVehicle(self):
        global lock
        allocate = False
        print("Inside Allocate Vehicle")
        while True:
            vname = None
            etamin = float("inf")
            if (datetime.now() - self.time).seconds > 8 and not lock:
                
                print("Inside compare")
                for key in self.eta.keys():
                    if self.eta[key] != -1:
                        if not vname:
                            etamin = self.eta[key]
                            vname = key
                        if self.eta[key] < etamin and getAmbulanceDetails(vname).inuse == False:
                            etamin = self.eta[key]
                            vname = key
                if not vname:
                    print(self.eta.keys())
                    print("No Emergency service can be initiated now, connecting to Hub 2")
                else:
                    lock = True
                    getAmbulanceDetails(vname).inuse = True
                    self.assignVehicle(getAmbulanceDetails(vname))
                    time.sleep(4)
                    lock = False
                    break
                

    

        




class MType:
    def __init__(self,typ,name,connector,inuse = False):
        self.typ = typ
        self.name = name
        self.connector = connector
        self.inuse = inuse



class Register:
    def __init__(self,port,addr = str(args.deviceIP)):
        self.port = port
        self.addr = addr
        self.soc = socket.socket()
        print ("Central Socket successfully created")
        self.soc.bind((addr, port))
        print ("Socket binded to %s" %(port))
        self.soc.listen(5)
        print ("Socket is listening")
        connthread = threading.Thread(target=self.activeConnector,daemon=True)
        connthread.start()



    def activeConnector(self):
        global pat_count
        try:
            while True:
                c, addr = self.soc.accept()
                print ('Got connection from', addr )
                c.send('Thank you for connecting, Please provide registration info'.encode())
                data = c.recv(1024)
                raw_details = format(data.decode())
                details = raw_details.split(':')
                tmp_obj = MType(details[0],details[1],c)
                print("Registration Successfull for {}".format(details[1]))
                if details[0] == 'H':
                    pat_count += 1
                    if pat_count > 1:
                        time.sleep(4)
                    h_list.append(tmp_obj)
                    threading.Thread(target=self.activeListenPatient,kwargs={'obj':h_list[len(h_list)-1]},daemon=True).start()
                else:
                    a_list.append(tmp_obj)
                    threading.Thread(target=self.activeListenAmb,kwargs={'obj':a_list[len(a_list)-1]},daemon=True).start()
        finally:
            self.soc.close()
        
    
    def activeListenPatient(self,obj = None):
        if obj == None:
            print("Listening Object not defined")
        else:
            
            while True:
                data = obj.connector.recv(1024)
                msg = data.decode()
                print('\r{}: {}\n> '.format(obj.name,msg), end='')
                msg_split = msg.split(':')
                if msg_split[0] == 'EM00':
                    sensor_vals = msg_split[1].split(',')
                    print('\rEmrgency service initated for {} @ {}\n'.format(obj.name,msg_split[1]), end='')
                    em_obj = EmergencyServiceInNeed(obj,sensor_vals[0],sensor_vals[1],sensor_vals[2],sensor_vals[3])
                    emergency_dict[obj.name] = em_obj
                    threading.Thread(target=em_obj.allocateVehicle, daemon= True).start()
                    print('Done')
            

    

    def assignEmergencyObj(self, obj,msg_split):
        global emergency_dict
        try:
            emergency_dict[msg_split[1]].eta[obj.name] = float(msg_split[2])
            emergency_dict[msg_split[1]].responses += 1 #to ensure the change gets reflected
            #return em_obj
        except KeyError:
            time.sleep(1)
            self.assignEmergencyObj(obj,msg_split)
    
    def activeListenAmb(self,obj = None):
        global lock
        #global em_obj
        if obj == None:
            print("Listening Object not defined")
        else:
            while True:
                data = obj.connector.recv(1024)
                msg = data.decode()
                print('\r{}: {}\n> '.format(obj.name,msg), end='')
                msg_split = msg.split(':')
                if msg_split[0] == 'ETA':
                    self.assignEmergencyObj(obj,msg_split)
                    


chub = Register(port)








while True:
    msg = input('> ')
    details = msg.split(':')
    obj = getObjectByDetails(details[1],details[0])
    if obj == None:
        print("Details not found")
    else:
        obj.connector.send(details[2].encode())


    



    

