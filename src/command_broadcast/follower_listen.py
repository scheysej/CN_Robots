import socket
import json
import time
from utils.device_identity import get_device_identity

port = 65010

def listen_for_commands():
	robot_identity = get_device_identity()

	name = robot_identity["robot_brand"]
	
	if(name == "adeept"):
		import Amove as am
		import aservo
	elif (name == "osoyoo"):
		import movement
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

			name = name
			if message['movement_y'] == "forward":
				print(message['movement_y'])

				#am.Motor(1,1,100)	

				# am.forward(100,1)
				# time.sleep(3)

				if name == "adeept":
					am.forward(100, 1)
				elif name == "osoyoo":
					movement.forward()

			elif message['movement_y'] == "stop":
				print(message['movement_y'])
				# am.motorStop()

				if name == "adeept":
					am.motorStop()
				elif name == "osoyoo":
					movement.stopcar()
					
			elif message['movement_y'] == "backward":
				print(message['movement_y'])
				# am.Motor(1,-1,100)
				if name == "adeept":
					am.backward(100)
				elif name == "osoyoo":
					movement.backward()
				
			if message['movement_x'] == "left":
				print(message['movement_x'])
				# aservo.left()

				if name == "adeept":
					aservo.left()
				elif name == "osoyoo":
					movement.steer(movement.LEFT)
			elif message['movement_x'] == "right":
				print(message['movement_x'])
				# aservo.right()

				if name == "adeept":
					aservo.right()
				elif name == "osoyoo":
					movement.steer(movement.RIGHT)
			elif message['movement_x'] == "center":
				print(message['movement_x'])
				# aservo.center()

				if name == "adeept":
					aservo.center()
				elif name == "osoyoo":
					movement.steer(movement.CENTER)
	except KeyboardInterrupt:
		am.destroy()
		print("The last message was: ", message)
		print("\nListener stopped by user.")
	finally:
		sock.close()
		print("Socket closed.")
