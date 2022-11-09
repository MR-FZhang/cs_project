import pygame 
import json
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
    sprite_list = []
    for x in range (num_pic):
      sprite = self.data['frames'][f'{name}{x}.png']['frame']
      x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
      image = self.get_sprite(x, y, w, h)
      sprite_list.append(image)
    return sprite_list