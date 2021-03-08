import pygame
from button import Button
from listmenu import ListMenu
from more_itertools import locate
import threading
import socket
import time
class GAME_BASICS():
	def __init__(self):
		self.WIDTH, self.HEIGHT = 800 , 500 
		self.w = self.WIDTH//2
		self.h = self.HEIGHT//2
		self.GAME_STATUS = 'LOBBY'
		self.gametype = 'PONGMULTI'
		self.c = conection("192.168.0.10")
		self.B_search_menu = Button(pos=(int(self.WIDTH//2)-int(self.w//2),int(self.HEIGHT//2)-int(self.h//4)),size=(self.w,self.h/2),callback=self.SET_SEARCH_MENU ,text="SELECT SERVER",text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
		self.B_back = Button(pos=(0,0),size=(150,50),callback=self.BACK ,text="Back",text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
		self.LM_list_game = ListMenu(callback=self.GAME_SELECTED,list=[],pos=(self.WIDTH//2-self.w//2,self.HEIGHT-self.h),size=(self.w,self.h),text_bias=(-10,0) ,bg_color=(75,75,75))
		self.B_quit = Button(pos=(0,0),size=(150,50),callback=self.QUIT ,text="Back",text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
		self.B_server_info = Button(pos=(0,0),size=(150,50) ,text="",text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
		self.LM_list_game_origine= []
		self.GAME_INFOS = {'ID':None, 'SERVER_IP':None}

	def reciveing(self):

		while self.GAME_STATUS == 'LOADING_SCREEN':
			
			msg = self.c.recive()

			if msg != False:
				if "{"  in msg:
					msg= eval(msg)
					if msg['GAME_TYPE'] == self.gametype:
						if (msg)['type'] == 'PING':
							print('client reviced ping')
							self.c.send({'type': 'PING_SUCCESSFUL', 'GAME_TYPE': 'PONGMULTI', 'GAME_ID': 1212})
		

	def SET_SEARCH_MENU(self):
		self.GAME_STATUS = 'SEARCH_MENU'
		threading.Thread(target=self.SEARCH_MENU).start()
	def GAME_SELECTED(self,i,l):
		print(self.LM_list_game_origine,i,l)
		if i <= len(l)-1:
			print('join')
			self.c.serverAddressPort = (self.LM_list_game_origine[i][1], 20010)
			self.c.GAME_JOIN(self.LM_list_game_origine[i][0])
			msg = False
			t =0
			while msg == False and t<30:
				msg = self.c.recive()

				t+= 1
				if msg != False:
					print(msg)
					self.GAME_INFOS['ID'] = self.LM_list_game_origine[i][0]
					self.GAME_INFOS['SERVER_IP'] = self.LM_list_game_origine[i][1]
					self.GAME_STATUS = 'LOADING_SCREEN'
					threading.Thread(target=self.reciveing).start()


	def SEARCH_MENU(self):
		print('run')
		r = (self.c.scan())
		z = []
		self.LM_list_game_origine = []
		print(r)
		for i in r:
			self.c.serverAddressPort= (eval(r[i])[0], 20010)
			w = eval(self.c.GAME_HOSTED())
			#w = [1212,122,12,1]
			for q in w:
				self.LM_list_game_origine.append([q,i])
				ww = " "*(10-len(str(q))*2) 
				z.append(f"GAMES ID: {q} {ww} IP: {i}")

		self.LM_list_game.list=z

	def SET_LOADING_SCREEN(self):
		self.GAME_STATUS = 'LOADING_SCREEN'

	def BACK(self):
		if self.GAME_STATUS =='SEARCH_MENU':
			self.GAME_STATUS = 'LOBBY'
	def QUIT(self):
		self.c.GAME_QUIT(self.GAME_INFOS['ID'])
		self.GAME_STATUS = 'LOBBY'



	def update_screen(self, WIN,ev):
		B= []
		WIN.fill(DARCK_GREY)
		if self.GAME_STATUS == 'LOBBY':
			B = [self.B_search_menu]
		elif self.GAME_STATUS == 'SEARCH_MENU':
			B = [self.B_back, self.LM_list_game]
		elif self.GAME_STATUS == 'GAME':
			B = [self.B_quit]
		elif self.GAME_STATUS == 'LOADING_SCREEN':
			B = [self.B_quit]

		for i in B:
			i.Check_pressed(ev)
			WIN =i.Draw_Button(WIN)



		return WIN




class conection():
	def __init__(self, c = None ):
		
		self.serverAddressPort   = (c, 20010)
		self.bufferSize= 1024
		self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPClientSocket.settimeout(1)
		self.gametype = 'PONGMULTI'
	def SetserverAddressPort(self, ip):
		self.serverAddressPort[0] = ip

	def sub_scan(self, s,e, bts):

		self.UDPClientSocket.settimeout(0.0005)#0.0005
		for i in range(s,e):
			#print('client',self.local+str(i))
			##bts = eval(bts.decode("utf-8"))
			#bts['to'] = self.local+str(i)
			#bts = str(bts)
			#print('client',bts)
			#bts = str.encode(bts)

			self.UDPClientSocket.sendto(bts, (self.local+str(i), 20010))
			msgFromServer =None
			try:
				msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
				msg = (msgFromServer[0]).decode("utf-8") 
				msg = eval(msg)
				print('client',msg)
				if msg['type'] == 'SERVER_SEARCH_REPOND':
					self.server_op[eval(msg['DATA'])[0]] = msg['DATA']# important l'adress ip choisi et celle contenue dans le msg
					print('client',(msgFromServer[1]) )
				
			except Exception as e:
				#print(e,self.local+str(i) )
				pass

	def scan(self):
		self.hostname = socket.gethostname()
		self.my_ip = socket.gethostbyname(self.hostname)


		################
		self.my_ip = "192.168.0.10"
		#########


		self.local = self.my_ip[:list(locate(self.my_ip, lambda a: a == '.'))[-1]+1]
		msgFromClient = str({"type":"SERVER_SEARCH",'GAME_TYPE':self.gametype})
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.settimeout(0.01)#0.0005
		self.server_op = {}
		
		sub =1

		
		for i in range(sub):
			x = threading.Thread(target=self.sub_scan, args=(256//sub*i,(256//sub*i+256//sub)-1, bytesToSend))
			x.start()
		
		
			
		x.join()
		
		print('client',self.server_op)
		return self.server_op

	def GAME_HOSTED(self):
		print('GAME_HOSTED')
		self.send({'type':'GAME_HOSTED','GAME_TYPE':self.gametype})
		msg  =False
		t =0

		while msg == False and t<30:
			#print(t)
			msg = self.recive()
			t+= 1 
		#print('client',msg)
		if msg == False:
			msg = '[]'
		return msg


	def GAME_JOIN(self, id=1212):
		self.send({'type':'GAME_JOIN','GAME_TYPE':self.gametype,'GAME_ID':id})
	def GAME_QUIT(self, id=1212):
		self.send({'type':'GAME_QUIT','GAME_TYPE':self.gametype,'GAME_ID':id})

	def send(self, data):
		msgFromClient = str(data)
		bytesToSend= str.encode(msgFromClient)
		self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
		
	def recive(self, t= 0.0005):
		#print(self.UDPClientSocket.gettimeout())
		self.UDPClientSocket.settimeout(t)
		try:
			msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
			msg = (msgFromServer[0]).decode("utf-8") 
		except:
			msg= False
		return msg




g = GAME_BASICS()
c = g.c


WIDTH, HEIGHT = 800 , 500 
w = WIDTH//4
h = HEIGHT//4
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))

gametype = 'PONGMULTI'






def test_local():
	print('client','send')
	c.send(str(time.time()))




B_game_join = Button(pos=(0,0),size=(w,h),callback=c.GAME_JOIN ,text='game_join',text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
B_game_quit = Button(pos=(w,0),size=(w,h),callback=c.GAME_QUIT ,text='game_quit',text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
B_in_game_data = Button(pos=(w*2,0),size=(w,h) ,text='in_game_data',text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
B_server_search = Button(pos=(w*3,0),size=(w,h),callback=c.scan ,text='server_search',text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
B_game_search = Button(pos=(w*3,h),size=(w,h),callback=c.GAME_HOSTED ,text='game_search',text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))
B_test = Button(pos=(w*2,h),size=(w,h),callback=test_local ,text='test',text_bias = (40,15),bg_color=(50,50,50),bg_color_hover=(100,100,100))

B = [B_game_join,B_game_quit,B_in_game_data,B_game_search,B_test,B_server_search]#

pygame.display.set_caption('client connection')
#####


WHITE = (255,255,255)
BLACK = (0,0,0)
DARCK_GREY  = (25 , 25, 25)
GREY  = (50 , 50, 50)
FPS = 15
c.SetserverAddressPort = '192.168.0.10'
def main():
	
	global WIN
	clock = pygame.time.Clock()
	run = True

	while run:
		clock.tick(FPS)
		ev  = pygame.event.get()
		PYGAME_EVENT = ev
		for event in ev:
			if event.type == pygame.QUIT:
				run = False
				g.GAME_STATUS = 'CLOSE'
				
		#threading.Thread(target=c.recive).start()


		keys_pressed = pygame.key.get_pressed()

		WIN = g.update_screen(WIN,ev)

		



		pygame.display.update()
		
		

	pygame.quit()

if __name__ == "__main__":
	main()
'''
if event.type == pygame.MOUSEBUTTONDOWN:
				print('client',"pressed")

				'''
