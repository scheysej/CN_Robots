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
    
    time.sleep(10) #This makes it so that messages sent from discovery dont try to get interpreted as elections

    # Run leader election
    leader = elections.simulate_leader_election(devices)
    print(f"Elected leader: {leader}")
    
    # If this is a keyboard controller, start the control interface
    if device_type == "Keyboard":
        # Find leader's IP from devices list
        leader_ip = next((device['IP'] for device in devices if device['ID'] == leader), None)
        
        if leader_ip:
            controller = KeyboardController(leader_ip=leader_ip, leader_id=leader)
            controller.run()  # Start the controller logic
        else:
            print("Error: Could not find leader's IP address")

if __name__ == "__main__":
    main()
