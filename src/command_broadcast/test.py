import socket
import json
import movement
import time
import Amove as am
import aservo
# from utils.device_identity import get_device_identity

port = 65009

def listen_for_commands(x,y):
	# # Set up the UDP socket
	# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	# # Bind the socket to listen on all available interfaces
	# sock.bind(("", port))
	# print(f"Listening for broadcast messages on port {port}...")

	try:
			# # Receive broadcast message
			# data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
			# message = json.loads(data.decode())

			name = "Adeept"
			
			if x == "forward":
				print("y forward")
				am.forward(100)

				if name == "Adeept":
					am.forward(100)
				elif name == "Osoyoo":
					movement.forward()

			elif x == "stop":
				print("y stop")
				am.destroy()
				
				if name == "Adeept":
					am.destroy()
				elif name == "Osoyoo":
					movement.stopcar()
					
			elif x == "backward":
				print("y backward")
				am.backward(100)
				# if name == "Adeept":
				# 	am.backward(100)
				# elif name == "Osoyoo":
				# 	movement.backward()
				
			if y == "left":
				print("x left")

				# if name == "Adeept":
				# 	aservo.left()
				# elif name == "Osoyoo":
				# 	movement.steer(movement.LEFT)
			elif y == "right":
				print("x right")
				aservo.right()

				# if name == "Adeept":
				# 	aservo.right()
				# elif name == "Osoyoo":
				# 	movement.steer(movement.RIGHT)
			elif y == "center":
				print("x center")
				aservo.center()

				# if name == "Adeept":
				# 	aservo.center()
				# elif name == "Osoyoo":
				# 	movement.steer(movement.CENTER)
	except KeyboardInterrupt:
		print("The last message was: ", message)
		print("\nListener stopped by user.")
	finally:
		# sock.close()
		print("Socket closed.")


if __name__ == "__main__":
	
    message = {'x': 'forward', 'y': 'center'}

    listen_for_commands(**message)
	
    time.sleep(3)
	
    message = {'x': 'stop', 'y': 'center'}
	
    listen_for_commands("stop")