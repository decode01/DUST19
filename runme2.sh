#SCENARIO 2: one hub, two faulty ambulances and one patient having heart attacks
#Command to run the Hub
python3 hub_n.py --port 33000 --deviceIP 10.35.70.37 &
sleep  3
#Command to run the faulty Ambulance
python3 ambulance.py --deviceID 124 --port 33000 --hubIP 10.35.70.37 &

#sleep 2
#Command to run the faulty Ambulance
python3 ambulance.py --deviceID 126 --port 33000 --hubIP 10.35.70.37 &
sleep 3
#Command to run the Body Area Network
python3 body_data.py --deviceID Alice  --port 33000 --mode emergency --emport 33080 --hubIP 10.35.70.37 --patientIP 10.35.70.37 &
#Command to run the second Body area network
#python3 body_data.py --deviceID Bob  --port 33000 --mode emergency --emport 33060 --hubIP 10.35.70.37 --patientIP 10.35.70.37 &

#waiting for 120 seconds before killing the user ID
sleep 120
my_username=$USER
killall -u $my_username

