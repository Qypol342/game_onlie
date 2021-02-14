import socket
from more_itertools import locate

class conection():
	def __init__(self):
		
		self.serverAddressPort   = ("192.168.0.10", 20001)
		self.bufferSize= 1024
		self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	def scan(self):
		self.hostname = socket.gethostname()
		self.my_ip = socket.gethostbyname(self.hostname)
		self.local = self.my_ip[:list(locate(self.my_ip, lambda a: a == '.'))[-1]+1]
		msgFromClient = str({"type":"server_recherche"})
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.settimeout(1)
		self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
		
		for i in range(256):
			print(self.local+str(i))
			if self.local+str(i) == "192.168.0.10":
				print('good')
			self.UDPClientSocket.sendto(bytesToSend, (self.local+str(i), 20001))
			msgFromServer =None
			try:
				msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
			except:
				pass
			print(msgFromServer)
		

	def send(self, data):
		msgFromClient = str(data)
		bytesToSend= str.encode(msgFromClient)
		
	def recive(self):
		msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
		return msgFromServer







c = conection()
c.scan()