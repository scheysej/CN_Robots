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
    leader = elections.simulate_leader_election()
    print(f"Elected leader: {leader}")
    
    # If this is a keyboard controller, start the control interface
    if device_type == "Keyboard":
        controller = KeyboardController()
        controller.run()

if __name__ == "__main__":
    main()
