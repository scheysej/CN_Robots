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
BROADCAST_ADDR = "255.255.255.255"  # Define the broadcast address and port
PORT = 65009


class Device:
    def __init__(self):
        self.id, self.device_type = get_device_identity()
        self.ip = get_local_ip()
        self.status = "Active"
        self.role = "Undecided"

    def create_broadcast_message(self):
        return f"""Type: DISCOVER
        ID: {self.id}
        DeviceType: {self.device_type}
        IP: {self.ip}
        Status: {self.status}
        Role: {self.role}"""

    def object_representation(self):
        return {
            "ID": self.id,
            "DeviceType": self.device_type,
            "IP": self.ip,
            "Status": self.status,
            "Role": self.role,
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
        listen_socket.bind(("", PORT))

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

                type = message[0].split(":")[1].strip()

                if type == "DISCOVER":
                    # Parse the broadcast message into a dictionary
                    device_info = {
                        "ID": int(message[1].split(":")[1].strip()),
                        "DeviceType": message[2].split(":")[1].strip(),
                        "IP": message[3].split(":")[1].strip(),
                        "Status": message[4].split(":")[1].strip(),
                        "Role": message[5].split(":")[1].strip(),
                    }

                    with lock:
                        # Avoid duplicate devices with the same ID
                        if not any(
                            device["ID"] == device_info["ID"]
                            for device in discovered_devices
                        ):
                            discovered_devices.append(device_info)
                            print(f"Discovered device: {device_info}")

            except socket.timeout:
                continue

        print("Listening has stopped")


# Start the broadcasting and listening threads
def discover_neighbouring_devices():
    """Modified version of discover_neighbouring_robots that handles both robots and joysticks"""
    device = Device()  # Create device instance
    BROADCAST_MESSAGE = device.create_broadcast_message()

    discovered_devices = []  # Will contain both robots and joysticks
    discovered_devices.append(device.object_representation())

    lock = threading.Lock()
    stop_event = threading.Event()

    # Create and start broadcast and listen threads
    broadcast_thread = threading.Thread(
        target=broadcast, args=(BROADCAST_MESSAGE, stop_event), daemon=True
    )
    listen_thread = threading.Thread(
        target=listen, args=(discovered_devices, lock, stop_event), daemon=True
    )

    broadcast_thread.start()
    listen_thread.start()

    # Run for 20 seconds, then stop both threads
    time.sleep(10)
    stop_event.set()

    # Wait for both threads to finish
    broadcast_thread.join()
    listen_thread.join()

    return discovered_devices
