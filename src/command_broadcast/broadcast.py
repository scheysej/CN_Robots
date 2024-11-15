import socket
import time

broadcast_ip = '255.255.255.255'
port = 65010

message = "forward"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

try:
	sock.sendto(message.encode(), (broadcast_ip, port))
	print(f"Broadcast message sent: {message}")
	time.sleep(2)
	message = "left"
	sock.sendto(message.encode(), (broadcast_ip, port))
	time.sleep(2)
	message = "center"
	sock.sendto(message.encode(), (broadcast_ip, port))
	time.sleep(2)
	message = "right"
	sock.sendto(message.encode(), (broadcast_ip, port))
	time.sleep(2)
	message = "stop"
	sock.sendto(message.encode(), (broadcast_ip, port))
finally:
	sock.close()

