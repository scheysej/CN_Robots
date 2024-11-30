from discovery import discover
from leader_election import elections
from joystick_communication.joystick import KeyboardController
from utils.device_identity import get_device_identity
import time 

def main():
    # Get device identity
    _, device_type = get_device_identity()

    # Discover network devices
    devices = discover.discover_neighbouring_devices()
    print(f"Discovered devices: {devices}")
    
    #time.sleep(10) #This makes it so that messages sent from discovery dont try to get interpreted as elections

    # Run leader election
    if device_type == "Robot":
        from command_broadcast import listen
        leader = elections.simulate_leader_election(devices)
        print(f"Elected leader: {leader}")

    elected_leader = elections.keyboard_listen_election(devices)    
    if elected_leader:
            # Find leader's IP from devices list
            leader_ip = None
            for device in devices:
                if device["DeviceType"] == "Robot" and str(device["ID"]) == str(elected_leader):
                    leader_ip = device["IP"]
                    break


    if device_type == "Keyboard":        
        if leader_ip:
            controller = KeyboardController(leader_ip=leader_ip, leader_id=elected_leader)
            controller.run()  # Start the controller logic
        else:
            print("Error: Could not find leader's IP address")
    elif device_type == "Robot":
        listen.listen_for_commands()

if __name__ == "__main__":
    main()
