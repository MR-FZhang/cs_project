#creating a player class
import pygame 
import math

class Player(pygame.sprite.Sprite):
  def __init__(self,pos ,size):
    super().__init__()
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect(topleft = pos)
    self.image.fill('Blue')
    self.speed = 6
    self.direction = pygame.math.Vector2(0,0)
    self.gravity = 0.75
    self.jump_speed = -11
    
  # obtains inputs from the keyboard and updates player postion accordinly 
  
  
  def player_input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
      self.direction.x = 1
    elif keys[pygame.K_LEFT]:
      self.direction.x = -1
    else:
      self.direction.x = 0
    if keys[pygame.K_SPACE]:
      self.vertical_jump()
      
  # allow user to control player jump
    
  def vertical_jump(self):
    self.direction.y = self.jump_speed
  
  # applies gravity to the player, note adding a float < 1 to rect.x or y does happens
  #this is because it is rounded down to zero.
  def apply_gravity (self):
    self.direction.y += self.gravity
    print(self.direction.y)
    self.rect.y += self.direction.y
    
    
    
  # Function to update player status  
  def update(self):
    self.player_input()
   
    

    



  
    
