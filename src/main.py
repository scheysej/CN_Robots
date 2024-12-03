from discovery import discover
from leader_election import elections
from joystick_communication.joystick import KeyboardController
from utils.device_identity import get_device_identity
import time 

def main():
    # Get device identity
    robot_identity = get_device_identity() 

    # Discover network devices
    devices = discover.discover_neighbouring_devices()
    print(f"Discovered devices: {devices}")
    
    # Run leader election
    if robot_identity['device_type'] == "robot":
        from command_broadcast import listen
        from command_broadcast import follower_listen

        leader = elections.simulate_leader_election(devices)
        print(f"Elected leader: {leader}")
        
    
    # if device_type == "Keyboard":
    #     elected_leader = elections.keyboard_listen_election(devices)
    #     if elected_leader:
    #         # Find leader's IP from devices list
    #         leader_ip = None
    #         for device in devices:
    #             if device["DeviceType"] != "Keyboard" and str(device["ID"]) == str(elected_leader):
    #                 leader_ip = device["IP"]
    #                 break
        
    #     if leader_ip:
    #         controller = KeyboardController(leader_ip=leader_ip, leader_id=elected_leader)
    #         controller.run()  # Start the controller logic
    #     else:
    #         print("Error: Could not find leader's IP address")
    # elif device_type == "Leader":
    #     listen.listen_for_commands()
    # elif device_type == "Robot":
    #     follower_listen.listen_for_commands()

if __name__ == "__main__":
    main()
