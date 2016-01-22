import pygame
import time
import random

pygame.init()

window_height = 800
window_width = 800

floor = 700
gravity = 1200
player_Jump_Impulse = 600
enemy_Speed = 600


display = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
enemyImage = pygame.image.load("SpaceShip3.png")
playerImage = pygame.image.load("2.png")
playerImage = pygame.transform.scale(playerImage,(48,48))



class Player(object):
	x = 0
	y = 0
	velocity_x = 0
	velocity_y = 0
	width = 48
	height = 48 #double the source image resolution
	isJumping = False

	def __init__(self,x,y):
		self.x = x
		self.y = y
		
	def rect(self): #Return rectangle for collision
		return pygame.Rect(self.x, self.y, self.width, self.height)
	
	def update(self, deltaTime):
		self.gravity(deltaTime)
		self.x += self.velocity_x * deltaTime
		self.y += self.velocity_y * deltaTime
		self.restrict()
		
	def restrict(self):
		if self.y > floor:  #If you are below the floor with 0,0 being top left
			self.y = floor
			self.velocity_y = 0
			self.isJumping = False
			
	def gravity(self, deltaTime):
		self.velocity_y += gravity * deltaTime
		
	def Jump(self, deltaTime):
		if self.isJumping == False:
			self.velocity_y = -player_Jump_Impulse
			self.isJumping = True
		
class Enemy(object):
	x = 0
	y = 0
	velocity_x = 0
	velocity_y = 0
	width = 24
	height = 24
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
	
	def update(self, deltaTime):
		self.x += self.velocity_x * deltaTime
		self.y += self.velocity_y * deltaTime
		if self.x < -1 * self.width:
			self.x = 800
		
	def rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)

		
def main_Menu():
	display.fill((0,0,0))
	font = pygame.font.Font('freesansbold.ttf', 60)
	text = font.render("Jump!", True, (255,255,255))
	textRect = text.get_rect()
	textRect.center = (window_width/2, window_height/2)
	display.blit(text, textRect)
	pygame.display.update()
	wait_For_Secs(2)
	game_Loop()
	
def game_Loop():
	deltaTime = clock.tick(60) / 1000
	display.fill((140,140,140))
	pygame.display.update()
	
	player = Player(200,600)
	enemy = Enemy(800,700)
	enemy.velocity_x = -enemy_Speed
	
	while True:
		deltaTime = clock.tick(60) / 1000
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					player.Jump(deltaTime)
		
		
		list_rects = [] #List of Rectangles for the screen to update
		
		list_rects.append(player.rect()) #Store old positions to be updated on the screen so we don't leave a streak of old positions on the window
		list_rects.append(enemy.rect())
		
		player.update(deltaTime)
		enemy.update(deltaTime)
		
		list_rects.append(player.rect()) #Store new positions so that the new position actually gets drawn
		list_rects.append(enemy.rect())
		
		if player.rect().colliderect(enemy.rect()): #check for collision
			break
		
		display.fill((140,140,140))
		display.blit(playerImage, player.rect())
		display.blit(enemyImage, enemy.rect())
		pygame.display.update(list_rects)
		
	game_Over()
		
def game_Over():
	display.fill((0,0,0))
	font = pygame.font.Font('freesansbold.ttf', 60)
	text = font.render("Game Over", True, (255,255,255))
	textRect = text.get_rect()
	textRect.center = (window_width/2, window_height/2)
	display.blit(text, textRect)
	pygame.display.update()
	wait_For_Secs(2)
	main_Menu()
	
def wait_For_Secs(time):
	initTime = pygame.time.get_ticks()
	
	while pygame.time.get_ticks() < initTime + time * 1000:
		handle_Window_Events()
		
	
def handle_Window_Events():
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
		
main_Menu()
	
	


