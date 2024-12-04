import socket
import time


def broadcast_message(message, hostIP):

    # broadcast_ip = '255.255.255.255'
    port = 65010

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((hostIP, port))

    try:
        client_socket, address = sock.accept()

        print(f"Connection received from {address}")

        client_socket.send(message)
    finally:
        sock.close()


    # try:
    #     sock.sendto(message, (broadcast_ip, port))
    #     print(f"Broadcast message sent: {message}")
    # finally:
    #     sock.close()
