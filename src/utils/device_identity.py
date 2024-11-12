"""
Author: Benyamain Yacoob
Date: 11-12-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import os
import json

def get_device_identity():
    """
    Get or create a persistent device identity using the Raspberry Pi's serial number.
    """
    identity_file = "/home/pi/device_identity.json"
    
    if os.path.exists(identity_file):
        with open(identity_file, 'r') as f:
            identity = json.load(f)
            return identity['id'], identity['type']
    
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    serial = line.split(':')[1].strip()
                    # Use last 6 digits of serial as device ID
                    device_id = int(serial[-6:], 16)
                    break
    except:
        raise Exception("Could not read Raspberry Pi serial number")
    
    # Determine device type based on connected hardware or configuration file
    device_type = "Robot"
    try:
        # Check for joystick hardware connection
        if os.path.exists("/dev/input/js0"):
            device_type = "Joystick"
    except:
        pass
    
    identity = {
        'id': device_id,
        'type': device_type,
        'serial': serial
    }
    with open(identity_file, 'w') as f:
        json.dump(identity, f)
    
    return device_id, device_type 