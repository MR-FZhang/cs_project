#setting up a level
import pygame
import random
import sys
from level_map import *
from import_spritesheet import *

pygame.init()

size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60   
class Level():
  def __init__(self, map, surface):
    self.display_surface = surface
    self.screen_bond = 200
    self.map = map
    self.load_map(map)
    self.shift = 0
    self.camera_pos = pygame.math.Vector2(0,0)
      
  def load_map(self, map):
    # creating a sprite group to hold the player and map_tiles 
    self.tiles = pygame.sprite.Group()
    # the enumerate function returns the row count value itself
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
        if cell == 'P':
          player = Player((x,y), 30)
          self.player = player
          #health_bar = HealthBar(10, 10, player.health, player.health)
          #self.health_bar = health_bar
        if cell == 'E':
          print("enemy", x, y)
          start,end = self.get_boundary(col_num, row_num)
          enemy = Enemies((x,y), 30, start, end)
          enemies_group.add(enemy)
        if cell == 'H':
          pick_up = Pick_up((x,y),30)
          pick_ups_group.add(pick_up)
  
  def pick_up_collesion(self):
    group = pygame.sprite.spritecollide(self.player, pick_ups_group, False)
    player = self.player
    for pick_up in group:
        
      player.health = player.health + 10
      if self.player.health > player.max_health:
          player.health = player.max_health
      pick_up.kill()
      print(player.health)
  
  def get_boundary(self, col_num, row_num):
    row_num = row_num + 1
    start_boundary = col_num * sprite_size
    while map[row_num][col_num] == 'X':
      col_num += 1
    return start_boundary, col_num * sprite_size

  def x_collision(self):
    player = self.player
    player.rect.x += player.direction.x * player.speed
    
    for tiles in self.tiles.sprites():
      if tiles.rect.colliderect(player.rect):
        if player.direction.x < 0:
          player.rect.left = tiles.rect.right
        elif player.direction.x > 0:
          player.rect.right = tiles.rect.left
  
  def y_collision(self):
      player = self.player
      player.apply_gravity()
      
      for tiles in self.tiles.sprites():
        if tiles.rect.colliderect(player.rect):
          if player.direction.y < 0:
            player.rect.top = tiles.rect.bottom
            player.direction.y = 0
          elif player.direction.y > 0:
            player.rect.bottom = tiles.rect.top
            player.direction.y = 0   
  
  # function to track the player. Once to player exceeds a boundary the position of the camera shifts
  #with each iteration, objects will be drawn according to the poisiton of the camera
  def camera_update(self):
    if self.player.rect.left < self.camera_pos.x + 200:
      self.camera_pos.x = self.player.rect.left - 200
    
    if self.player.rect.right > self.camera_pos.x + screen_width - 200:
      self.camera_pos.x = self.player.rect.right - screen_width + 200

  def run(self):
      #getting the current camera position
      self.camera_update()
      # Displaying the map tiles
      for tile in self.tiles:
        tile.draw(self.display_surface, self.camera_pos)
      self.tiles.update(self.shift)
      # checking for collisions
      self.x_collision()
      self.y_collision()
      # Displaying the player
      self.player.draw(self.display_surface,self.camera_pos)
      self.player.update()
      #Displaying the enemies
      for enemy in enemies_group:
        enemy.draw(self.display_surface,self.camera_pos)
      enemies_group.update()
      for pick_up in pick_ups_group:
        pick_up.draw(self.display_surface,self.camera_pos)
      #Checking for collision between player and pick_ups
      self.pick_up_collesion()
      #self.health_bar.draw(self.player.health)

class Player(pygame.sprite.Sprite):
  def __init__(self,pos ,size):
    super().__init__()
    self.filename = './graphics/Animation'
    self.spritesheet = Spritesheet(self.filename)
    self.attack = self.spritesheet.get_spritelist('Attack', 4)
    print(self.attack)
    print(len(self.attack))
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect(topleft = pos)
    self.image.fill('Blue')
    self.speed = 10
    self.direction = pygame.math.Vector2(0,0)
    self.gravity = 0.80
    self.jump_speed = -15
    self.health = 100
    self.max_health = self.health
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
    self.rect.y += self.direction.y
    
  # Function to update player status  
  def update(self):
    self.player_input()
  def draw(self, screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y))

class Enemies(pygame.sprite.Sprite):
  def __init__(self, pos, size, start, end):
    super().__init__()
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect(topleft = (pos[0],pos[1] + 30))
    self.image.fill('red')
    self.speed = random.randint(1,4)
    self.direction = 1
    self.start = start
    self.end = end
    self.move = True
    bullet_group = pygame.sprite.Group()
  def movement(self):
    if self.move == True:
        self.rect.x += self.direction * self.speed
        if self.rect.right > self.end :
          self.rect.right = self.end
          self.direction *= -1
        elif self.rect.left < self.start:
          self.rect.left = self.start
          self.direction *= -1

  def update(self):
    self.movement()

  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y))

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
    
  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y))

class Pick_up(pygame.sprite.Sprite):
  def __init__(self,pos,size):
    super().__init__()
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect(topleft = (pos[0],pos[1] + 30))
    self.image.fill('green')
  
  
  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y))

# creating a pickup group
pick_ups_group = pygame.sprite.Group()
# creating a sprite group to hold enemies 
enemies_group = pygame.sprite.Group()          
# creating a bullet group 
#bullet_group = pygame.sprite.Group()
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