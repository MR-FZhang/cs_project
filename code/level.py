#setting up a level
from re import S
from sprites import Sprites
from level_map import *
import pygame
from player import Player

class Level():
  def __init__(self, map, surface):
    self.display_surface = surface
    self.screen_bond = 200
    self.load_map(map)
    self.shift = 0
    

  def load_map(self, map):
    # creating a sprite group to hold the map tiles
    self.tiles = pygame.sprite.Group()
    # the enumerate function returns the row count value itself
    self.player = pygame.sprite.GroupSingle()
    for row_num, row in enumerate(map):
      for col_num, cell in enumerate(row):
        # getting the scaled coordinates of the tiles
        y = row_num * sprite_size 
        x = col_num * sprite_size 
        if cell == 'X':
          # instantiating a sprite
          tile = Sprites((x,y), sprite_size)
          self.tiles.add(tile)
        #placing the player at W on the map
        if cell == 'W':
          player = Player((x,y), 30)
          self.player.add(player)

  def x_collision(self):
    player = self.player.sprite 
    player.rect.x += player.direction.x * player.speed
    
    for tiles in self.tiles.sprites():
      if tiles.rect.colliderect(player.rect):
        if player.direction.x < 0:
          player.rect.left = tiles.rect.right
        elif player.direction.x > 0:
          player.rect.right = tiles.rect.left
  
  def y_collision(self):
      player = self.player.sprite 
      player.apply_gravity()
      print (player.direction.y)
      for tiles in self.tiles.sprites():
        if tiles.rect.colliderect(player.rect):
          if player.direction.y < 0:
            player.rect.top = tiles.rect.bottom
            player.direction.y = 0
          elif player.direction.y > 0:
            player.rect.bottom = tiles.rect.top
            player.direction.y = 0   
 

  def level_shift(self):
    if self.player.sprite.rect.centerx <= self.screen_bond and self.player.sprite.direction.x <0:
      self.player.sprite.speed = 0
      self.shift = 6
    elif self.player.sprite.rect.centerx >= (screen_width - self.screen_bond) and self.player.sprite.direction.x > 0 : 
      self.player.sprite.speed = 0
      self.shift = -6
    else:
      self.shift = 0
      self.player.sprite.speed = 6

  def run(self):
      # Displaying the map tiles
      self.tiles.draw(self.display_surface)
      self.tiles.update(self.shift)
      # Displaying tile movement   
      self.level_shift()
      # checking for collisions
      self.x_collision()
      self.y_collision()
      # Displaying the player
      self.player.draw(self.display_surface)
      self.player.update()
      