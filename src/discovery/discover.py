import socket
import threading
import time
import random

# Get the local IP address of the machine
def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Use any reachable IP
        return s.getsockname()[0]

LOCAL_IP_ADDRESS = get_local_ip()
BROADCAST_ADDR = '255.255.255.255'     # Define the broadcast address and port
PORT = 65009

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
def listen(discovered_robots, lock, stop_event):
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
                
                # Parse the broadcast message into a dictionary
                robot_info = {
                    'ID': int(message[0].split(":")[1].strip()),
                    'DeviceType': message[1].split(":")[1].strip(),
                    'IP': message[2].split(":")[1].strip(),
                    'Status': message[3].split(":")[1].strip(),
                    'Role': message[4].split(":")[1].strip()
                }
                
                with lock:
                    # Avoid duplicate robots with the same ID
                    if not any(robot['ID'] == robot_info['ID'] for robot in discovered_robots):
                        discovered_robots.append(robot_info)
                        print(f"Discovered robot: {robot_info}")

            except socket.timeout:
                continue

        print("Listening has stopped")

# Start the broadcasting and listening threads
def discover_neighbouring_robots():
    BROADCAST_MESSAGE = f'''
    ID: {random.randint(1, 10000)}
    DeviceType: Robot
    IP: {LOCAL_IP_ADDRESS}
    Status: Active
    Role: Undecided
    '''

    discovered_robots = []

    lock = threading.Lock()
    stop_event = threading.Event()

    # Create and start broadcast and listen threads
    broadcast_thread = threading.Thread(target=broadcast, args=(BROADCAST_MESSAGE, stop_event), daemon=True)
    listen_thread = threading.Thread(target=listen, args=(discovered_robots, lock, stop_event), daemon=True)

    broadcast_thread.start()
    listen_thread.start()

    # Run for 20 seconds, then stop both threads
    time.sleep(20)
    stop_event.set()

    # Wait for both threads to finish
    broadcast_thread.join()
    listen_thread.join()

    return discovered_robots
