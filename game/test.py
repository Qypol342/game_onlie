import pygame
import time

pygame.font.init()

WIDTH, HEIGHT = 800 , 500 
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Pong')

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY  = (50 , 50, 50)
BULLET_FONT = pygame.font.SysFont('arial',40)



BALLE_HIT = pygame.USEREVENT +1

HUD_BORDER = pygame.Rect(0, 50, WIDTH , 10)

FPS = 60

T_COOL_DOWN  = 1
BLOOD_COOL_DOWN  = 1

def draw_window(b, bullet, back_col, nb_bul):
	WIN.fill(back_col)
	
	nb_bul_text = BULLET_FONT.render("Bullet: "+str(nb_bul),1,WHITE)
	WIN.blit(nb_bul_text,(0,10))

	BALLE_IMAGE = pygame.image.load('asset/balle.png')
	BALLE = pygame.transform.scale(BALLE_IMAGE,(50,50))
	pygame.draw.rect(WIN,BLACK, HUD_BORDER)
	WIN.blit(BALLE,(b.x,b.y))
	for i in bullet:
		pygame.draw.rect(WIN, BLACK, i)


	pygame.display.update()

def mouvement_balle(keys_pressed, balle, bullet):
	if keys_pressed[pygame.K_d]:
		balle.x += 2
	if keys_pressed[pygame.K_q]:
		balle.x -= 2
	if keys_pressed[pygame.K_z]:
		balle.y -= 2
	if keys_pressed[pygame.K_s]:
		balle.y += 2
	if balle.y >= HEIGHT-balle.height:
		balle.y = HEIGHT-balle.height
	if balle.y <= 0:
		balle.y = 0
	if keys_pressed[pygame.K_a]:
		global T_COOL_DOWN
		delta = time.time()  -T_COOL_DOWN
		print(delta)
		if len(bullet) < 10 and delta >= 0.5 :
			print("shot")
			_bullet = pygame.Rect(balle.x+balle.width, balle.y+balle.height//2, 20, 10)
			bullet.append(_bullet)
			T_COOL_DOWN = time.time()
	pygame.display.update()
def bullet_manager(balle, bullet):
	print(bullet)
	for b in  bullet:
		b.x += 1
		if balle.colliderect(b):
			bullet.remove(b)
			pygame.event.post(pygame.event.Event(BALLE_HIT))
		if b.x>WIDTH:
			bullet.remove(b)


	



def main():
	balle = pygame.Rect(50,100,50,50)


	clock = pygame.time.Clock()
	bullet = []
	BLOOD_COOL_DOWN = 0
	run = True
	while run:
		clock.tick(FPS)
		if BLOOD_COOL_DOWN == 0 or time.time()-BLOOD_COOL_DOWN>0.1:
			back_col = GREY
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == BALLE_HIT:
				back_col = (255,0,0)
				BLOOD_COOL_DOWN = time.time()
		#
		keys_pressed = pygame.key.get_pressed()


		bullet_manager(balle, bullet)
		mouvement_balle(keys_pressed, balle, bullet)
		

		draw_window(balle, bullet,back_col, len(bullet))
		

	pygame.quit()

if __name__ == "__main__":
	main()