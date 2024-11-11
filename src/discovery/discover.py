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

# Function to broadcast a message
def broadcast(broadcast_message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as broadcast_socket:
        # Since by default, sockets cant send broadcast messages, this will allow it
        # to brodcast on 255.255.255.255
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print(f"Broadcasting message: {broadcast_message}")
        # Broadcast message for 20 seconds
        start_time = time.time()
        while time.time() - start_time < 20:
            broadcast_socket.sendto(broadcast_message.encode(), (BROADCAST_ADDR, PORT))
            time.sleep(1)  # Broadcast every 1 second
        
        print("Broadcasting has completed")

# Function to listen for broadcast messages
def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listen_socket:
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(('', PORT))

        print(f"Listening on port {PORT} for broadcasts...")
        
        start_time = time.time()
        while True:
            data, addr = listen_socket.recvfrom(1024)
            sender_ip = addr[0]
            
            # Ignore messages sent from this device
            if sender_ip == LOCAL_IP_ADDRESS:
                continue

            message = data.decode()
            
            # Thread-safe check and update of received messages
            with lock:
                # Check if we already have this message from this IP
                if sender_ip in received_messages and received_messages[sender_ip] == message:
                    continue  # Skip duplicate message

                # Store or update the message from this IP
                received_messages[sender_ip] = message
                print(f"Received broadcast from {addr}: {message}")
                        
        print("Listening has completed")

# Start the broadcasting and listening threads
if __name__ == "__main__":
    BROADCAST_ADDR = '255.255.255.255'     # Define the broadcast address and port
    PORT = 6969


    BROADCAST_MESSAGE = f'''
    ID: {random.randint(1, 10000)}
    DeviceType: Robot
    IP: {LOCAL_IP_ADDRESS}
    Status: Active
    Role: Undecided
    '''

    # Dictionary to store messages received from each IP address
    received_messages = {}

    # Lock for thread-safe access to received_messages
    lock = threading.Lock()

    broadcast_thread = threading.Thread(target=broadcast, args=(BROADCAST_MESSAGE,), daemon=True)
    listen_thread = threading.Thread(target=listen, daemon=True)

    broadcast_thread.start()
    listen_thread.start()

    broadcast_thread.join()
    listen_thread.join()


