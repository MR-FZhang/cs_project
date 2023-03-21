import pygame
from settings import tile_size
from csv import reader
from os import walk 
import json

def import_csv_layout(path):
  
  terrain_map = []
  with open(path) as map:
    level = reader(map, delimiter = ',')
    for row in level:
      terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
  
  surface_list = []
  for _,__, image_files in walk(path):
    for image in image_files:
      
      full_path = path + '/' + image
      image_surf = pygame.image.load(full_path).convert_alpha()
      surface_list.append(image_surf)
  
  return surface_list

def import_cut_graph(path, width, height):
  
  surface = pygame.image.load(path).convert_alpha()
  tile_num_x = int(surface.get_size()[0] / width)
  tile_num_y = int(surface.get_size()[1] / height)

  cut_tiles = []
  
  for row in range(tile_num_y):
    for col in range(tile_num_x):
      x = col * width
      y = row * height
      new_surf = pygame.Surface((width, height), flags = pygame.SRCALPHA)
      new_surf.blit(surface, (0, 0), pygame.Rect(x, y, width, height))
      cut_tiles.append(new_surf)
  
  return cut_tiles

class Spritesheet:
  def __init__(self, filename):
    self.filename = f'{filename}.png'
    self.sprite_sheet = pygame.image.load(self.filename).convert_alpha()
    self.meta_data = f'{filename}.json'
    #opens up the json file
    with open(self.meta_data) as file:
      #loading the meta data
      self.data = json.load(file)
    #closing
    file.close()
  
  def get_sprite(self, x, y, w, h):
    #getting a pygame surface, with size and the image
    sprite = pygame.Surface((w, h))
    # defines colours that will not be displayed on to the screen, when it is run
    sprite.set_colorkey((0,0,0))
    sprite.blit(self.sprite_sheet,(0,0),(x, y, w, h))
    return sprite
  
  def get_spritelist(self, name, num_pic):
    
    self.sprite_list = []
    for x in range (num_pic):
      sprite = self.data['frames'][f'{name}{x}.png']['frame']
      x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
      image = self.get_sprite(x, y, w, h)
      enlarged_img = pygame.transform.scale(image, ((w * 2), (h * 2 ))).convert_alpha()
      self.sprite_list.append(enlarged_img)
    return self.sprite_list

  
    
