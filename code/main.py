import pygame 
import sys
from level_map import *
from level import Level
# setting up pygame
pygame.init()

size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60
# creates an instance of the level
level = Level(map,screen)
# setting up game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit
  screen.fill("black")
  # runs the entire level
  level.run()
  pygame.display.update()
  clock.tick(FPS)

  