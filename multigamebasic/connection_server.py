import socket
from more_itertools import locate
import threading
import random
import time

class serv():
	def __init__(self,  ):
		self.hostname = socket.gethostname()
		self.my_ip = socket.gethostbyname_ex(self.hostname)[-1][-1]
		print("server",self.my_ip)

		self.serverAddressPort   = (self.my_ip, 20010) ##################################################
		#self.serverAddressPort   = ("192.168.0.13", 20010)
		print("server",self.serverAddressPort)
		self.bufferSize= 1024
		self.server_id = random.randint(10000000,99999999)
		print("server",'server_id',self.server_id)
		self.gametype = 'PONGMULTI'
		self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		#self.UDPServerSocket.settimeout(1)
		self.GAME_RUN = False
		self.active_reciveing = True
		self.GAMES = {1212:{'PLAYER':{},'GAME_STATUS':'WAITING'}}
		

		self.UDPServerSocket.bind(self.serverAddressPort)

		

	def send(self, data):
		msgFromClient = str(data)
		bytesToSend= str.encode(msgFromClient)
		self.UDPServerSocket.sendto(bytesToSend, self.serverAddressPort)


	def PING_PLAYER(self):
		while self.active_reciveing :
			time.sleep(1)
			for i in self.GAMES:
				if self.GAMES[i]['GAME_STATUS'] == 'WAITING':
					to_del = []
					for z in self.GAMES[i]['PLAYER']:
						d = (time.time()-self.GAMES[i]['PLAYER'][z]['PING'])
						if d>1.5:
							to_del.append( z)
							print(d)
						else:

							data = {'type':'PING','GAME_TYPE': self.gametype,'GAME_ID':i}
							msgFromClient = str(data)
							bytesToSend= str.encode(msgFromClient)
							self.UDPServerSocket.sendto(bytesToSend, self.GAMES[i]['PLAYER'][z]['INFO'])
					for z in to_del:
						print('del',z)
						del self.GAMES[i]['PLAYER'][z]



						
						
		pass

		
	def reciveing(self):
		threading.Thread(target=self.PING_PLAYER).start()
		print("reciveing")
		while self.active_reciveing:
			try:
				msgFromServer = self.UDPServerSocket.recvfrom(self.bufferSize)
				msg = (msgFromServer[0]).decode("utf-8")
			except:
				#connection perdu
				msg = ""
			print("server",msg,msgFromServer[1])
			#print("server",type(msg))
			if "{"  in msg:
				msg= eval(msg)
				if msg['GAME_TYPE'] == self.gametype:
					if (msg)['type'] == 'SERVER_SEARCH':

						bytesToSend = str.encode(str({'type':'SERVER_SEARCH_REPOND', 'DATA':str(self.serverAddressPort)}))
						self.UDPServerSocket.sendto(bytesToSend, msgFromServer[1])
					elif (msg)['type'] == 'GAME_HOSTED':
						r = []
						for i  in self.GAMES:
							r.append(i)
						bytesToSend = str.encode(str(r))
						self.UDPServerSocket.sendto(bytesToSend, msgFromServer[1])
					elif (msg)['type'] == 'GAME_JOIN':
						ms = (msg)

						if msgFromServer[1][0] not in self.GAMES[ms['GAME_ID']]['PLAYER']:
							self.GAMES[ms['GAME_ID']]['PLAYER'][msgFromServer[1][0]] = {'PING':time.time(), 'INFO':msgFromServer[1]}

							r = {'type': 'GAME_JOIN_SUCCESSFUL', 'GAME_TYPE': 'PONGMULTI','GAME_ID':ms['GAME_ID']}
							bytesToSend = str.encode(str(r))
							self.UDPServerSocket.sendto(bytesToSend, msgFromServer[1])
						print(self.GAMES)
					elif (msg)['type'] == 'GAME_QUIT':
						ms = (msg)

						if msgFromServer[1][0]  in self.GAMES[ms['GAME_ID']]['PLAYER']:	
							del self.GAMES[ms['GAME_ID']]['PLAYER'][msgFromServer[1][0]]
						print(self.GAMES)
					elif (msg)['type'] == 'PING_SUCCESSFUL':
						ms = (msg)

						if msgFromServer[1][0]  in self.GAMES[ms['GAME_ID']]['PLAYER']:	
							self.GAMES[ms['GAME_ID']]['PLAYER'][msgFromServer[1][0]]['PING'] = time.time()
						

                                        
                                        


			else:
				print("server",msg)
			
		
	def runing(self):
		threading.Thread(target=self.reciveing).start()


	def game(self):
		while self.GAME_RUN:
			pass


c= serv()
c.runing()



