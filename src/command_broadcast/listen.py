import socket
import json
import movement
import time
import Amove as am
from utils.device_identity import get_device_identity

port = 65009

def listen_for_commands():
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

			device_identity = get_device_identity()
			
			if message['movement_y'] == "forward":
				print("y forward")
				if device_identity["name"] == "Adeept":
					am.forward(100)
				elif device_identity["name"] == "Osoyoo":
					movement.forward()

			elif message['movement_y'] == "stop":
				print("y stop")
				if device_identity["name"] == "Adeept":
					am.destroy()
				elif device_identity["name"] == "Osoyoo":
					movement.stopcar()
					
			elif message['movement_y'] == "backward":
				print("y backward")
				if device_identity["name"] == "Adeept":
					am.backward(100)
				elif device_identity["name"] == "Osoyoo":
					movement.backward()
				
			if message['movement_x'] == "left":
				print("x left")
				movement.steer(movement.LEFT)
			elif message['movement_x'] == "right":
				print("x right")
				movement.steer(movement.RIGHT)
			elif message['movement_x'] == "center":
				print("x center")
				movement.steer(movement.CENTER)
	except KeyboardInterrupt:
		print("\nListener stopped by user.")
	finally:
		sock.close()
		print("Socket closed.")
