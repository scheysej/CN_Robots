import socket

broadcast_ip = '255.255.255.255'
port = 65010

message = "Hello, this is a broadcast message from Raspberry Pi!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

try:
	sock.sendto(message.encode(), (broadcast_ip, port))
	print(f"Broadcast message sent: {message}")
finally:
	sock.close()

