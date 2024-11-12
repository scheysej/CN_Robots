"""
Author: Benyamain Yacoob
Date: 11-11-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import socket
import time
import os
import json
from hashlib import sha256
from utils.device_identity import get_device_identity

class JoystickController:
    def __init__(self):
        self.id, _ = get_device_identity()  # We know it's a joystick
        self.device_type = "Joystick"
        self.ip = self.get_local_ip()
        self.status = "Active"
        self.role = "Controller"
        self.leader_ip = None
        self.leader_port = 5005
        self.leader_id = None
        
    def get_local_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    def wait_for_leader(self):
        while True:
            try:
                with open('leader_info.txt', 'r') as f:
                    self.leader_ip = f.readline().strip()
                    self.leader_id = f.readline().strip()
                if self.leader_ip and self.leader_id:
                    break
            except FileNotFoundError:
                print("Waiting for leader election to complete...")
                time.sleep(1)

    def create_message(self, x, y, button_state):
        """Create a signed message that can be validated by the leader."""
        message = {
            "id": self.id,
            "device_type": self.device_type,
            "ip": self.ip,
            "status": self.status,
            "role": self.role,
            "joystick_x": x,
            "joystick_y": y,
            "button_state": button_state,
            "timestamp": time.time()
        }
        # add signature for validation
        message["signature"] = self.sign_message(message)
        return json.dumps(message)

    def sign_message(self, message_dict):
        message_str = str(message_dict["id"]) + str(message_dict["timestamp"])
        return sha256(message_str.encode()).hexdigest()

    def send_to_leader(self, message):
        """Send message to leader with error handling."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(message.encode(), (self.leader_ip, self.leader_port))
                print(f"Sent message to leader at {self.leader_ip}:{self.leader_port}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def run(self):
        self.wait_for_leader()
        print(f"Connected to leader at {self.leader_ip}")

        while True:
            try:
                # Read joystick inputs
                x = os.system("joystick_read x")
                y = os.system("joystick_read y")
                buttons = os.system("joystick_read buttons")

                # Create and send message
                message = self.create_message(x, y, buttons)
                self.send_to_leader(message)

                time.sleep(0.1)  # Adjust rate as needed
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)

if __name__ == "__main__":
    controller = JoystickController()
    controller.run()
