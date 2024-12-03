from discovery import discover
from leader_election import elections
from joystick_communication.joystick import KeyboardController
from utils.device_identity import get_device_identity
import time 

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

    # Discover network devices
    devices = discover.discover_neighbouring_devices()
    print(f"Discovered devices: {devices}")
    
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
            controller.run()  # Start the controller logic
        else:
            print("Error: Could not find leader's IP address")
    

    # Get device identity again as its updated after leader election    
    robot_identity = get_device_identity() 

    if robot_identity['role'] == "leader":
        leader_listen.listen_for_commands()
    elif robot_identity['role'] == "follower":
        follower_listen.listen_for_commands()

if __name__ == "__main__":
    main()
