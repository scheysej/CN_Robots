import socket
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
		print(f"Received message: {data.decode()} from {addr}")
		if data.decode() == "forward":
			movement.forward()
		elif data.decode() == "stop":
			movement.stopcar()
		elif data.decode() == "backward":
			movement.backward()
		elif data.decode() == "left":
			movement.steer(movement.LEFT)
		elif data.decode() == "right":
			movement.steer(movement.RIGHT)
		elif data.decode() == "center":
			movement.steer(movement.CENTER)
except KeyboardInterrupt:
	print("\nListener stopped by user.")
finally:
	sock.close()
	print("Socket closed.")
