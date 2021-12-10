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

Command to run the Hub
python3 hub_n.py --port <Hub Port> --deviceIP <Hub IP>
eg:- python3 hub_n.py --port 34000 --deviceIP 10.35.70.37

Command to run the Ambulance
python3 ambulance.py --deviceID <Ambulance unique ID> --port <Hub Port> --hubIP <Hub IP>
eg:- python3 ambulance.py --deviceID 125 --port 34000 --hubIP 10.35.70.37
If the Ambulance ID is even then it willbe considered as a faulty ambulance

Command to run the Body Area Network
python3 body_data.py --deviceID <Patient Name> --port <Hub Port> --mode <Mode> --emport <Patient Emergency Channel Port> --hubIP <Hub IP> --patientIP <Patient Emergency Channel IP>
eg:- python3 body_data.py --deviceID Evelyn --port 34000 --mode emergency --emport 33090 --hubIP 10.35.70.37 --patientIP 10.35.70.37
--mode is a optional paramater. If any value is passed it means that the patient would get an attack in a sepcific time.
    
| Scenarios | Scripts  | Execution | Pi
| :------------ |:---------------:| -----:|------:|
| one hub, two ambulances( one faulty, one working) and one patient having a heart attack     | runme1.sh       | bash runme1.sh | 10.35.70.37 |
| one hub, two ambulances ( both faulty), one patient (having heart attack)     | runme2.sh       | bash runme2.sh | 10.35.70.37 |
| one hub, two ambulances ( both working), one patient (having heart attack) | runme3.sh       | bash runme3.sh | 10.35.70.37 |
| one hub, three ambulances ( one faulty, two working), three patients( two having heart attacks,one healthy ) | runme4.sh       | bash runme4.sh | 10.35.70.37 |
