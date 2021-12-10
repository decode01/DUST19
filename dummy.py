# Written by the entire group - 19
# Almost all the time we worked on this project, we've physically met and peer programmed
# To peer program, we've used VSCODE LIVE SHARING, where we all coded on the same .py file together
# That's why it's quite hard to make a separation of who did what because we all coded together
# and debugged each others' code live.

# This file mostly written by DEEPAYAN DATTA

import numpy as np
import random
import time
import sys
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--deviceID')
args = parser.parse_args()
output = {}
if args.deviceID is None:
    print("Please enter device ID")
    exit(1)
class Dummy:
    def __init__(self,id):
        self.id = id
        #self.output = {}
        
        #self.fuel_start = fuel_start
    def dummy1(self):
        #can be fuel/heartbeat
        self.dummy_s1 = random.randint(70,90)
        #self.ful_start -= 0.01
        return self.dummy_s1
    def dummy2(self):
        self.dummy_s2 = random.randint(4,16)
        return self.dummy_s2
    def dummy3(self):
        self.dummy_s3 = random.randint(12,56)
        return self.dummy_s3
    def dummy4(self):
        self.dummy_s4 = random.randint(1,16)
        return self.dummy_s4
    def dummy5(self):
        self.dummy_s5 = random.randint(12,16)
        return self.dummy_s5
    def dummy6(self):
        self.dummy_s6 = random.randint(4,55)#*1.1
        return self.dummy_s6
    def dummy7(self):
        self.dummy_s7 = random.randint(45,55)#*1.1
        return self.dummy_s7
    def dummy8(self):
        self.dummy_s8 = random.randint(45,55)#*1.1
        return self.dummy_s8

    def start(self):
        #output = {}
        output["ID"] = self.id
        output["D1"] = self.dummy1()
        output["D2"] = self.dummy2()
        output["D3"] = self.dummy3()
        output["D4"] = self.dummy4()
        output["D5"] = self.dummy5()
        output["D6"] = self.dummy6()
        output["D7"] = self.dummy7()
        output["D8"] = self.dummy8()

        return output

def instantiate(id):
    dummy = Dummy(id)
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
    
def peek(output): #gets instance of output
    return(output)
    
dummy = instantiate(args.deviceID)
listener = threading.Thread(target=init_and_start,kwargs={'dummy':dummy},daemon=True)
#init_and_start(args.deviceID) #"Pass this to thread and this will output steady steam of values"
listener.start()
time.sleep(20)


#CURRENT THREAD..call peek withing a loop to periodically check
#should be called in a while loop
print("\n Parent thread looking at the output after 20 seconds ",peek(output))
#time.sleep(3)
