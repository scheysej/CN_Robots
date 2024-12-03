"""Author: Andre Price
Date: 11-11-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import threading
import random
import socket
import time
from utils.device_identity import get_device_identity
from utils.device_identity import write_device_identity

BROADCAST_ADDR = "255.255.255.255"  # Define the broadcast address and port
PORT = 65009


def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Use any reachable IP
        return s.getsockname()[0]


class Robot:
    def __init__(self, robot_id, ip, device_type, brand, devices):
        self.id = robot_id
        self.ip = ip
        self.device_type = device_type
        self.robot_brand = brand
        self.election_id = random.randint(1, 100)
        self.is_leader = False
        self.leader_id = ""
        self.received_election_ids = []
        self.all_devices = devices

    def broadcast(self, stop_event):
        # Simulate broadcasting the robot's ElectionID to all other robots.
        broadcast_message = f"""
            MessageType: ELECTION
            RobotID: {self.id}
            ElectionID: {self.election_id}
        """

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as broadcast_socket:
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            print(f"Broadcasting message: {broadcast_message}")

            while not stop_event.is_set():
                broadcast_socket.sendto(
                    broadcast_message.encode(), (BROADCAST_ADDR, PORT)
                )
                time.sleep(1)

            print("Broadcasting my election ID has stopped")

            time.sleep(1)

    def listen(self, stop_event):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listen_socket:

            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listen_socket.bind(("", PORT))

            print(f"Listening for the Election ID of other robots")

            while not stop_event.is_set():
                try:
                    listen_socket.settimeout(1)
                    data, addr = listen_socket.recvfrom(1024)
                    sender_ip = addr[0]

                    # Ignore messages from itself
                    if sender_ip == get_local_ip():
                        continue

                    message = data.decode().strip().splitlines()

                    if message[0].split(":")[1].strip() == "ELECTION":
                        robot_id = message[1].split(":")[1].strip()
                        election_id = message[2].split(":")[1].strip()

                        # for received_robot in self.election_id:
                        if not any(
                            e["election_id"] == election_id
                            for e in self.received_election_ids
                        ):
                            self.received_election_ids.append(
                                {
                                    "robot_id": str(robot_id),
                                    "election_id": str(election_id),
                                }
                            )
                            print(
                                f"I received ElectionID {election_id} from Robot {robot_id}"
                            )

                    # Function above makes it so that it checks to make sure that the election id isnt already in the received election ids
                except socket.timeout:
                    continue

            # Adding myself to received election ids
            self.received_election_ids.append(
                {"robot_id": self.id, "election_id": self.election_id}
            )
            print("Listening has stopped")


    def decide_leader(self):
        # Decide the leader based on the highest ElectionID received, including its own.
        election_ids = [int(id["election_id"]) for id in self.received_election_ids]
        
        # Check if there are any duplicate election IDs
        if len(set(election_ids)) < len(election_ids):
            print("Duplicate election IDs detected - need to redo election")
            return "REDO"  # Special signal to indicate election needs to be redone
        
        max_election_id = None
        leader_id = None
        for id in self.received_election_ids:
            election_id = int(id["election_id"])
            robot_id = id["robot_id"]

            if max_election_id is None or election_id > max_election_id:
                max_election_id = election_id
                leader_id = robot_id

        print(
            f"The max election id is "
            + str(max_election_id)
            + " from "
            + str(leader_id)
        )
        self.type = "Leader"
        return leader_id

    def update_device_identity(self):
        # Receive the leader announcement and recognize the leader.
        print(f"Robot {self.id} recognizes Robot {self.leader_id} as the leader.")

        identity = None

        if str(self.id) == str(self.leader_id):
            identity = {
                'device_id': self.id,
                'device_type': self.device_type,
                'robot_brand': self.robot_brand,
                'role': "leader",
            }
        elif self.id == self.leader_id:
            identity = {
                'device_id': self.id,
                'device_type': self.device_type,
                'robot_brand': self.robot_brand,
                'role': "follower",
            }

        write_device_identity(identity)


def announce_leader_to_keyboard(keyboard, leader_id):
    if not keyboard:
        print("No keyboard device found")
        return
        
    port = 65011
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((keyboard["IP"], port))
                sock.sendall(str(leader_id).encode("utf-8"))
                print(f"Successfully announced leader {leader_id} to keyboard at {keyboard['IP']}")
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    print(f"Failed to announce leader to keyboard after {max_retries} attempts")
    return False


def simulate_leader_election(devices):
    # Create robots based on discovered_robots but generate ElectionID here
    robot = None

    # Robot creates its own election id
    for device in devices:
        # Loop through all the devices in the fleet, if the device is a robot and has the same ip address (essentially)
        # finds the raspberry pi in the list of all the devices
        if (device["DeviceType"] != "keyboard") and (device["IP"] == get_local_ip()):
            robot = Robot(
                device["DeviceID"],
                device["IP"],
                device["DeviceType"],
                device["RobotBrand"],
                devices
            )  

    while True:  # Keep trying until we get a valid election
        stop_event = threading.Event()

        print(
            f"I am starting broadcast [{robot.id}] with my ElectionID of {robot.election_id}"
        )

        electionid_broadcast_thread = threading.Thread(
            target=robot.broadcast, args=(stop_event,)
        )
        electionid_listen_thread = threading.Thread(target=robot.listen, args=(stop_event,))

        electionid_broadcast_thread.start()
        electionid_listen_thread.start()

        time.sleep(10)
        stop_event.set()

        electionid_broadcast_thread.join()
        electionid_listen_thread.join()

        potential_leader_id = robot.decide_leader()
        
        if potential_leader_id == "REDO":
            print("Restarting election due to duplicate IDs...")
            robot.election_id = random.randint(1, 100)  # Generate new election ID
            robot.received_election_ids = []  # Clear received IDs
            continue
            
        robot.leader_id = potential_leader_id

        keyboard = None
        for device in devices:
            if device["DeviceType"] == "keyboard":
                keyboard = device

        robot.update_device_identity()
        announce_leader_to_keyboard(keyboard, robot.leader_id)
        return robot.leader_id


def keyboard_listen_election(devices):
    """Listen to election process from all robots and verify consensus."""
    # Create TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 65011))  # Using port 65011 as defined in announce_leader_to_keyboard
    server_socket.listen(5)
    
    robot_votes = {}  # Track each robot's leader vote
    robot_count = sum(1 for device in devices if device["DeviceType"] != "keyboard")
    
    print("Keyboard listening for leader election results...")
    
    try:
        while len(robot_votes) < robot_count:
            client_socket, addr = server_socket.accept()
            data = client_socket.recv(1024).decode()
            
            # Parse the leader ID from the robot
            robot_votes[addr[0]] = data
            print(f"Received vote from {addr[0]}: Leader ID = {data}")
            
            client_socket.close()
            
        # Verify consensus
        unique_votes = set(robot_votes.values())
        if len(unique_votes) == 1:
            elected_leader = next(iter(unique_votes))
            print(f"Consensus reached! Leader ID: {elected_leader}")
            return elected_leader
        else:
            print("Warning: No consensus reached among robots!")
            return None
            
    finally:
        server_socket.close()
