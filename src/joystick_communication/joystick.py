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
import threading

class KeyboardController:
    def __init__(self, leader_ip=None, leader_id=None):
        self.id, _ = get_device_identity()
        self.device_type = "Keyboard"
        self.ip = self.get_local_ip()
        self.status = "Active"
        self.role = "Controller"
        self.leader_ip = leader_ip
        self.leader_port = 65009
        self.leader_id = leader_id
        self.last_x_command = "center"
        self.last_y_command = "stop"
        self.listen_port = 65010
        self.stop_event = threading.Event()
        
    def get_local_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    def read_keyboard_input(self):
        x_command = "center"  # default steering position
        y_command = "stop"    # default movement state
        
        # horizontal movement (steering)
        if keyboard.is_pressed('left'):
            x_command = "left"
        elif keyboard.is_pressed('right'):
            x_command = "right"
        # when neither left nor right is pressed, it will remain "center"
        
        # vertical movement
        if keyboard.is_pressed('up'):
            y_command = "forward"
        elif keyboard.is_pressed('down'):
            y_command = "backward"
        # when neither up nor down is pressed, it will remain "stop"
        
        commands_changed = (x_command != self.last_x_command or 
                          y_command != self.last_y_command)
        
        self.last_x_command = x_command
        self.last_y_command = y_command
        
        return x_command, y_command, commands_changed

    def create_message(self, x_command, y_command):
        """Create a signed message that can be validated by the leader."""
        message = {
            "id": self.id,
            "device_type": self.device_type,
            "ip": self.ip,
            "status": self.status,
            "role": self.role,
            "movement_x": x_command,
            "movement_y": y_command,
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

    def start_listener(self):
        """Start listening for responses from leader."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', self.listen_port))
            sock.settimeout(1)  # 1 second timeout
            print(f"Listening for responses on port {self.listen_port}")
            
            while not self.stop_event.is_set():
                try:
                    data, addr = sock.recvfrom(1024)
                    message = json.loads(data.decode())
                    print(f"Received response from {addr}: {message}")
                    
                except socket.timeout:
                    continue
                except json.JSONDecodeError:
                    print("Received malformed JSON message")
                except Exception as e:
                    print(f"Error in listener: {e}")

    def run(self):
        print("Starting keyboard controller. Use arrow keys to control robots.")
        print("Press Ctrl+C to exit.")
        
        if not self.leader_ip or not self.leader_id:
            print("Error: No leader information provided")
            return
        
        print(f"Connected to leader at {self.leader_ip}")

        listener_thread = threading.Thread(target=self.start_listener, daemon=True)
        listener_thread.start()

        while True:
            try:
                x_command, y_command, commands_changed = self.read_keyboard_input()
                
                # only send message if commands changed
                if commands_changed:
                    message = self.create_message(x_command, y_command)
                    self.send_to_leader(message)

                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\nKeyboard controller stopped.")
                self.stop_event.set()  # stop listener thread
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)

if __name__ == "__main__":
    # run sudo for keyboard access
    controller = KeyboardController()
    controller.run()