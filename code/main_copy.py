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

# all game events happen here
class Level():
  def __init__(self, map, surface):
    self.display_surface = surface
    self.screen_bond = 200
    self.map = map
    self.load_map(map)
    self.shift = 0
    self.camera_pos = pygame.math.Vector2(0, 0)
    self.screen_bond_height = 25 
    self.current_x = 0
  
  def load_map(self, map):
    # creating a sprite group to hold the player and map_tiles 
    self.tiles_group = pygame.sprite.Group()
    # creating a pickup group
    self.pick_ups_group = pygame.sprite.Group()
    # creating a sprite group to hold enemies 
    self.enemies_group = pygame.sprite.Group()          
    # creating a bullet group 
    self.bullets_group = pygame.sprite.Group()
    # creating a player group
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
          player = Player((x,y), 80)
          self.player_group.add(player)
          self.player = self.player_group.sprite
          health_bar = HealthBar(10, 10, player.health, player.health)
          self.health_bar = health_bar
        if cell == 'E':
          start,end = self.get_boundary(col_num, row_num)
          enemy = Enemies((x,y), 30, start, end)
          self.enemies_group.add(enemy)
        if cell == 'H':
          pick_up = Pick_up((x,y),30)
          self.pick_ups_group.add(pick_up)
  
  def get_boundary(self, col_num, row_num):
    row_num = row_num + 1
    start_boundary = col_num * sprite_size
    while map[row_num][col_num] == 'X':
      col_num += 1
    return start_boundary, col_num * sprite_size

  def x_collision(self):

    #if player.rect.x > len(map[0]) * sprite_size and player.direction.x > 0:
    #  player.speed = 0
    #  
    #elif player.rect.x <= 0 and player.direction.x < 0:
    #  player.speed = 0
    #else: 
    player = self.player_group.sprite
    player.rect.x += player.direction.x * player.speed
    
    for sprite in self.tiles_group.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.x < 0: 
          player.rect.left = sprite.rect.right
          player.on_left = True
          self.current_x = player.rect.left
        elif player.direction.x > 0:
          player.rect.right = sprite.rect.left
          player.on_right = True
          self.current_x = player.rect.right
    
    if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
      player.on_left = False
    if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
      player.on_right = False

  def y_collision(self):
    player = self.player_group.sprite
    player.apply_gravity()
    
    for sprite in self.tiles_group.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.y > 0: 
          player.rect.bottom = sprite.rect.top
          player.direction.y = 0
          player.on_ground = True
        elif player.direction.y < 0:
          player.rect.top = sprite.rect.bottom
          player.direction.y = 0
          player.on_ceiling = True
    if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
      player.on_ground = False
    if player.on_ceiling and player.direction.y > 0.1:
      player.on_ceiling = False

  
  
  # function to track the player. Once to player exceeds a boundary the position of the camera shifts
  #with each iteration, objects will be drawn according to the poisiton of the camera
  def camera_update(self):
    if self.player.rect.left < self.camera_pos.x + self.screen_bond:
      self.camera_pos.x = self.player.rect.left - self.screen_bond
    
    if self.player.rect.right > self.camera_pos.x + screen_width - self.screen_bond:
      self.camera_pos.x = self.player.rect.right - screen_width + self.screen_bond
    # When the player's y is smaller than 0 but is falling, there would be an error if you set the camera to position to 0
    # because there is a gap for the player to travel before it can reach 0, so glitches would be seen
    if self.player.rect.top < self.camera_pos.y + 20:
      self.camera_pos.y = self.player.rect.top - 20
    elif self.player.rect.top < 20 and self.player.rect.top > self.camera_pos.y :
      self.camera_pos.y = self.player.rect.top -20
    elif self.player.rect.top >= 20:
      self.camera_pos.y = 20
  
  
  def run(self):
      #getting the current camera position
      self.camera_update()
      # Displaying the map tiles
      for tile in self.tiles_group:
        tile.draw(self.display_surface, self.camera_pos)
      #updaating tiles in tile group
      self.tiles_group.update(self.shift)
      # checking for collisions
      self.x_collision()
      self.y_collision()
      # Displaying the player
      self.player.draw(self.display_surface, self.camera_pos)
      self.player.update()
      #Displaying the enemies
      for enemy in self.enemies_group:
        enemy.draw(self.display_surface, self.camera_pos)
      # updating enemies
      self.enemies_group.update()
      # displaying pick_ups
      for pick_up in self.pick_ups_group:
        pick_up.draw(self.display_surface, self.camera_pos)
      #updating pick_ups status
      self.pick_ups_group.update()
      # displaying heath bar
      self.health_bar.draw(self.player.health)
      # displaying the all bullets
      for bullet in self.bullets_group:
        bullet.draw(self.display_surface, self.camera_pos)
      # updating bullets
      self.bullets_group.update(self.camera_pos)
      
