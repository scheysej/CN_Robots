import socket
import time


def broadcast_message(message):

    broadcast_ip = '255.255.255.255'
    port = 65010

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        sock.sendto(message, (broadcast_ip, port))
        print(f"Broadcast message sent: {message}")
    finally:
        sock.close()

