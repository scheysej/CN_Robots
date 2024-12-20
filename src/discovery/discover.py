"""
Author: Eyiara Oladipo
Date: 11-11-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import socket
import threading
import time
from utils.device_identity import get_device_identity

# Get the local IP address of the machine
def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Use any reachable IP
        return s.getsockname()[0]

LOCAL_IP_ADDRESS = get_local_ip()
BROADCAST_ADDR = '255.255.255.255' # Define the broadcast address and port
PORT = 65009

def create_broadcast_message(robot_identity):
        return f"""MessageType: DISCOVER
        DeviceID: {robot_identity['device_id']}
        DeviceType: {robot_identity['device_type']}
        IP: {LOCAL_IP_ADDRESS}
        RobotBrand: {robot_identity['robot_brand']}
        """
    
def create_object_representation(robot_identity):
        return {
            'DeviceID': robot_identity['device_id'],
            'DeviceType': robot_identity['device_type'],
            'IP': LOCAL_IP_ADDRESS,
            'RobotBrand': robot_identity['robot_brand']
        }

    
# Function to broadcast a message
def broadcast(broadcast_message, stop_event):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as broadcast_socket:
        # Since by default, sockets cant send broadcast messages, this will allow it
        # to brodcast on 255.255.255.255
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print(f"Broadcasting message: {broadcast_message}")
        
        # While the stop event has not been called, the robot broadcasts itself every 1 second
        while not stop_event.is_set():
            broadcast_socket.sendto(broadcast_message.encode(), (BROADCAST_ADDR, PORT))
            time.sleep(1)

        print("Broadcasting has stopped")

# Function to listen for broadcast messages
def listen(discovered_devices, lock, stop_event):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listen_socket:
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(('', PORT))

        print(f"Listening on port {PORT} for broadcasts...")

        while not stop_event.is_set():
            try:
                listen_socket.settimeout(1) 
                data, addr = listen_socket.recvfrom(1024)
                sender_ip = addr[0]
                
                # Ignore messages from itself
                if sender_ip == LOCAL_IP_ADDRESS:
                    continue  

                message = data.decode().strip().splitlines()
                
                message_type = message[0].split(":")[1].strip()
                
                if message_type == 'DISCOVER':

                    # Parse the broadcast message into a dictionary
                    device_info = {
                        'DeviceID': int(message[1].split(":")[1].strip()),
                        'DeviceType': message[2].split(":")[1].strip(),
                        'IP': message[3].split(":")[1].strip(),
                        'RobotBrand': message[4].split(":")[1].strip(),
                    }
                    
                    with lock:
                        # Avoid duplicate devices with the same ID
                        if not any(device['DeviceID'] == device_info['DeviceID'] for device in discovered_devices):
                            discovered_devices.append(device_info)
                            print(f"Discovered device: {device_info}")

            except socket.timeout:
                continue

        print("Listening has stopped")

# Start the broadcasting and listening threads
def discover_neighbouring_devices():
    robot_identity = get_device_identity()
    BROADCAST_MESSAGE = create_broadcast_message(robot_identity)
    
    discovered_devices = []  
    discovered_devices.append(create_object_representation(robot_identity))

    lock = threading.Lock()
    stop_event = threading.Event()

    # Create and start broadcast and listen threads
    broadcast_thread = threading.Thread(target=broadcast, args=(BROADCAST_MESSAGE, stop_event), daemon=True)
    listen_thread = threading.Thread(target=listen, args=(discovered_devices, lock, stop_event), daemon=True)

    broadcast_thread.start()
    listen_thread.start()

    # Run for 20 seconds, then stop both threads
    time.sleep(10)
    stop_event.set()

    # Wait for both threads to finish
    broadcast_thread.join()
    listen_thread.join()

    return discovered_devices
