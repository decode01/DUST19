# DUST19
In this project, we aimed to combine two main concepts discussed throughout the SC module: 
    i) vehicular setting 
    ii) body area network
The purpose of the project was to provide real-time communication between three main systems: 
a hub network, ambulance nw (vehicles) and body-area networks (patients with sensors) 
and efficiently allocate ambulances to patients based on various logic statements in the control layer. 
The centralization aspect in our infrastructure (client-server) consists of the communication between our Hub (server) and 
ambulances + patients (clients). On top of the central communication infrastructure, we aimed to add a peer-to-peer aspect 
to our project as well: ambulances to patients and patients to ambulances. Both ambulances and body-area networks communicate 
through a peer2peer fashion once they establish a socket connection (e.g, once the Hub allocates an ambulance to the patient). 
We’ve used around 8 sensors for both the ambulance and the body-area network, and based on the sensor readings, 
the logic in our control layer determines whether a patient’s sensor values are not within a predetermined range and 
requires medical assistance (e.g., hub assigns an ambulance to the patient, etc). We also aimed to separate 
the Data Layer from the Control Layer as much as we could. The Data Layer mostly consists of various sensor readings and 
the control layer includes the logic that determines whether the sensor readings of a body-area network is not within a 
given range (body-area network) and one that.

* There are four runme files corresponding to four different use-cases that need to be executed. These runme files together with their respective scenarios and their execution commands can be found in the below table.
* Since each runme file uses the same ports, we have included a "killall" linux command at the end of each shell script to run after 120 seconds ( estimated time of execution ).These scripts would self terminate after 120 seconds each.
* However, as a precautionary measure, we would suggest that you should wait for about 2-3 minutes in between each runme execution( e.g.,bash runme1.sh <---2/3 minutes-----> bash runme2.sh ,etc) corresponding to the different scenarios.
* Now, all the runme scripts need to be executed in pi37 separately, but the underlying python codes have the flexibility to be executed in any of the pi-s. You could verify from the screenshots included in the report, that the hub_n, ambulance and the body_data scripts were run in both pi-s 37 and 38.


**STEPS TO BE FOLLOWED FOR REPLICATING THE USE CASES (each runme corresponds to a different scenario):**
    
| Scenarios | Scripts  | Execution | Pi
| :------------ |:---------------:| -----:|------:|
| one hub, two ambulances( one faulty, one working) and one patient having a heart attack     | runme1.sh       | bash runme1.sh | 10.35.70.37 |
| one hub, two ambulances ( both faulty), one patient (having heart attack)     | runme2.sh       | bash runme2.sh | 10.35.70.37 |
| one hub, two ambulances ( both working), one patient (having heart attack) | runme3.sh       | bash runme3.sh | 10.35.70.37 |
| one hub, three ambulances ( one faulty, two working), three patients( two having heart attacks,one healthy ) | runme4.sh       | bash runme4.sh | 10.35.70.37 |


