"""
Author: Andre Price
Date: 11-11-24
Course: ELEE 4680
Instructor: Dr. Utayba Mohammad
"""

import threading
import random
import time
from utils.device_identity import get_device_identity

class Robot:
    def __init__(self, robot_id, status, ip, type):
        self.id = robot_id
        self.status = status
        self.ip = ip
        self.device_type = type
        # self.id, _ = get_device_identity()
        self.election_id = random.randint(1, 100)
        self.is_leader = False
        self.received_ids = {}

    def broadcast(self, stop_event, robots):
        #Simulate broadcasting the robot's ElectionID to all other robots.
        broadcast_message = {
            "RobotID": self.id,
            "ElectionID": self.election_id
        }
        while not stop_event.is_set():
            print(f"Robot {self.id} broadcasting ElectionID: {self.election_id}")
            for robot in robots:
                if robot.id != self.id:
                    robot.receive_broadcast(broadcast_message)
            time.sleep(1)  # Broadcast every second for demonstration

    def receive_broadcast(self, message):
        #Receive ElectionID from another robot and store it.
        self.received_ids[message["RobotID"]] = message["ElectionID"]

    def decide_leader(self):
        # Decide the leader based on the highest ElectionID received, including its own.
        all_ids = {self.id: self.election_id, **self.received_ids}
        leader_id = max(all_ids, key=all_ids.get)
        
        if leader_id == self.id:
            self.is_leader = True
        return leader_id

    def announce_leader(self, robots):
        #Announce to all robots that this robot is the leader.
        for robot in robots:
            if robot.id != self.id:
                robot.receive_leader_announcement(self.id)

    def receive_leader_announcement(self, leader_id):
        #Receive the leader announcement and recognize the leader.
        print(f"Robot {self.id} recognizes Robot {leader_id} as the leader.")

    def broadcast_leader(self, stop_event, robots):
        #Broadcast that this robot is the leader to all others until acknowledged.
        leader_announcement = {
            "LeaderID": self.id
        }

        while not stop_event.is_set():
            print(f"Leader Robot {self.id} broadcasting that it is the leader.")
            for robot in robots:
                if robot.id != self.id:
                    robot.receive_leader_announcement(self.id)
            time.sleep(1)  # Leader broadcasts every second

def notify_joystick_of_leader(leader_robot):
    """Notify joystick of the elected leader."""
    return {
        'LEADER_IP': leader_robot.ip,
        'LEADER_ID': leader_robot.id
    }
    
    # Write leader information to a file that joystick.py can read
   # with open('leader_info.txt', 'w') as f:
     #   f.write(f"{leader_info['LEADER_IP']}\n{leader_info['LEADER_ID']}")

def simulate_leader_election(devices):
    # Create robots based on discovered_robots but generate ElectionID here
    # robots = [Robot() for _ in enumerate(devices)]
    robots = []
    for robot in devices:
        if robot['DeviceType'] == 'Robot':
            robots.append(Robot(robot['ID'], robot['Status'], robot['IP'], robot['DeviceType']))
    
    stop_event = threading.Event()  # Event to signal the end of broadcasting
    threads = []

    # Initialize each robot and start broadcasting on a separate thread
    for robot in robots:
        thread = threading.Thread(target=robot.broadcast, args=(stop_event,robots))
        threads.append(thread)
        thread.start()
    
    # Allow broadcasting for a brief period, then stop to determine leader
    time.sleep(5)
    stop_event.set()  # Stop all broadcasting

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Consensus Protocol: Decide and announce leader
    for robot in robots:
        leader_id = robot.decide_leader()
        print(f"Robot {robot.id} thinks Robot {leader_id} should be the leader.")

    # Leader Announcement
    for robot in robots:
        if robot.is_leader:
            print(f"Robot {robot.robot_id} is the leader and will announce.")
            leader_stop_event = threading.Event()
            leader_thread = threading.Thread(target=robot.broadcast_leader, args=(leader_stop_event,robots))
            leader_thread.start()
            
            # Let the leader announce for a short time, then stop
            time.sleep(3)
            leader_stop_event.set()
            leader_thread.join()
            
            print(f"Joystick notified: Robot {robot.robot_id} is the leader.")
            notify_joystick_of_leader(robot)
            break
