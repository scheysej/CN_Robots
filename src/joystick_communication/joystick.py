"""
Author: Benyamain Yacoob
Date: 11-11-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import socket
import time
import json
from hashlib import sha256
from utils.device_identity import get_device_identity
import threading
from pynput import keyboard

import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../command_broadcast"))
)
import broadcast


class StopAndPrepareForReelection(Exception):
    pass

class KeyboardController:
    def __init__(self, leader_ip=None, leader_id=None):
        devc = get_device_identity()
        self.id = devc["device_id"]
        self.devices_list = None
        self.device_type = "Keyboard"
        self.ip = self.get_local_ip()
        self.status = "Active"
        self.role = "Controller"
        self.leader_ip = leader_ip
        self.leader_port = 65009
        self.leader_id = leader_id
        self.last_x_command = "center"
        self.last_y_command = "stop"
        self.listen_port = 65009
        self.stop_event = threading.Event()

        # Initialize the keyboard listener
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener_thread = threading.Thread(target=self.start_listener, daemon=True)
        self.dynamic_joining_thread = threading.Thread(target=self.dynamic_joining_listener, daemon=True)
       
        # State variables for movement commands
        self.x_command = "center"
        self.y_command = "stop"

    def get_local_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    def on_press(self, key):
        """Handles key press events."""
        try:
            if key == keyboard.Key.left:
                self.x_command = "left"
            elif key == keyboard.Key.right:
                self.x_command = "right"
            elif key == keyboard.Key.up:
                self.y_command = "forward"
            elif key == keyboard.Key.down:
                self.y_command = "backward"
        except AttributeError:
            pass

    def on_release(self, key):
        """Handles key release events."""
        try:
            # Reset commands when keys are released
            if key == keyboard.Key.left or key == keyboard.Key.right:
                self.x_command = "center"
            elif key == keyboard.Key.up or key == keyboard.Key.down:
                self.y_command = "stop"
        except AttributeError:
            pass

        # Stop listener when escape key is pressed
        if key == keyboard.Key.esc:
            return False

    def create_message(self, x_command, y_command):
        """Create a signed message that can be validated by the leader."""
        message = {
            "type": "KEYBOARD_COMMAND",
            "id": self.id,
            "device_type": self.device_type,
            "ip": self.ip,
            "status": self.status,
            "role": self.role,
            "movement_x": x_command,
            "movement_y": y_command,
            "timestamp": time.time(),
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
                # print(f"Sent movement command to leader: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def dynamic_joining_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 65099))
            stop_event_dynamic_joining = threading.Event()

            print(f"Listening for join requests on port 65099")
            devices = self.devices_list

            print("All devices", devices)
            while not stop_event_dynamic_joining.is_set():
                try:
                    data, addr = sock.recvfrom(1024)

                    message = data.decode().strip().splitlines()
                
                    message_type = message[0].split(":")[1].strip()
                    
                    if message_type == 'REQUEST_TO_JOIN':
                        device_info = {
                            'DeviceID': int(message[1].split(":")[1].strip()),
                            'DeviceType': message[2].split(":")[1].strip(),
                            'IP': message[3].split(":")[1].strip(),
                            'RobotBrand': message[4].split(":")[1].strip(),
                        }
                    
                        device_exists = any(device['IP'] == device_info['IP'] or device['DeviceID'] == device_info['DeviceID'] for device in devices)
                        
                        if device_exists:
                            continue  

                        print("JOIN REQUEST RECEIVED AND PROCESSED")
                        print(data, addr)

                         # Prepare the response
                        response_message = "ACCEPTED"
                        response = response_message.encode()
                        print("SEND REQUEST")

                        #Send to each robot in devices to stop moving
                        self.stopForReelection()

                        #Send to the robot that its request has been heard and it is now part of the robot fleet
                        sock.sendto(response, (device_info['IP'], 65099))
                        print("Response sent to: ", addr)

                        raise StopAndPrepareForReelection()

                        #message = json.loads(data.decode())
                        # broadcast.broadcast_message(data)
                        #print(f"Received response from {addr}: {message}")
                except StopAndPrepareForReelection:
                        print("Restarting...")
                        os.execv(sys.executable, ['python'] + sys.argv)
                except socket.timeout:
                        continue
                except json.JSONDecodeError:
                        print("Received malformed JSON message")
                except Exception as e:
                        print(f"Error in listener: {e}")
  

    def stopForReelection(self):
        print("Stop and request for reelection")

        message = {
            "type": "STOP_AND_PREPARE_FOR_REELECTION",
            "id": self.id,
            "device_type": self.device_type,
            "timestamp": time.time()
        }

        message["signature"] = self.sign_message(message)
        msg = json.dumps(message)
        self.send_to_leader(msg)

        print("message sent")

    def start_listener(self):
        """Start listening for responses from leader."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("", self.listen_port))
            print(f"Listening for responses on port {self.listen_port}")

            while not self.stop_event.is_set():
                try:
                    data, addr = sock.recvfrom(1024)
                    # message = json.loads(data.decode())
                    broadcast.broadcast_message(data)
                    # print(f"Received response from {addr}: {message}")
                except socket.timeout:
                    continue
                except json.JSONDecodeError:
                    print("Received malformed JSON message")
                except Exception as e:
                    print(f"Error in listener: {e}")

    def run(self, devices):
        print("Starting keyboard controller. Use arrow keys to control robots.")
        print("Press Ctrl+C to exit.")
        self.devices_list = devices
        
        if not self.leader_ip or not self.leader_id:
            print("Error: No leader information provided")
            return

        print(f"Connected to leader at {self.leader_ip}")

        # Start the listener thread
        self.listener_thread.start()
        self.dynamic_joining_thread.start()
        self.listener.start()
        

        try:
            while True:
                # Only send message if commands have changed
                message = self.create_message(self.x_command, self.y_command)
                self.send_to_leader(message)
                
                time.sleep(0.1)  # Small delay to prevent CPU overuse

        except KeyboardInterrupt:
            print("\nKeyboard controller stopped.")
            self.stop_event.set()  # stop listener thread
            self.listener.stop()  # Stop the pynput listener thread
            self.listener_thread.join()  # Wait for listener thread to finish


if __name__ == "__main__":
    # run sudo for keyboard access
    controller = KeyboardController()
    controller.run()
