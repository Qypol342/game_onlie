import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
#while running:
#	pass

import socket


class conection():
	def __init__(self):
		
		self.serverAddressPort   = ("192.168.0.10", 20001)
		self.bufferSize= 1024
		self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	def send(self, data):
		msgFromClient = str(data)
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
	def recive(self):
		msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
		return msgFromServer

 
c = conection()
c.send({"type":"position"})

msg = "Message from Server {}".format(c.recive()[0])
print(msg)

