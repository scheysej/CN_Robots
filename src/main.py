from discovery import discover
from leader_election import elections
from joystick_communication.joystick import KeyboardController
from utils.device_identity import get_device_identity
<<<<<<< HEAD
from command_broadcast import listen
import time


def main():
    # Get device identity
    _, device_type = get_device_identity()
=======
import time 
import json
import socket
import threading

def main():
    # Get device identity
    # Robot identity will look like
    # {
    #   'device_id': device_id,
    #    'device_type': device_type,
	#    'robot_brand': robot_brand,
    #    'role': "undecided"
    # }

    robot_identity = get_device_identity() 
>>>>>>> clean

    # Discover network devices
    devices = discover.discover_neighbouring_devices()
    print(f"Discovered devices: {devices}")
<<<<<<< HEAD

    # time.sleep(10) #This makes it so that messages sent from discovery dont try to get interpreted as elections

=======
    
>>>>>>> clean
    # Run leader election
    if robot_identity['device_type'] == "robot":
        from command_broadcast import leader_listen
        from command_broadcast import follower_listen

        # devices array will look like 
        # [{
        #  'DeviceID':  100002342,
        #  'DeviceType': keyboard,
        #  'IP': 192.168.0.111,
        #  'RobotBrand': osoyoo
        # }]

        leader = elections.simulate_leader_election(devices)
        print(f"Elected leader: {leader}")
<<<<<<< HEAD

    if device_type == "Keyboard":
        elected_leader = elections.keyboard_listen_election(devices)
        if elected_leader:
            # Find leader's IP from devices list
            leader_ip = None
            for device in devices:
                if device["DeviceType"] == "Robot" and str(device["ID"]) == str(elected_leader):
                    leader_ip = device["IP"]
                    break
                
            if leader_ip:
                # Initialize keyboard controller with verified leader
                controller = KeyboardController(leader_ip=leader_ip, leader_id=elected_leader)
                controller.run()
            else:
                print("Error: Could not find leader's IP address in devices list")
    elif device_type == "Robot":
        listen.listen_for_commands()
=======
        
    
    if robot_identity['device_type'] == "keyboard":
        elected_leader_id = elections.keyboard_listen_election(devices)
        
        if elected_leader_id:
            leader_ip = None

            for device in devices:
                if device["DeviceType"] != "keyboard" and str(device["DeviceID"]) == str(elected_leader_id):
                    leader_ip = device["IP"]
                    break
        

            if leader_ip:
                controller = KeyboardController(leader_ip=leader_ip, leader_id=elected_leader_id)
                controller.run(devices)  # Start the controller logic
            else:
                print("Error: Could not find leader's IP address")


    # Get device identity again as its updated after leader election    
    robot_identity = get_device_identity() 
    
    if 'role' in robot_identity:
        if robot_identity['role'] == "leader":
            leader_listen.listen_for_commands()
        elif robot_identity['role'] == "follower":
            follower_listen.listen_for_commands()
>>>>>>> clean


if __name__ == "__main__":
    main()
