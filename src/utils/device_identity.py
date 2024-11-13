"""
Author: Benyamain Yacoob
Date: 11-12-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import os
import json
import glob

def find_project_root():
    """Find the CN_Robots directory"""
    home = os.path.expanduser("~")
    cn_robots = glob.glob(f"{home}/**/CN_Robots", recursive=True)
    if not cn_robots:
        raise Exception("CN_Robots directory not found")
    return cn_robots[0]

def find_keyboard_device():
    """Check for keyboard presence"""
    # TODO - FIND WAY TO TEST WITHOUT KEYBOARD SO THAT RASPBERRY PIS ARENT ALWAYS DETECTED AS KEYBOARD
    # keyboard_devices = glob.glob("/dev/input/by-id/*kbd*")
    # return bool(keyboard_devices)
    return False

def get_device_identity():
    project_root = find_project_root()
    identity_file = os.path.join(project_root, "device_identity.json")
    
    if os.path.exists(identity_file):
        with open(identity_file, 'r') as f:
            identity = json.load(f)
            return identity['id'], identity['type']
    
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    serial = line.split(':')[1].strip()
                    device_id = int(serial[-6:], 16)
                    break
    except:
        raise Exception("Could not read Raspberry Pi serial number")
    
    device_type = "Robot"
    # if find_keyboard_device():
    #     device_type = "Keyboard"
    
    identity = {
        'id': device_id,
        'type': device_type,
        'serial': serial
    }
    
    with open(identity_file, 'w') as f:
        json.dump(identity, f)
    
    return device_id, device_type 