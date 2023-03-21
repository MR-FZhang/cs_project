import pygame
import random
from support import Spritesheet
from settings import *

class troll_enemies(pygame.sprite.Sprite):
  def __init__(self, x, y, speed, path):
    super().__init__()
    self.speed = speed
    self.filename = path
    self.frame_index = 0 
    self.frame_speed = 0.5
    self.image = pygame.Surface((32, 32))
    self.rect = self.image.get_rect(bottomleft = (x, y + (tile_size + 15)))
    self.image_height = self.image.get_height()
    self.image_width = self.image.get_width()
    self.moving = True
    self.ammo = 100
    self.cool_down = 0 
    self.movement_counter = 0
    self.vision = pygame.Rect(0, 0, 50, 50)
    self.facing_right = True
    self.shoot_cooldown = 0
    self.attacking = False
    self.status = 'walk'
    self.enemy = 0
    self.direction = 1
    self.health = 100
    self.death_frame_index = 0
    self.attack_cooldown = 0
    self.enemy = 'troll'
    self.attack_sound_1 = pygame.mixer.Sound('./audio/enemy_attacking.wav')
    self.sound_cooldown = 0
  def get_visions(self):
    
    if self.facing_right == True:
      self.vision = pygame.Rect(self.rect.centerx , self.rect.centery, self.rect.width / 2 , self.rect.height)  

    if self.facing_right == False:
      self.vision = pygame.Rect(self.rect.centerx - (self.rect.width / 2)  , self.rect.centery, self.rect.width, self.rect.height)  
      
    # displaying enemy animations
  
  def death_animations (self):

    if self.status == 'death':
      
      self.death_frame_index += self.frame_speed
      self.animations_list = self.get_animations()

      if self.death_frame_index < len(self.animations_list):
        self.image = self.animations_list[int(self.death_frame_index)]
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
      
      if self.death_frame_index >= len(self.animations_list):
        self.image = self.animations_list[len(self.animations_list) - 1]
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
      self.direction = 0
      self.speed = 0

  def attack_action(self, player):
    
    if self.attacking == True and self.attack_cooldown <= 0:
      
      if self.facing_right == True:
        
        attacking_rect = pygame.Rect(self.rect.centerx , self.rect.y, self.rect.width / 2 , self.rect.height)  
        self.attaking = False
        
        self.attack_cooldown = 10
      
      if self.facing_right == False:
        
        attacking_rect = pygame.Rect(self.rect.centerx - self.rect.width / 2, self.rect.y, self.rect.width / 2 , self.rect.height)   
        self.attaking = False
        self.attack_cooldown = 10
        
      if player.rect.colliderect(attacking_rect) and player.health > 0 and self.attacking == True:
          self.attack_sound()
          player.health -= 50

    else :
      self.attack_cooldown -= 1

  def get_animations(self):
      animations = Spritesheet(self.filename)
   
      animations_list = {'walk':[],'idle':[],'attack':[],'attack_combo':[],'attack_power':[]}
      animations_list['walk'] = animations.get_spritelist('Walk', 8)
      animations_list['idle'] = animations.get_spritelist('Idle', 10)
      animations_list['attack'] = animations.get_spritelist('Attack', 10)
      animations_list['attack_combo'] = animations.get_spritelist('Attack_combo', 9)
      animations_list['attack_power'] = animations.get_spritelist('Attack_power', 7)
      animations_list['ultimate'] = animations_list['attack'] + animations_list['attack_combo'] + animations_list['attack_power']
      animations_list['death'] = animations.get_spritelist('Death', 7)
      
      return animations_list[self.status]
 
  def attack_sound(self):
      
      if self.sound_cooldown <= 0:
        self.attack_sound_1.play()
        self.sound_cooldown = 1
      else:
        self.sound_cooldown -= 1
  def get_status(self):
    if self.moving:
      self.status = 'walk'
    
    if not self.moving and self.attacking == False:
      self.status = 'idle'
    
    if self.attacking and self.attack_cooldown == 0 and not self.moving: 
      self.status = 'ultimate'    
    if self.health <= 0:
      self.status = 'death'
  
  def animations(self):

    self.animations_list = self.get_animations()

    self.frame_index += self.frame_speed
    if self.frame_index >= len(self.animations_list):
      self.frame_index = 0
    
    image = self.animations_list[int(self.frame_index)]
    
    if self.facing_right:
      self.image = image
      self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
    
    else:
      flipped_image = pygame.transform.flip(image,True,False)
      self.image = flipped_image
      self.rect = self.image.get_rect(bottomright = self.rect.bottomright)

  def move(self):
    if self.moving == True :
      if self.status == 'death':
        self.rect.x = self.rect.x
      else:  
        self.rect.x += self.direction * self.speed

  def reverse_image(self):
    if self.direction < 0:
      self.facing_right = False
    
    elif self.direction > 0:
      self.facing_right = True
  
  def reverse(self):
    self.direction *= -1

  def attack(self):
    self.attacking = True
    self.status == 'ultimate'
    
  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))
  
  def update(self):
    if self.status != 'death':
      self.get_status()
      self.animations()
      self.reverse_image()

class mech_enemies(troll_enemies):
  def __init__(self, x, y, speed, path):
    super().__init__(x, y, speed, path)

    self.death_frame_index = 0
    self.enemy = 'mech'

  def get_animations(self):
      animations = Spritesheet(self.filename)
      animations_list = {'walk':[],'idle':[],'attack':[],'attack_combo':[],'attack_power':[]}
      animations_list['walk'] = animations.get_spritelist('Walk', 8)
      animations_list['idle'] = animations.get_spritelist('Idle-', 13)
      animations_list['attack'] = animations.get_spritelist('Attack', 15)
      animations_list['attack_combo'] = animations.get_spritelist('Attack_combo', 10)
      animations_list['attack_power'] = animations.get_spritelist('Attack_power', 10)
      animations_list['ultimate'] = animations_list['attack'] + animations_list['attack_combo'] + animations_list['attack_power']
      animations_list['death'] = animations.get_spritelist('Death-', 8)

      return animations_list[self.status]

  def death_animations (self):

    if self.status == 'death':

      self.death_frame_index += self.frame_speed
      self.animations_list = self.get_animations()

      if self.death_frame_index < len(self.animations_list):
        self.image = self.animations_list[int(self.death_frame_index)]
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
      
      if self.death_frame_index >= len(self.animations_list):
        self.image = self.animations_list[len(self.animations_list) - 1]
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

  


