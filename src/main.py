from discovery import discover
from leader_election import elections
from joystick_communication.joystick import KeyboardController
from utils.device_identity import get_device_identity

def main():
    # Get device identity
    _, device_type = get_device_identity()
    
    # Discover network devices
    devices = discover.discover_neighbouring_devices()
    print(f"Discovered devices: {devices}")
    
    # Run leader election
    leader = elections.simulate_leader_election(devices)
    print(f"Elected leader: {leader}")
    
    # If this is a keyboard controller, start the control interface
    if device_type == "Keyboard":
        # find leader's IP from devices list
        leader_ip = next((device['IP'] for device in devices if device['ID'] == leader), None)
        if leader_ip:
            controller = KeyboardController(leader_ip=leader_ip, leader_id=leader)
            controller.run()
        else:
            print("Error: Could not find leader's IP address")

if __name__ == "__main__":
    main()