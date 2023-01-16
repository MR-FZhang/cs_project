import pygame
from support import import_folder, Spritesheet
import random
class Tile(pygame.sprite.Sprite):
  def __init__(self, width, height, x, y):
    super().__init__()
    self.image = pygame.Surface((width, height))
    
    self.rect = self.image.get_rect(topleft = (x,y))
    
  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

class StaticTile(Tile):
  def __init__(self, width, height, x, y, surface):
    super().__init__(width, height, x, y)
    self.image = surface
  
class Animated_tile(Tile):
  def __init__(self, width, height, x, y, path):
    super().__init__(width, height, x, y)
    self.frames = import_folder(path)
    self.frame_index = 0
    self.image = self.frames[int(self.frame_index)]
    self.animation_frame = 0.50

  def animations(self):
    self.frame_index += self.animation_frame
    if self.frame_index >= len(self.frames):
      self.frame_index = 0
    self.image = self.frames[int(self.frame_index)]

  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

  def update(self):
    self.animations()

class coins(Animated_tile):
  def __init__(self, width, height, x, y, path):
    super().__init__(width, height, x, y, path)
    center_x = x + int(width / 2)
    center_y = y + int(height / 2)
    self.rect = self.image.get_rect(center = (center_x, center_y))
    self.object = 'coins'

class diamonds(Animated_tile):
  def __init__(self, width, height, x, y, path):
    super().__init__(width, height, x, y, path)
    center_x = x + int(width / 2)
    center_y = y + int(height / 2)
    self.rect = self.image.get_rect(center = (center_x, center_y))
    self.object = 'diamonds'

class potions(Animated_tile):
  def __init__(self, width, height, x, y, path):
    super().__init__(width, height, x, y, path)
    center_x = x + int(width / 2)
    center_y = y + int(height / 2)
    self.rect = self.image.get_rect(center = (center_x, center_y))
    