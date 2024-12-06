
import socket
import threading
import time
from utils.device_identity import get_device_identity


BROADCAST_ADDR = '255.255.255.255' 
PORT = 65999

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  
        return s.getsockname()[0]

LOCAL_IP_ADDRESS = get_local_ip()

def listen_for_response(stop_event):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listen_socket:
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(('', PORT))

        print(f"Listening for a response on the same port...")

        while not stop_event.is_set():
            try:
                listen_socket.settimeout(1) 
                data, addr = listen_socket.recvfrom(1024)
                sender_ip = addr[0]
                
                if sender_ip == LOCAL_IP_ADDRESS:
                    continue  

                message = data.decode().strip().splitlines()
                
                message_type = message[0].split(":")[1].strip()
                
                if message_type == 'REQUEST_ACCEPTED':
                        stop_event.set()

            except socket.timeout:
                continue

        print("Listening has stopped")

def request_join(robot_identity, stop_event):
    stop_event = threading.Event()
    
    request_message = f"""
        MessageType: REQUEST_TO_JOIN
        DeviceID: {robot_identity['device_id']}
        DeviceType: {robot_identity['device_type']}
        IP: {LOCAL_IP_ADDRESS}
        RobotBrand: {robot_identity['robot_brand']}
    """

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as requesting_socket:
        requesting_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print(f"Requesting to Join...")
        
        while not stop_event.is_set():
            requesting_socket.sendto(request_message.encode(), (BROADCAST_ADDR, PORT))
            time.sleep(1)

        print("Asking to join has stopped")

    time.sleep(10)
    stop_event.set()


def main(): 
    robot_identity = get_device_identity()
    print("Device identity retrieved")
    
    
    stop_event = threading.Event()

    # Create and start broadcast and listen threads
    broadcast_thread = threading.Thread(target=request_join, args=(robot_identity, stop_event), daemon=True)
    listen_thread = threading.Thread(target=listen_for_response, args=(stop_event), daemon=True)

    broadcast_thread.start()
    listen_thread.start()

    # Run for 20 seconds, then stop both threads
    time.sleep(10)
    
    if(not stop_event.is_set()):
            stop_event.set()



if __name__ == "__main__":
    main()