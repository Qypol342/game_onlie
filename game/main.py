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
BULLET_FONT = pygame.font.SysFont('arial',20)
HUD_BORDER = pygame.Rect(0, 50, WIDTH , 10)
YOUR_PADDEL = pygame.Rect(WIDTH//2-WIDTH*0.1//2, HEIGHT-50, WIDTH*0.1 , 20)
OPPO_PADDEL = pygame.Rect(WIDTH//2-WIDTH*0.1//2, 50, WIDTH*0.1 , 20)

BALLE = Cirl(WIDTH//2, HEIGHT//2, 20, 0)
PADDEL_VEL = 2

FPS = 60
GAME_ID = 1212




def draw_window():
	WIN.fill(GREY)
	nb_bul_text = BULLET_FONT.render("Bullet: "+str(1),1,WHITE)
	WIN.blit(nb_bul_text,(0,HEIGHT//2))
	pygame.draw.rect(WIN,WHITE, YOUR_PADDEL)
	pygame.draw.rect(WIN,WHITE, OPPO_PADDEL)
	pygame.draw.circle(WIN,WHITE, (BALLE.x, BALLE.y), BALLE.r)
	#pygame.draw.rect(WIN,BLACK, HUD_BORDER)



	pygame.display.update()

def paddel_manager(keys_pressed):
	global YOUR_PADDEL
	if keys_pressed[pygame.K_d] and YOUR_PADDEL.x + PADDEL_VEL <= WIDTH:
		YOUR_PADDEL.x += PADDEL_VEL
	if keys_pressed[pygame.K_q] and YOUR_PADDEL.x - PADDEL_VEL >= 0:
		YOUR_PADDEL.x -= PADDEL_VEL
def tmp_balle_manager(keys_pressed):
	global BALLE
	if keys_pressed[pygame.K_UP] and BALLE.x + PADDEL_VEL <= HEIGHT:
		BALLE.y -= PADDEL_VEL
		BALLE.v = 0
	if keys_pressed[pygame.K_DOWN] and BALLE.x - PADDEL_VEL <= HEIGHT:
		BALLE.y += PADDEL_VEL
		BALLE.v = 0
	if BALLE.v != 0:
		if BALLE.x <= BALLE.r:
			BALLE.v = -BALLE.v
		if BALLE.x >= WIDTH- BALLE.r:
			BALLE.v = -BALLE.v
		BALLE.y -= 1
		BALLE.x += BALLE.v


def key_manager(keys_pressed):
	paddel_manager(keys_pressed)
	tmp_balle_manager(keys_pressed)
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



def update_pos():
	global YOUR_PADDEL
	global BALLE
	global OPPO_PADDEL
	c = conection()
	while  True:
		c.send(YOUR_PADDEL.x)
		r = c.recive()
		print(r)
		if r !=  False:
			r = eval(r)
			print(r)
			OPPO_PADDEL.x = r[0]

		time.sleep(0.1)
		
def main():
	#global YOUR_PADDEL

	clock = pygame.time.Clock()
	run = True
	threading.Thread(target=update_pos).start()
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		keys_pressed = pygame.key.get_pressed()
		key_manager(keys_pressed)
		check_BALLE_colision()
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
