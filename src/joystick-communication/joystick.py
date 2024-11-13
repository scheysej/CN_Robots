"""
Author: Benyamain Yacoob
Date: 11-11-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import socket
import time
import json
import keyboard
from hashlib import sha256
from utils.device_identity import get_device_identity

class KeyboardController:
    def __init__(self):
        self.id, _ = get_device_identity()
        self.device_type = "Keyboard"
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

    def read_keyboard_input(self):
        x = 0  # -100 (left) to 100 (right)
        y = 0  # -100 (down) to 100 (up)
        
        if keyboard.is_pressed('up'):
            y = 100
        elif keyboard.is_pressed('down'):
            y = -100
            
        if keyboard.is_pressed('left'):
            x = -100
        elif keyboard.is_pressed('right'):
            x = 100
            
        return x, y

    def create_message(self, x, y):
        """Create a signed message that can be validated by the leader."""
        message = {
            "id": self.id,
            "device_type": self.device_type,
            "ip": self.ip,
            "status": self.status,
            "role": self.role,
            "movement_x": x,
            "movement_y": y,
            "timestamp": time.time()
        }
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
                print(f"Sent movement command to leader: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def run(self):
        print("Starting keyboard controller. Use arrow keys to control robots.")
        print("Press Ctrl+C to exit.")
        
        self.wait_for_leader()
        print(f"Connected to leader at {self.leader_ip}")

        while True:
            try:
                x, y, _ = self.read_keyboard_input()
                
                # only send message if there's actual movement
                if x != 0 or y != 0:
                    message = self.create_message(x, y, 0)
                    self.send_to_leader(message)

                time.sleep(5.0)
                
            except KeyboardInterrupt:
                print("\nKeyboard controller stopped.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)

if __name__ == "__main__":
    # run sudo for keyboard access
    controller = KeyboardController()
    controller.run()