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
    keyboard_devices = glob.glob("/dev/input/by-id/*kbd*")
    return bool(keyboard_devices)


def get_device_identity():
    project_root = find_project_root()
    identity_file = os.path.join(project_root, "device_identity.json")
    
    # Check for existing keyboard devices in identity files
    keyboard_count = 0
    if os.path.exists(identity_file):
        with open(identity_file, "r") as f:
            identity = json.load(f)
            if identity["type"] == "Keyboard":
                keyboard_count += 1
            return identity["id"], identity["type"]
            
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("Serial"):
                    serial = line.split(":")[1].strip()
                    device_id = int(serial[-6:], 16)
                    break
    except:
        raise Exception("Could not read Raspberry Pi serial number")

    device_type = "Robot"
    if find_keyboard_device():
        # Check network for other keyboard devices
        keyboard_files = glob.glob(os.path.join(os.path.dirname(project_root), "**/device_identity.json"), recursive=True)
        for kf in keyboard_files:
            try:
                with open(kf, "r") as f:
                    other_identity = json.load(f)
                    if other_identity["type"] == "Keyboard":
                        keyboard_count += 1
            except:
                continue
                
        if keyboard_count >= 2:
            print("Error: More than 2 keyboards detected in the network!")
            print("Please ensure only one keyboard controller is active.")
            exit(1)  # Exit the program
            
        device_type = "Keyboard"

    identity = {"id": device_id, "type": device_type, "serial": serial}

    with open(identity_file, "w") as f:
        json.dump(identity, f)

    return device_id, device_type
