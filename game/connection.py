import socket
from more_itertools import locate
import threading

class conection():
	def __init__(self):
		
		self.serverAddressPort   = ("192.168.0.10", 20001)
		self.bufferSize= 1024
		self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPClientSocket.settimeout(1)
	def sub_scan(self, s,e, bts):

	
		for i in range(s,e):
			#print(self.local+str(i))
			self.UDPClientSocket.sendto(bts, (self.local+str(i), 20001))
			msgFromServer =None
			try:
				msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
				msg = (msgFromServer[0]).decode("utf-8") 
				if msg == "server_found":
					self.server_op.append(self.local+str(i))
				
			except:
				pass

	def scan(self):
		self.hostname = socket.gethostname()
		self.my_ip = socket.gethostbyname(self.hostname)


		################
		self.my_ip = "192.168.0.10"
		#########


		self.local = self.my_ip[:list(locate(self.my_ip, lambda a: a == '.'))[-1]+1]
		msgFromClient = str({"type":"server_recherche"})
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.settimeout(0.05)
		self.server_op = []
		sub = 3
		for i in range(sub):
			x = threading.Thread(target=self.sub_scan, args=(256//sub*i,256//sub*i+256//sub, bytesToSend))
			x.start()
		
		
			
		x.join()
		print(self.server_op)

	def send(self, data):
		msgFromClient = str(data)
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
		
	def recive(self):
		try:
			msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
			msg = (msgFromServer[0]).decode("utf-8") 
		except:
			msg= False
		return msg