# defines player characteristics and its methods
class Player(pygame.sprite.Sprite):
  def __init__(self,pos, size):
    super().__init__()
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect(topleft = pos)
    self.speed = 8
    self.direction = pygame.math.Vector2(0,0)
    self.gravity = 0.75
    self.jump_speed = -15
    self.health = 100
    self.max_health = self.health
    self.frame_index = 0
    self.frame_time = 0.20
    self.status = 'idle'
    self.on_left = False
    self.on_right = False
    self.on_ground = False
    self.on_ceiling =False
    self.facing_right = False
  # gets the current animation to be displayed
  
  def animation_actions(self, action):
    player_actions = {'idle':[],'run':[],'jump':[],'fall':[],'attack':[]}
    sprite_sheet = Spritesheet('./graphics/Animation')
    player_actions['idle'] = sprite_sheet.get_spritelist('Idle', 10)
    player_actions['run'] = sprite_sheet.get_spritelist('Run', 10)
    player_actions['jump'] = sprite_sheet.get_spritelist('Jump', 3)
    player_actions['attack'] = sprite_sheet.get_spritelist('Attack', 4)
    player_actions['fall'] = sprite_sheet.get_spritelist('Fall', 3)
    return player_actions[action]
 
  def animations(self):
    self.frame_index += self.frame_time
    self.animations_list = self.animation_actions(self.status)
    if self.frame_index >= len(self.animations_list):
      self.frame_index = 0

    image = self.animations_list[int(self.frame_index)]
    
    if self.facing_right:
      self.image = image
    else:
      flipped_image = pygame.transform.flip(image,True,False)
      self.image = flipped_image
    
    if self.on_ground and self.on_right:
      self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
    elif self.on_ground and self.on_left:
      self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
    elif self.on_ground:
      self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
    elif self.on_ceiling and self.on_right:
      self.rect = self.image.get_rect(topright = self.rect.topright)
    elif self.on_ceiling and self.on_left:
      self.rect = self.image.get_rect(topleft = self.rect.topleft)
    elif self.on_ceiling:
      self.rect = self.image.get_rect(midtop = self.rect.midtop)

  def get_status(self):
    if self.direction.y < 0:
      self.status = 'jump'
    elif self.direction.y > 1:
      self.status = 'fall'
    else:
      if self.direction.x != 0:
        self.status = 'run'
      else:
        self.status = 'idle'


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
      if self.on_ground == True and self.direction.y == 0:
        self.vertical_jump()
    
    if keys[pygame.K_q]  :
      self.attack = True  
  
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
    self.get_status()
    self.animations()
    self.player_input()
    
  def draw(self, screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

# blue print fro all of the enemies
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
    self.moving = True
    self.ammo = 100
    self.cool_down = 0 
    self.movement_counter = 0
    self.vision = pygame.Rect(0, 0, 150, 30)
    self.shoot_cooldown = 0
  
  def movement(self):
    if self.moving == True:
      self.rect.x += self.direction * self.speed
      if self.rect.right > self.end :
        self.rect.right = self.end
        self.direction *= -1
      elif self.rect.left < self.start:
        self.rect.left = self.start
        self.direction *= -1
    else:
      self.speed = 0
  
  def shoot(self):
    if self.shoot_cooldown == 0 and self.ammo > 0:
      self.shoot_cooldown = 20
      bullet = Bullet(self.rect.centerx + int(0.75 * self.rect.size[0] * self.direction), \
      self.rect.centery, 5, self.direction)
      level.bullets_group.add(bullet)
      #reduce ammo
      self.ammo -= 1
  
  def enemy_movement(self):
    if self.moving == False and random.randint(1, 200) == 1:
      self.movement_counter = 50
    #check if the ai in near the player
    if self.vision.colliderect(level.player.rect):
      #stop running and face the player
      self.moving = False
      #shoot
      self.shoot()
    else:
      if self.moving == True:
        self.movement()
        #update ai vision as the enemy moves
        self.vision.center = (self.rect.centerx + (75 * self.direction), self.rect.centery)
      else:
        self.movement_counter -= 1
        if self.movement_counter <= 0:
            self.moving = True

  def update(self):
    self.enemy_movement()
    if self.shoot_cooldown > 0:
      self.shoot_cooldown -= 1
    
  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

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
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

# blue print for all pick_ups
class Pick_up(pygame.sprite.Sprite):
  def __init__(self,pos,size):
    super().__init__()
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect(topleft = (pos[0],pos[1] + 30))
    self.image.fill('green')
  
  def pick_up_collesion(self):
    group = pygame.sprite.spritecollide(level.player, level.pick_ups_group, False)
    for pick_up in group:
        
      level.player.health = level.player.health + 10
      if level.player.health > level.player.max_health:
          level.player.health = level.player.max_health
      pick_up.kill()
  
  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))

  def update(self):
    self.pick_up_collesion()

# a blue print for all bullets
class Bullet(pygame.sprite.Sprite):
    
  def __init__(self, x, y, size, direction):
    pygame.sprite.Sprite.__init__(self)
    self.speed = 10
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect()
    self.image.fill('red')
    self.direction = direction
    self.rect.center = (x, y)

  def draw(self,screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))
  
  def update(self, camera_pos: pygame.math.Vector2):
    #move bullet
    self.rect.x += (self.direction * self.speed)
    #check if bullet has gone off screen
    if self.rect.right < camera_pos.x or self.rect.left > camera_pos.x + screen_width:
        self.kill()
    #check for collision with level
    for tile in level.tiles_group.sprites():
        if tile.rect.colliderect(self.rect):
            self.kill()
    #check collision with characters
    if pygame.sprite.spritecollide(level.player, level.bullets_group, False):
      level.player.health -= 5
      self.kill()
    
# displaying a health bar
class HealthBar():
  def __init__(self, x, y, health, max_health):
    self.x = x
    self.y = y
    self.health = health
    self.max_health = max_health

  def draw(self, health):
    #update with new health
    self.health = health
    #calculate health ratio
    ratio = self.health / self.max_health
    pygame.draw.rect(screen, 'BLACK', (self.x - 2, self.y - 2, 154, 24))
    pygame.draw.rect(screen, 'RED', (self.x, self.y, 150, 20))
    pygame.draw.rect(screen, 'GREEN', (self.x, self.y, 150 * ratio, 20))

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