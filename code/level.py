#setting up a level
from sprites import Sprites
from level_map import *
import pygame
class Level():
  def __init__(self, map, surface):
    self.display_surface = surface
    self.load_map(map)
    
  def run(self):
    self.tiles.draw(self.display_surface)
    self.tiles.update(-2)
  def load_map(self, map):
    # creating a sprite group to hold the map tiles
    self.tiles = pygame.sprite.Group()
    # the enumerate function returns the row count value itself
    
    for row_num, row in enumerate(map):
      for col_num, cell in enumerate(row):
        if cell == 'X':
          # getting the scaled coordinates of the tiles
          y = row_num * sprite_size 
          x = col_num * sprite_size 
          # instantiating a sprite
          tile = Sprites((x,y), sprite_size)
          self.tiles.add(tile)
  
