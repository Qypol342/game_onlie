import pygame
import socket
from lib.connection import conection
from lib.cirl import Cirl
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
DARCK_GREY  = (25 , 25, 25)
LIGHT_GREY  = (120 , 120, 120)
RED  = (255 , 0, 0)
GREEN  = (0 , 255, 0)
BULLET_FONT = pygame.font.SysFont('arial',20)
SCORE_FONT = pygame.font.SysFont('arial',40)
PACKAGE_FONT = pygame.font.SysFont('arial',10)
NB_PACKAGE = 0
TICK = 0
M_SCORE = ''
HUD_BORDER = pygame.Rect(0, 50, WIDTH , 10)

YOUR_PADDEL = pygame.Rect(WIDTH//2-WIDTH*0.1//2, HEIGHT-50, WIDTH*0.1 , 20)
OPPO_PADDEL = pygame.Rect(WIDTH//2-WIDTH*0.1//2, 50-20, WIDTH*0.1 , 20)

BALLE = Cirl(WIDTH//2, HEIGHT//2, 20, 0)
PADDEL_VEL = 5

FPS = 60

hostname = socket.gethostname()
		
DEFAULT_IP = socket.gethostbyname_ex(hostname)[-1][-1]

SCORE = (0,0)
RUN = True



def draw_window():
	global NB_PACKAGE
	WIN.fill(GREY)
	nb_bul_text = BULLET_FONT.render(str(SCORE),1,WHITE)
	WIN.blit(nb_bul_text,(0,HEIGHT//2))
	if int(NB_PACKAGE/TICK)<=80:
		WIN.blit(PACKAGE_FONT.render(str(int(NB_PACKAGE/TICK)),1,RED),(10,10))
	elif int(NB_PACKAGE/TICK)>80 and int(NB_PACKAGE/TICK)<=90:
		WIN.blit(PACKAGE_FONT.render(str(int(NB_PACKAGE/TICK)),1,LIGHT_GREY),(10,10))
	else :
		WIN.blit(PACKAGE_FONT.render(str(int(NB_PACKAGE/TICK)),1,GREEN),(10,10))
	score_text = SCORE_FONT.render(str(M_SCORE),1,WHITE)
	WIN.blit(score_text,(100,HEIGHT//2))


	pygame.draw.rect(WIN,WHITE, YOUR_PADDEL)
	pygame.draw.rect(WIN,WHITE, OPPO_PADDEL)
	pygame.draw.circle(WIN,WHITE, (BALLE.x, BALLE.y), BALLE.r)
	#pygame.draw.rect(WIN,BLACK, HUD_BORDER)



	pygame.display.update()

def paddel_manager(keys_pressed):
	global YOUR_PADDEL
	if keys_pressed[pygame.K_d] and YOUR_PADDEL.x + PADDEL_VEL+YOUR_PADDEL.width <= WIDTH:
		YOUR_PADDEL.x += PADDEL_VEL
	if keys_pressed[pygame.K_q] and YOUR_PADDEL.x - PADDEL_VEL >= 0:
		YOUR_PADDEL.x -= PADDEL_VEL
	if  keys_pressed[pygame.K_DELETE] or keys_pressed[pygame.K_BACKSPACE]:
			global RUN 
			RUN = False
def tmp_balle_manager(keys_pressed):
	global BALLE
	if keys_pressed[pygame.K_UP] and BALLE.x + PADDEL_VEL <= HEIGHT:
		BALLE.y -= PADDEL_VEL
		BALLE.v = 0
	if keys_pressed[pygame.K_DOWN] and BALLE.x - PADDEL_VEL <= HEIGHT:
		BALLE.y += PADDEL_VEL
		BALLE.v = 0


def key_manager(keys_pressed):
	paddel_manager(keys_pressed)
	#tmp_balle_manager(keys_pressed)
	'''
def check_BALLE_colision():
	global BALLE
	global YOUR_PADDEL
	
	if BALLE.y+BALLE.r >= YOUR_PADDEL.y:
		print("Below")
		print(BALLE.x-BALLE.r > YOUR_PADDEL.x , BALLE.x+BALLE.r< YOUR_PADDEL.x+YOUR_PADDEL.width)
		print(BALLE.x-BALLE.r , YOUR_PADDEL.x , BALLE.x+BALLE.r, YOUR_PADDEL.x+YOUR_PADDEL.width)
		if BALLE.x+BALLE.r > YOUR_PADDEL.x and BALLE.x-BALLE.r< YOUR_PADDEL.x+YOUR_PADDEL.width :
			print('touch')
			distance = BALLE.x- YOUR_PADDEL.x- YOUR_PADDEL.width//2 
			print(tan(distance/60))
			BALLE.v = tan(distance/60)

'''

def update_pos():
	global YOUR_PADDEL
	global BALLE
	global OPPO_PADDEL
	global SCORE
	global M_SCORE
	global NB_PACKAGE
	c = conection(DEFAULT_IP)
	while  RUN:
		c.send({'type':'IN_GAME_DATA','DATA':YOUR_PADDEL.x})
		r = c.recive()
		NB_PACKAGE += 1
		if r !=  False:
			r = eval(r)
			#print(r)
			OPPO_PADDEL.x = r[0]
			BALLE.x = r[1][0]
			BALLE.y = r[1][1]
			SCORE = r[2]
			e_s = (SCORE)
			if e_s[0] >= 10:
				M_SCORE = 'YOU WON'
			elif e_s[1] >= 10:
				M_SCORE = 'YOU LOSE'
			else:
				M_SCORE =''



		#time.sleep(0.1)
		
def main(ip):
	global DEFAULT_IP
	global NB_PACKAGE
	global TICK
	global RUN
	RUN = True
	DEFAULT_IP = ip
	print(ip)

	clock = pygame.time.Clock()
	
	threading.Thread(target=update_pos).start()
	while RUN:
		TICK += 1 
		clock.tick(FPS)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				
				RUN = False
		keys_pressed = pygame.key.get_pressed()
		key_manager(keys_pressed)
		#check_BALLE_colision()
		draw_window()
		if TICK >= 60:
			TICK = 0 
			NB_PACKAGE = 0
		
		

	############pygame.quit()

if __name__ == "__main__":
	main(DEFAULT_IP)
