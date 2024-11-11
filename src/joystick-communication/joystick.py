"""
Author: Benyamain Yacoob
Date: 11-11-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import socket
import time
import os

LEADER_IP = None  # set this later once the leader is identified
LEADER_PORT = 5005

def create_joystick_message(id, device_type, ip, status, role, x, y, button_state):
    """
    Create a joystick control message following the protocol.

    Parameters:
    id (int): Unique identifier for the joystick
    device_type (str): Type of the device (e.g., "Joystick")
    ip (str): IP address of the joystick
    status (str): Status of the joystick (e.g., "Active")
    role (str): Role of the joystick (e.g., "Undecided")
    x (int): X-axis value of the joystick (-100 to 100)
    y (int): Y-axis value of the joystick (-100 to 100)
    button_state (int): Bitfield representing the state of the joystick buttons

    Returns:
    str: The formatted joystick control message
    """
    return f"ID: {id}\nDeviceType: {device_type}\nIP: {ip}\nStatus: {status}\nRole: {role}\nJoystickX: {x}\nJoystickY: {y}\nButtonState: {button_state}"

def send_to_leader(message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        data = message.encode('utf-8')
        sock.sendto(data, (LEADER_IP, LEADER_PORT))
        print(f"Sent message to {LEADER_IP}:{LEADER_PORT}")
        print(message)

if __name__ == "__main__":
    # wait for the discovery process to complete and identify the leader
    while LEADER_IP is None:
        try:
            from discovery import LEADER_IP
            break
        except ImportError:
            print("Waiting for the discovery process to identify the leader...")
            time.sleep(1)

    # assuming we have an external joystick controller connected
    joystick_id = 9294
    joystick_device_type = "Joystick"
    joystick_ip = "111.222.333.444"
    joystick_status = "Active"
    joystick_role = "Undecided"

    while True:
        # joystick_x: Represents the X-axis value of the joystick (-100 to 100)
        # joystick_y: Represents the Y-axis value of the joystick (-100 to 100)
        # joystick_buttons: Represents the bitfield of the joystick buttons
        joystick_x = os.system("joystick_read x")
        joystick_y = os.system("joystick_read y")
        joystick_buttons = os.system("joystick_read buttons")

        message = create_joystick_message(
            joystick_id, joystick_device_type, joystick_ip,
            joystick_status, joystick_role, 0, 0, 0
        )
        send_to_leader(message)

        time.sleep(0.5)