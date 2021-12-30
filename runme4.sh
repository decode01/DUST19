#SCENARIO 4: one hub, three ambulances( one faulty, two working) and three patients, two having  heart attacks and the other one is healthy
#Command to run the Hub
python3 hub_n.py --port 33000 --deviceIP 10.35.70.37 &
sleep  3
#Command to run the faulty Ambulance
python3 ambulance.py --deviceID 126 --port 33000 --hubIP 10.35.70.37 &

#sleep 2
#Command to run the working Ambulance
python3 ambulance.py --deviceID 125 --port 33000 --hubIP 10.35.70.37 &

#Command to run the working Ambulance
python3 ambulance.py --deviceID 127 --port 33000 --hubIP 10.35.70.37 &
sleep 3
#Command to run the Body Area Network
python3 body_data.py --deviceID Alice  --port 33000 --mode emergency --emport 33080 --hubIP 10.35.70.37 --patientIP 10.35.70.37 &
#Command to run the second Body area network
python3 body_data.py --deviceID Bob  --port 33000  --mode emergency --emport 33060 --hubIP 10.35.70.37 --patientIP 10.35.70.37 &
#Command to run the third  Body area network ( healthy scenario )
python3 body_data.py --deviceID Eve  --port 33000  --emport 33040 --hubIP 10.35.70.37 --patientIP 10.35.70.37 &


#waiting for 120 seconds before killing the user ID
sleep 120
my_username=$USER
killall -u $my_username

