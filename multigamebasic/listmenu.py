import pygame
import threading

WHITE = (255,255,255)
BLACK = (0,0,0)
DARCK_GREY  = (25 , 25, 25)
GREY  = (50 , 50, 50)

class ListMenu():
	def __init__(self, **args):
		pygame.font.init()
		self.WIDTH, self.HEIGHT = 800 , 500 
		self.pos = args.pop('pos',(0,0))
		self.size = args.pop('size',(10,10))
		self.bg_color = args.pop('bg_color',(0,0,0))
		self.bg_color_hover = args.pop('bg_color_hover',self.bg_color)
		self.text_color = args.pop('text_color',(255,255,255))
		self.text_color_hover = args.pop('text_color_hover',self.text_color)

		self.font = args.pop('font',pygame.font.SysFont('impact',20))
		self.list = args.pop('list',[])
		self.text_spacing = args.pop('text_spacing',30)
		self.outline = args.pop('outline',True)
		self.outline_width = args.pop('outline',2)
		
		self.callback = args.pop('callback',None)
		self.bg_color_active = self.bg_color
		self.text_color_active = self.bg_color
		self.text_bias = args.pop('text_bias',(0,0))
		#global WIN
		#self.WIN = WIN
		



		
		"""YOUR_PADDEL = pygame.Rect(WIDTH//2-100-5,HEIGHT//2-50+4, 220+25 , 40)
		pygame.draw.rect(WIN,WHITE, YOUR_PADDEL)
		"""
	def Draw_Button(self, WIN):
		#print(self.WIN)

		pygame.draw.rect(WIN,self.bg_color_active,pygame.Rect(self.pos[0],self.pos[1], self.size[0] , self.size[1]))
		if self.outline == True:
			for i in range(len(self.list)):
				pygame.draw.rect(WIN,WHITE, pygame.Rect(self.pos[0],self.pos[1]-self.text_bias[1]+self.text_spacing*(i+1)-self.outline_width,self.size[0] , self.outline_width))

				WIN.blit(self.font.render(str(self.list[i]),1,self.text_color_active),(self.pos[0]-self.text_bias[0],self.pos[1]-self.text_bias[1]+self.text_spacing*i))
		else:
			for i in range(len(self.list)):
				WIN.blit(self.font.render(str(self.list[i]),1,self.text_color_active),(self.pos[0]-self.text_bias[0],self.pos[1]-self.text_bias[1]+self.text_spacing*i))


		return WIN
	def Check_pressed(self, ev):
		mouse = pygame.mouse.get_pos()
		self.bg_color_active= self.bg_color
		self.text_color_active= self.text_color

		if mouse[0]>=self.pos[0] and mouse[0]<=self.pos[0]+self.size[0] and mouse[1]>=self.pos[1] and mouse[1]<=self.pos[1]+self.size[1]:
			self.bg_color_active = self.bg_color_hover
			self.text_color_active= self.text_color_hover
		for event in ev:
			if event.type == pygame.MOUSEBUTTONDOWN:
				
				if mouse[0]>=self.pos[0] and mouse[0]<=self.pos[0]+self.size[0] and mouse[1]>=self.pos[1] and mouse[1]<=self.pos[1]+self.size[1]:
					index = (mouse[1]- self.pos[1])//self.text_spacing
					print("pressed_on_button",index)
					if self.callback != None:
						self.callback(index,self.list)





######### tmp
'''
WIDTH, HEIGHT = 800 , 500 
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))


def b_pressed(x):
	print("pressed")

w = 400
h = 300

b = ListMenu(list=['hello','by'],pos=(WIDTH//2-w//2,HEIGHT-h),size=(w,h),text_bias=(-10,0), callback=b_pressed ,bg_color=(75,75,75))
pygame.display.set_caption('Button')
#####


WHITE = (255,255,255)
BLACK = (0,0,0)
DARCK_GREY  = (25 , 25, 25)
GREY  = (50 , 50, 50)
FPS = 15

def main():
	

	clock = pygame.time.Clock()
	run = True

	while run:
		clock.tick(FPS)
		ev  = pygame.event.get()
		PYGAME_EVENT = ev
		for event in ev:
			if event.type == pygame.QUIT:
				run = False
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				print("pressed")
		b.Check_pressed(ev)
		keys_pressed = pygame.key.get_pressed()
		b.Draw_Button(WIN)

		
		#pygame.draw.rect(WIN,WHITE,pygame.Rect(WIDTH//2-100-5,HEIGHT//2-50+4, 220+25 , 40))
		pygame.display.update()
		
		

	pygame.quit()

if __name__ == "__main__":
	main()
'''