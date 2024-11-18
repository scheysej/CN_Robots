import socket
import json
import movement
port = 65010

# Set up the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to listen on all available interfaces
sock.bind(("", port))
print(f"Listening for broadcast messages on port {port}...")

try:
	while True:
		# Receive broadcast message
		data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
		message = json.loads(data.decode())
		
		if message['movement_y'] == "forward":
			movement.forward()
		elif message['movement_y'] == "stop":
			movement.stopcar()
		elif message['movement_y'] == "backward":
			movement.backward()
			
		if message['movement_x'] == "left":
			movement.steer(movement.LEFT)
		elif message['movement_x'] == "right":
			movement.steer(movement.RIGHT)
		elif message['movement_x'] == "center":
			movement.steer(movement.CENTER)
except KeyboardInterrupt:
	print("\nListener stopped by user.")
finally:
	sock.close()
	print("Socket closed.")
