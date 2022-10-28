import pygame 
from level_map import *

# defining a sprite class, inherites from sprite
class Sprites(pygame.sprite.Sprite):
  # defining the constructor for the class
  def __init__(self,pos,size):
    super().__init__()
    # creates a square with specified size
    self.image = pygame.Surface((size,size))
    # give the square colour
    self.image.fill('grey')
    # gets a rectangular square around the image, with the topleft position at pos
    self.rect = self.image.get_rect(topleft = pos)
    
  def update(self, scroll):
    self.rect.x += scroll