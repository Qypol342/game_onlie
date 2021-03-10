import socket
from more_itertools import locate
import threading

class conection():
	def __init__(self, c = "192.168.0.10" ):
		
		self.serverAddressPort   = (c, 20001)
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
				msg = eval(msg)
				#print(msg)
				if msg['type'] == 'SERVER_SEARCH_REPOND':
					self.server_op[self.local+str(i)] = msg['DATA']
				
			except Exception as e:
				pass

	def scan(self):
		self.hostname = socket.gethostname()
		self.my_ip = socket.gethostbyname_ex(self.hostname)[-1][-1]





		self.local = self.my_ip[:list(locate(self.my_ip, lambda a: a == '.'))[-1]+1]
		msgFromClient = str({"type":"SERVER_SEARCH"})
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.settimeout(0.0005)
		self.server_op = {}
		
		sub =1

		
		for i in range(sub):
			x = threading.Thread(target=self.sub_scan, args=(256//sub*i,(256//sub*i+256//sub)-1, bytesToSend))
			x.start()
		
		
			
		x.join()
		
		print(self.server_op)
		return self.server_op

	def scan_test(self,sub,t):
		self.hostname = socket.gethostname()
		self.my_ip = socket.gethostbyname(self.hostname)


		################
		self.my_ip = "192.168.0.10"
		#########


		self.local = self.my_ip[:list(locate(self.my_ip, lambda a: a == '.'))[-1]+1]
		msgFromClient = str({"type":"SERVER_SEARCH"})
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.settimeout(t)
		self.server_op = {}
		

		
		for i in range(sub):
			x = threading.Thread(target=self.sub_scan, args=(256//sub*i,(256//sub*i+256//sub)-1, bytesToSend))
			x.start()
		
		
			
		x.join()
		
		print(self.server_op)
		return self.server_op
		

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

c= conection()
import time


def test(nb,dived_by,timeout):
	q = 0
	qq = 0
	st = time.time()
	for i in range(nb):
		print(i)
		r = c.scan_test(dived_by,timeout)
		#print(type(r))
		if r != {}:
			qq+=1
		if r == {'192.168.0.10': '0'}:
			print('true')
			q +=1
		r= {}
	print(qq/nb,q/nb, (time.time()-st)/nb,(time.time()-st))



w = time.time()

#test(10,3,1)#0.8 85.87607517242432
#test(10,1,0.2)#0.0 51.417667627334595
#test(10,2,0.5)#0.0 63.36056983470917
#test(1,1,0.5)
#test(1,1,0.08)#1.0 1.0 20.449771881103516 20.449771881103516
#test(1,3,0.08)#1.0 0.0 6.778711557388306 6.778711557388306
#test(1,3,0.07)#1.0 0.0 5.858825445175171 5.858825445175171
#test(1,3,0.06)#1.0 1.0 5.093029022216797 5.093029022216797
#test(3,3,0.06) 1.0 0.6666666666666666 5.092622677485148 15.277868032455444
#test(3,1,0.06) 1.0 1.0 15.37366239229838 46.12098717689514


#test(3,1,0.0009)
#print(time.time()-w)


#0.25760451952616376