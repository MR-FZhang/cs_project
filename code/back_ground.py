import pygame, sys
from settings import *

#Pygame setp
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


bg_images = []

scroll = 0
for i in range(4):
    bg_image = pygame.image.load(f"././graphics/background/background{i}.png").convert_alpha()
    bg_images.append(bg_image)
    width = bg_image.get_width()
def draw_bg():
    for x in range(5):
      speed = 1
      for i in bg_images:
        screen.blit(i, ((x * width) - scroll * speed, 0))
        speed += 0.5

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  scroll += 2
  
  screen.fill('black')
  draw_bg()

  
  pygame.display.update()
  clock.tick(60)