#setting up a level
import pygame
import sys
from level_map import *
from import_spritesheet import *

pygame.init()

size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60   

# all game events happen here
class Level():
  def __init__(self, map, surface):
    self.display_surface = surface
    self.screen_bond = 200
    self.map = map
    self.load_map(map)
    self.camera_pos = pygame.math.Vector2(0, 0)
    self.screen_bond_height = 25 
    self.shift = 0
  
  def load_map(self, map):
    # creating a sprite group to hold the player and map_tiles 
    self.tiles_group = pygame.sprite.Group()
    self.player_group =pygame.sprite.GroupSingle()
    # the enumerate function returns the row count value itself
    for row_num, row in enumerate(map):
      for col_num, cell in enumerate(row):
        # getting the scaled coordinates of the tiles
        y = row_num * sprite_size 
        x = col_num * sprite_size 
        if cell == 'X':
          # instantiating a sprite
          tile = Sprites((x,y), sprite_size)
          self.tiles_group.add(tile)
        #placing the player at W on the map
        if cell == 'P':
          player = Player((x,y), 66)
          self.player_group.add(player)
          self.player = self.player_group.sprite


  def x_collision(self):


    player = self.player_group.sprite
    player.rect.x += player.direction.x * player.speed
    if (player.rect.x >= screen_width - self.screen_bond and player.direction.x == 1)or (player.rect.x <= self.screen_bond and player.direction.x == -1):
      
      player.rect.x -= (player.speed * player.direction.x)
      self.shift = - (player.speed * player.direction.x)
    else:
      self.shift = 0
    
    for sprite in self.tiles_group.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.x < 0: 
          player.rect.left = sprite.rect.right
          
          self.current_x = player.rect.left
        elif player.direction.x > 0:
          player.rect.right = sprite.rect.left
          
          self.current_x = player.rect.right

  def y_collision(self):
    player = self.player_group.sprite
    player.apply_gravity()
    
    for sprite in self.tiles_group.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.y > 0: 
          player.rect.bottom = sprite.rect.top
          player.direction.y = 0
        elif player.direction.y < 0:
          player.rect.top = sprite.rect.bottom   
          player.direction.y = 0

  def run(self):
      # Displaying the map tiles
      for tile in self.tiles_group:
        tile.draw(self.display_surface, self.camera_pos)
      self.tiles_group.update(self.shift)
      # checking for collisions
      self.x_collision()
      self.y_collision()
      # Displaying the player
      self.player.draw(self.display_surface, self.camera_pos)
      self.player.update()

# defines player characteristics and its methods
class Player(pygame.sprite.Sprite):
  def __init__(self,pos, size):
    super().__init__()
    self.image = pygame.Surface((size,size))
    self.image.fill('yellow')
    self.rect = self.image.get_rect(topleft = pos)
    self.speed = 8
    self.direction = pygame.math.Vector2(0,0)
    self.gravity = 0.75
    self.jump_speed = -15 
    self.on_left = False
    self.on_right = False
    self.on_ground = False
    self.on_ceiling =False
 
  # obtains inputs from the keyboard and updates player postion accordinly 
  def player_input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
      self.direction.x = 1
      self.facing_right = True
    elif keys[pygame.K_LEFT]:
      self.direction.x = -1
      self.facing_right = False
    else:
      self.direction.x = 0
    
    if keys[pygame.K_SPACE]:
        self.vertical_jump()
    
    if keys[pygame.K_q]  :
      self.attack = True  
  
  # allow user to control player jump 
  def vertical_jump(self):
    if self.on_ground == True and self.direction.y == 0:
      self.direction.y = self.jump_speed

  # applies gravity to the player, note adding a float < 1 to rect.x or y does happens
  #this is because it is rounded down to zero.
  def apply_gravity (self):
    self.direction.y += self.gravity
    self.rect.y += self.direction.y
     
  # Function to update player status  
  def update(self):
    self.player_input()
    
  def draw(self, screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

# defining a sprite class, inherites from sprite
class Sprites(pygame.sprite.Sprite):
  # defining the constructor for the class
  def __init__(self,pos,size):
    super().__init__()
    # creates a square with specified size
    self.image = pygame.Surface((size,size))
    # give the square colour
    self.image.fill('blue')
    # gets a rectangular square around the image, with the topleft position at pos
    self.rect = self.image.get_rect(topleft = pos)
 
 # updating the tile positions based on the player positions
  def update(self, shift):
    self.rect.x += shift

  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

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