import pygame
import socket
from connection import conection
from cirl import Cirl
from math import sqrt, tan
import threading
import time
pygame.font.init()

WIDTH, HEIGHT = 800 , 500 
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Pong')

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY  = (50 , 50, 50)

TITLE_FONT = pygame.font.SysFont('impact',50)
BUTTON_FONT = pygame.font.SysFont('impact',40)
SERVER_LIST_FONT = pygame.font.SysFont('impact',20)


FPS = 60
GAME_ID = 1212
class Menu(object):
	def __init__(self ):
		self.STATUS = 'Menu'
		self.c = conection()
		self.SERVER_SCANING = None
		self.SERVER_LIST = []
	def DrawMenu(self):
		if self.STATUS =='Menu':
			WIN.blit(TITLE_FONT.render('PONG ONLINE',1,WHITE),(WIDTH//2-120,HEIGHT//2-50-150))
			pygame.draw.rect(WIN,BLACK, pygame.Rect(WIDTH//2-100-5,HEIGHT//2-50+4, 220+5 , 40))

			WIN.blit(BUTTON_FONT.render("SELECT SEVER",1,WHITE),(WIDTH//2-100,HEIGHT//2-50))
		elif self.STATUS == 'SERVER_SELECT':
			if self.SERVER_SCANING == None:
				threading.Thread(target=self.DrawServer).start()
			#print(self.SERVER_LIST,self.SERVER_SCANING)
			WIN.blit(TITLE_FONT.render('PONG ONLINE',1,WHITE),(100,HEIGHT//2-50-150))
			
			pygame.draw.rect(WIN,BLACK, pygame.Rect(WIDTH*0.1,HEIGHT//2-50+4, WIDTH*0.8 , HEIGHT-(HEIGHT//2-50+4)))
			pygame.draw.rect(WIN,BLACK, pygame.Rect(WIDTH-150-2,HEIGHT//2-75, 70+1 , 20+5))
			
			WIN.blit(SERVER_LIST_FONT.render("SELECT SEVER",1,WHITE),(WIDTH//2-300,HEIGHT//2-75))
			WIN.blit(SERVER_LIST_FONT.render("REFRESH",1,WHITE),(WIDTH-150,HEIGHT//2-75))
			for i in range(len(self.SERVER_LIST)):
				t = "IP: "+str(list(self.SERVER_LIST.items())[0][0])+"             Number of Player: "+str(list(self.SERVER_LIST.items())[0][1])
				WIN.blit(SERVER_LIST_FONT.render(t,1,WHITE),(WIDTH//2-300,(HEIGHT//2-40)+i*30))
				pygame.draw.rect(WIN,WHITE, pygame.Rect(WIDTH*0.1,((HEIGHT//2-40)+i*30)+28,WIDTH*0.8 , 2))
	def DrawServer(self):
		print(self.SERVER_LIST,self.SERVER_SCANING)
		self.SERVER_SCANING ='WORK'
		print(self.SERVER_LIST,self.SERVER_SCANING)
		self.SERVER_LIST = self.c.scan()
		self.SERVER_SCANING ='DONE'
		print(self.SERVER_LIST,self.SERVER_SCANING)
		
	def CheckRefresh(self,kp,evv):
		if self.STATUS == 'Menu':
			for ev in evv:  
				if ev.type == pygame.MOUSEBUTTONDOWN:
					mouse = pygame.mouse.get_pos()
					if mouse[0]>=WIDTH//2-100-5 and mouse[0]<=(WIDTH//2-100-5)+220+5 and mouse[1]>=HEIGHT//2-50+4 and mouse[1]<=(HEIGHT//2-50+4)+40:
						print('mouseclicked at ',mouse)
						self.STATUS = 'SERVER_SELECT'
		elif  kp[pygame.K_DELETE] or kp[pygame.K_BACKSPACE]:
			self.STATUS='Menu'

	def CheckServerSelect(self,kp,evv):
		if self.STATUS == 'SERVER_SELECT':
			for ev in evv:  
				if ev.type == pygame.MOUSEBUTTONDOWN:
					mouse = pygame.mouse.get_pos()
					x=WIDTH-150-2
					y=HEIGHT//2-75
					xx=70+1
					yy=20+5

	def CheckMenu(self,kp,evv):
		if self.STATUS == 'SERVER_SELECT':
			for ev in evv:  
				if ev.type == pygame.MOUSEBUTTONDOWN:
					mouse = pygame.mouse.get_pos()
					x=WIDTH*0.1
					y=HEIGHT//2-50+4
					xx=WIDTH*0.8
					yy=HEIGHT-(HEIGHT//2-50+4)
					
					
					if mouse[0]>=x and mouse[0]<=x+xx and mouse[1]>=y and mouse[1]<=y+yy:
						ii = (mouse[1]-(HEIGHT//2-40))//30
						if len(self.SERVER_LIST)-1>=ii:
							print('join')
							from main import main
							main(list(self.SERVER_LIST.items())[ii][0])
						

		

m = Menu()




def draw_window():
	WIN.fill(GREY)
	m.DrawMenu()
	

	'''
	WIN.fill(GREY)
	nb_bul_text = BULLET_FONT.render(str(SCORE),1,WHITE)
	WIN.blit(nb_bul_text,(0,HEIGHT//2))
	score_text = SCORE_FONT.render(str(M_SCORE),1,WHITE)
	WIN.blit(score_text,(100,HEIGHT//2))


	pygame.draw.rect(WIN,WHITE, YOUR_PADDEL)
	pygame.draw.rect(WIN,WHITE, OPPO_PADDEL)
	pygame.draw.circle(WIN,WHITE, (BALLE.x, BALLE.y), BALLE.r)
	#pygame.draw.rect(WIN,BLACK, HUD_BORDER)

	'''

	pygame.display.update()

def paddel_manager(keys_pressed):
	'''
	global YOUR_PADDEL
	if keys_pressed[pygame.K_d] and YOUR_PADDEL.x + PADDEL_VEL+YOUR_PADDEL.width <= WIDTH:
		YOUR_PADDEL.x += PADDEL_VEL
	if keys_pressed[pygame.K_q] and YOUR_PADDEL.x - PADDEL_VEL >= 0:
		YOUR_PADDEL.x -= PADDEL_VEL
	'''
	pass


def key_manager(keys_pressed, event):
	paddel_manager(keys_pressed)
	m.CheckMenu(keys_pressed,event)
	m.CheckRefresh(keys_pressed,event)

		
def main():
	#global YOUR_PADDEL

	clock = pygame.time.Clock()
	run = True
	#threading.Thread(target=update_pos).start()
	while run:
		clock.tick(FPS)
		ev  = pygame.event.get()
		for event in ev:
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				print("pressed")
		keys_pressed = pygame.key.get_pressed()
		key_manager(keys_pressed,ev)
		#check_BALLE_colision()
		draw_window()
		
		

	pygame.quit()

if __name__ == "__main__":
	main()

'''
c = conection()
c.send({"type":"position"})

msg = "Message from Server {}".format(c.recive())
print(msg)
'''
