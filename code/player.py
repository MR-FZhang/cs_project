#creating a player class
import pygame 

class Player(pygame.sprite.Sprite):
  def __init__(self,x,y,screen):
    super().__init__()
