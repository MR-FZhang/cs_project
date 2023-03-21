import pygame, sys
from settings import *
from level import Level
from game_data import level_0
from button import Button
from support import *
from settings import tile_size
import random
from enemies import *
from tiles import Tile, StaticTile, Animated_tile, coins, potions, diamonds
from settings import screen_width
from player import Player
#Pygame setp
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0,screen)

level_1 = {
          'bg_trees':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_Bg_trees.csv',
          'terrain':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_terrain.csv',
          'bridges':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_bridge.csv',
          'teasures':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_coin.csv',
          'potions':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_potion.csv',
          'enemies':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_enemies.csv',
          'constraints':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_constraints.csv',
          'flags':'/Users/fuchunzhang/Documents/cs_project/levels/0/level 0_flags.csv'
          }

level_0 = {
          'bg_trees':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_Bg_layout.csv',
          'terrain':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_Terrain_layout.csv',
          'bridges':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_Bridge_layout.csv',
          'teasures':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_coin_layout.csv',
          'potions':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_Potion_layout.csv',
          'enemies':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_Enemy_layout.csv',
          'constraints':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_Constraints_layout.csv',
          'flags':'/Users/fuchunzhang/Documents/cs_project/levels/0/test0_Flag_layout.csv'
          }

vertical_tile_numeber = 22
tile_size = 32

screen_height = vertical_tile_numeber * tile_size
screen_width = 1200
# button images
start_img = pygame.image.load('./graphics/green buttons/purple.png').convert_alpha()

option_img = pygame.image.load('./graphics/green buttons/options.png').convert_alpha()

exit_img = pygame.image.load('./graphics/green buttons/exit.png').convert_alpha()
# pause button images
resume = pygame.image.load('./graphics/green buttons/resume.png').convert_alpha()

audio = pygame.image.load('./graphics/green buttons/audio.png').convert_alpha()

control = pygame.image.load('./graphics/green buttons/controls.png').convert_alpha()

home = pygame.image.load('./graphics/green buttons/home.png').convert_alpha()

quit = pygame.image.load('./graphics/green buttons/quit.png').convert_alpha()

back = pygame.image.load('./graphics/green buttons/back.png').convert_alpha()
# pause pressed
resume_pressed = pygame.image.load('./graphics/green buttons/resume_pressed.png').convert_alpha()

audio_pressed = pygame.image.load('./graphics/green buttons/audio_pressed.png').convert_alpha()

control_pressed = pygame.image.load('./graphics/green buttons/controls_pressed.png').convert_alpha()

home_pressed = pygame.image.load('./graphics/green buttons/home_pressed.png').convert_alpha()

quit_pressed = pygame.image.load('./graphics/green buttons/quit_pressed.png').convert_alpha()

back_pressed = pygame.image.load('./graphics/green buttons/back_pressed.png').convert_alpha()
# button pressed images
start_pressed = pygame.image.load('./graphics/green buttons/purple_pressed.png').convert_alpha()

option_pressed = pygame.image.load('./graphics/green buttons/options_pressed.png').convert_alpha()

exit_pressed = pygame.image.load('./graphics/green buttons/exit_pressed.png').convert_alpha()
# button initialisations
start_button = Button( 300, 300,start_img, 2.5, screen_width, start_pressed, '')

option_button = Button(300, 420, option_img, 2.76, screen_width, option_pressed, '')

exit_button = Button(300, 500,exit_img, 2.76, screen_width, exit_pressed, '')
# pause button initialisations
resume_button = Button( 300, 300,resume, 2, screen_width, resume_pressed, '')

home_button = Button(300, 450,home, 2, screen_width, home_pressed, '')

quit_button = Button(300, 525, quit, 2, screen_width, quit_pressed, '')

death_home_button = Button(300, 505, home, 2, screen_width, home_pressed,'')

death_quit_button = Button(300, 575, quit, 2, screen_width, quit_pressed,'')

control_button = Button(300, 375, control, 2, screen_width, control_pressed, '')

back_button = Button( 50, 50, back, 2, screen_width, back_pressed, 'back')
# declaring font styples
saturday_detention = pygame.image.load('./graphics/Saturday_detention.png')

menu_img = pygame.image.load('./graphics/Grassy_Mountains_preview_fullcolor.png').convert_alpha()

pause_img = pygame.image.load('./graphics/background/background0.png').convert_alpha()

width = menu_img.get_width()
height = menu_img.get_height()

enlarged_image = pygame.transform.scale(menu_img, (int(width * 3.25), int(height * 3.3)))
menu = 'main'
start = False
main_menu = False
pause_menu = False
background_music = pygame.mixer.Sound('./audio/overworld_music.wav')
#game_music = pygame.mixer.Sound('./audio/overworld_music.wav')

font = pygame.font.SysFont('equipmentpro', 120, italic = False)
instruct_font = pygame.font.SysFont('expressionpro', 70, italic = False)
instruct_colour = '#FFFFFF'
colour = '#554111'
def draw_text (text, font, colour, x, y):
  img = font.render(text, True, colour)
  screen.blit(img, (x, y))

class Level:
  def __init__(self, level_data, surface):
    # sound effects

    # general setup
    self.display_surface = surface
    # player setup
    self.player_group = pygame.sprite.GroupSingle()
    player_setup = import_csv_layout(level_data['flags'])
    self.player_setup(player_setup)
    self.current_x = 0
    self.collided = False
    # goal set up
    self.goal_group = pygame.sprite.GroupSingle()
    # attributes to determine the posittions of the camera and boundery conditions
    self.screen_bond = 200
    self.camera_pos = pygame.math.Vector2(0, 0)
    self.screen_bond_height = 25 
    # determines positions to where the images should be blitted on to the screen
    self.bg_scroll = 0
    #back ground image set up
    self.bg1_img = pygame.image.load('./graphics/background/background0.png').convert_alpha()
    
    self.bg2_img = pygame.image.load('./graphics/background/background1.png').convert_alpha()
    
    self.mountain_img = pygame.image.load('./graphics/background/background2.png').convert_alpha()
    
    self.sky_img = pygame.image.load('./graphics/background/background3.png').convert_alpha() 
    # terrain setup
    terrain_layout = import_csv_layout(level_data['terrain'])
    self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

    # bridge setup
    bridges_layout = import_csv_layout(level_data['bridges'])
    self.bridges_sprites = self.create_tile_group(bridges_layout, 'bridges')
    
    # bg_trees setup
    bg_trees_layout = import_csv_layout(level_data['bg_trees'])
    self.bg_trees_sprites = self.create_tile_group(bg_trees_layout, 'bg_trees')
    
    # teasures setup
    teasures = import_csv_layout(level_data['teasures'])
    self.teasures_sprites = self.create_tile_group(teasures, 'teasures')

    #potions setup
    potions = import_csv_layout(level_data['potions'])
    self.potions_sprites = self.create_tile_group(potions, 'potions')

    # enemies setup 
    enemies = import_csv_layout(level_data['enemies'])
    self.enemies_sprites = self.create_tile_group(enemies, 'enemies')

    # enemies bounderies setup
    constraint_layout = import_csv_layout(level_data['constraints'])
    self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
    
    # determines objects that the player can collide with
    self.pick_up = Pick_up(self.player, self.potions_sprites, self.teasures_sprites)
    
  # iterates through a CSV file for a game setup to determine the postions for drawing an sprite on the screen.
  def create_tile_group(self,layout, type):
    # when ever the functions is called, a sprite group is established to contain sprites
    sprite_group = pygame.sprite.Group()
    # loops through a fill and determine the value that is contained in a cell of a CSV
    for row_index, row in enumerate(layout):
      for col_index, val in enumerate(row):
        if val != '-1' : 
          x,y = col_index * tile_size, row_index * tile_size
          # values allows the game to identify which elements should be created fro each value 
          if type == 'terrain':
            # gets a list of slices graphics for a passed in spritesheet
            terrain_tile_list = import_cut_graph('./graphics/terrain/terrain_layout.png', tile_size, tile_size)
            tile_surface = terrain_tile_list[int(val)]
            sprite = StaticTile(tile_size, tile_size, x, y, tile_surface)

          if type == 'bridges':
            bridges_tile_list = import_cut_graph('./graphics/terrain/bridges.png', tile_size, tile_size)
            tile_surface = bridges_tile_list[int(val)]
            sprite = StaticTile(tile_size, tile_size, x, y, tile_surface)
            
          if type == 'bg_trees':
            bg_trees_tile_list = import_cut_graph('./graphics/terrain/bg_layout.png', tile_size, tile_size)
            tile_surface = bg_trees_tile_list[int(val)]
            sprite = StaticTile(tile_size, tile_size, x, y, tile_surface)

          if type == 'teasures' and val == '0':
            sprite = coins(16, 16, x, y, './graphics/coins')
      
          if type == 'teasures' and val == '1':
            sprite = diamonds(16, 16, x, y, './graphics/diamonds')          
           
          if type == 'potions':
            sprite = potions(39, 51, x, y, './graphics/potions')      
        
          if type == 'enemies' and val == '0':
            sprite = troll_enemies(x, y, 2.5, './graphics/Troll_animations')

          if type == 'enemies' and val == '1':
            sprite = mech_enemies(x, y, 2.5, './graphics/Enemy_Animations')

          if type == 'constraints':
            sprite = Tile(tile_size, tile_size, x ,y)
          
          sprite_group.add(sprite)
    return sprite_group
  
  # allws the enemy to move in a specified boundary
  def enemy_collisions(self):
    # loops through eaach enemy in the enemy group
    for enemy in self.enemies_sprites:
      # identifies the kind of enemy
      if enemy.enemy == 'troll':
        troll  = enemy
        for sprite in self.constraint_sprites.sprites():
          
          # checks for coliision with the boundaries
          if sprite.rect.colliderect(troll.rect):
            # determines the direction of the enemy, to decide which way the enemy should turn
            if troll.direction < 0: 
              troll.rect.left = sprite.rect.right + 30
            
            elif troll.direction > 0:
              troll.rect.right = sprite.rect.left - 30
            # reverses the enemy directions
            troll.reverse()
      
      if enemy.enemy == 'mech':
        mech = enemy

        for sprite in self.constraint_sprites.sprites():
        
          if sprite.rect.colliderect(mech.rect):
            if mech.direction < 0: 
              mech.rect.left = sprite.rect.right + 30

            elif mech.direction > 0:
              mech.rect.right = sprite.rect.left - 30

            mech.reverse() 
  
  # defines how to enemy will move 
  def enemy_movement(self):

    for enemy in self.enemies_sprites: 
      # checks whether the enemy is dead
      if  enemy.status != 'death':
        # determines how long the enemy will wait before is starts to attack
        if enemy.moving == False and random.randint(1, 250) == 1:
          enemy.status = 'idle'
          enemy.movement_counter = 50
        #check if the ai in near the player
        if enemy.vision.colliderect(self.player.rect):
          #stop running and face the player
          enemy.moving = False
          #shoot
          if self.player.status != 'death':
            enemy.attack()
        else:
          if enemy.moving == True:
            enemy.move()
          #update ai vision as the enemy moves
          else:
            enemy.movement_counter -= 1
            if enemy.movement_counter <= 0:
                enemy.moving = True
      else:
          self.direction = 0
          self.speed = 0
  # separate function to determine the start and end locations of player
  def player_setup (self,layout):
    
    for row_index, row in enumerate(layout):
      for col_index, val in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size
        
        if val == '0' :
          sprite = Player((x, y), 80, self.display_surface)
          self.player_group.add(sprite)
          self.player = self.player_group.sprite
          
          self.initial_pos = (x, y)
        if val == '1' :
          sprite = Animated_tile(16, 16, x, y, './graphics/flag')
          self.goal_group.add(sprite)
          self.goal = self.goal_group.sprite
  # function to draw the background for the player
  def draw_bg(self):
   
    for x in range(5):
        # draws the background repeadedly 5 times
        # to make to paralax effect the images are needed to be blited at differing locations at different location

        width = self.sky_img.get_width()   
        self.display_surface.blit(self.bg1_img, (((x * width) - self.bg_scroll * 0.5  ), 0))
        self.display_surface.blit(self.bg2_img, (((x * width) - self.bg_scroll * 0.6 ) , 0))
        self.display_surface.blit(self.mountain_img, (((x * width) - self.bg_scroll * 0.7 ), 0))
        self.display_surface.blit(self.sky_img, (((x * width) - self.bg_scroll * 0.8 ), 0))

  # determines the horizontal collision of the player 
  def x_collision(self):
    # determine sthe objects that can collide with the player
    collidables = self.terrain_sprites.sprites() + self.bridges_sprites.sprites()  
    
    player = self.player
    
    # movement of the player
    player.rect.x += player.direction.x * player.speed
    if player.health <=0 and self.player.on_ground == True:
      player.speed = 0
      player.direction.x = 0
      player.status = 'death'

    if player.direction.x > 0:
      player.health -= 1
    
    # restircts the player movement, when it reaches the end of the screen
    if player.rect.x <= 25 or player.rect.x > 117 * tile_size:
      player.rect.x -= player.direction.x * player.speed
    
    # set the player position to the starting location
    if player.rect.y > screen_height:
      player.on_ground = True
      player.health = 0
      player.status = 'death'

    for sprite in collidables:
      
      if sprite.rect.colliderect(player.rect):
        if player.direction.x < 0: 
          player.rect.left = sprite.rect.right
          player.on_left = True
          self.current_x = player.rect.left
          self.collided = True
        
        elif player.direction.x > 0:
          player.rect.right = sprite.rect.left
          player.on_right = True
          self.current_x = player.rect.right
          self.collided = True

    if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
      player.on_left = False
      self.collided = False
    
    if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
      player.on_right = False
      self.collided = False
    # the sequence of the prrogramme determines the order of excution, therefore it is vital to place variables in the correct order
    if (player.rect.right > self.camera_pos.x + screen_width - 200 and self.bg_scroll < (120 * tile_size) \
      - screen_width) or (player.rect.x < self.camera_pos.x + 220 and self.bg_scroll > abs(player.speed)):
      
      if player.speed > 0 and player.direction.x > 0 and not self.collided:
        self.bg_scroll += player.speed

      elif player.direction.x < 0 and player.rect.x < self.camera_pos.x + 215 and not self.collided:
        self.bg_scroll -= player.speed
        
      else:
        self.bg_scroll += 0
  
  def y_collision(self):
    
    player = self.player
    player.apply_gravity()
    collidables = self.terrain_sprites.sprites() + self.bridges_sprites.sprites() 
    
    for sprite in collidables:
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

  def camera_update(self):
    if self.player.rect.left < self.camera_pos.x + self.screen_bond:
      self.camera_pos.x = self.player.rect.left - self.screen_bond
      self.player.scroll = self.player.speed
    if self.player.rect.right > self.camera_pos.x + screen_width - self.screen_bond:
      self.camera_pos.x = self.player.rect.right - screen_width + self.screen_bond
      self.player.scroll = -self.player.speed
    
    # When the player's y is smaller than 0 but is falling, there would be an error if you set the camera to position to 0
    # because there is a gap for the player to travel before it can reach 0, so glitches would be seen
    if self.player.rect.top < self.camera_pos.y:
      self.camera_pos.y = self.player.rect.top 
      
    elif self.player.rect.top < 0 and self.player.rect.top > self.camera_pos.y :
      self.camera_pos.y = self.player.rect.top
      
    elif self.player.rect.top >= 0:
      self.camera_pos.y = 0
      
  
  def run(self):
    
    # background initialisation
    self.draw_bg()
    self.camera_update()
    print(self.player.status)
    # diplaying the bg_trees
    for bg_trees in self.bg_trees_sprites:
      bg_trees.draw(self.display_surface, self.camera_pos)
    
    # run the entire game/level
    for terrain_sprite in self.terrain_sprites:
      terrain_sprite.draw(self.display_surface, self.camera_pos)
    
    # displaying bridge tiles
    for bridge_sprite in self.bridges_sprites:
      bridge_sprite.draw(self.display_surface, self.camera_pos)

    # displaying the teasures
    for teasure_sprite in self.teasures_sprites:
      teasure_sprite.draw(self.display_surface, self.camera_pos)
    self.teasures_sprites.update()

    # displaying the potions
    for potion_sprite in self.potions_sprites:
      potion_sprite.draw(self.display_surface, self.camera_pos)
    self.potions_sprites.update()

    self.pick_up.update()

    if self.player.status != 'death':
      self.player.update()
      self.y_collision()
      self.x_collision()
      self.player.attack(self.display_surface, self.enemies_sprites)
      self.player.draw(self.display_surface, self.camera_pos)
    
    if self.player.status == 'death' and not self.player.on_ground:
      self.player.update()
      self.y_collision()
      self.x_collision()
      self.player.draw(self.display_surface, self.camera_pos)

    if self.player.status == 'death':
      self.player.death_animations(self.initial_pos)
    
      self.player.draw(self.display_surface, self.camera_pos)
    
    self.health_bar = HealthBar(35, 50, self.player.health, self.player.max_health, self.display_surface)

    self.health_bar.draw(self.player.health)

    # displayingt the enemies
    self.constraint_sprites.update()

    #updating and drawing the enemies
    for enemy_sprite in self.enemies_sprites:
      
      if enemy_sprite.status != 'death':
          enemy_sprite.get_visions()
          enemy_sprite.attack_action(self.player)
          self.enemies_sprites.update()
          self.enemy_movement()
          self.enemy_collisions()
          enemy_sprite.draw(self.display_surface, self.camera_pos)
          
      if enemy_sprite.status == 'death':
          enemy_sprite.death_animations()
          enemy_sprite.draw(self.display_surface, self.camera_pos)

class Pick_up(pygame.sprite.Sprite):
      
      def __init__(self, player, pick_up_grp, coin_pick_up):
        super().__init__()
        self.player = player
        self.health_pick_up_grp = pick_up_grp
        self.coin_pick_up_grp = coin_pick_up

        self.coin_sound = pygame.mixer.Sound('./audio/coin.wav')
        self.potion_sound = pygame.mixer.Sound('./audio/potions.wav')
      
      def health_pick_up_collesion(self):
        
        group = pygame.sprite.spritecollide(self.player, self.health_pick_up_grp, True)
        if group:  
          self.potion_sound.play()
          for pick_up in group:
              self.player.score += 50
              self.player.health += 50
              if self.player.health > self.player.max_health:
                  self.player.max_health = self.player.max_health
 
      def coin_pick_up_collision(self):
        treasure_group = pygame.sprite.spritecollide(self.player, self.coin_pick_up_grp, True)

        if treasure_group:
          self.coin_sound.play()
          for pick_up in treasure_group:

              if pick_up.object == 'coins':
                self.player.coins += 1
                self.player.score += 120

              if pick_up.object == 'diamonds':
                self.player.diamonds += 1
                self.player.score += 150

      def update(self):
        self.health_pick_up_collesion()
        self.coin_pick_up_collision()

class HealthBar(pygame.sprite.Sprite):
    
    def __init__(self, x, y, health, max_health, screen):
      self.x = x
      self.y = y
      self.health = health
      self.max_health = max_health
      self.screen = screen
    
    def draw(self, health):
      #update with new health
      self.health = health
      #calculate health ratio
      ratio = self.health / self.max_health
      pygame.draw.rect(self.screen, 'BLACK', (self.x - 2, self.y - 2, 154, 24))
      pygame.draw.rect(self.screen, 'RED', (self.x, self.y, 150, 20))
      pygame.draw.rect(self.screen, 'GREEN', (self.x, self.y, 150 * ratio, 20))

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

import pygame
from import_spritesheet import Spritesheet

# defines player characteristics and its methods
class Player(pygame.sprite.Sprite):
  def __init__(self,pos, size, surface):
    super().__init__()
    self.display_surface = surface
    self.image = pygame.Surface((size,size))
    self.rect = self.image.get_rect(topleft = pos)
    self.speed = 12
    self.direction = pygame.math.Vector2(0,0)
    self.gravity = 1.6
    self.jump_speed = -21
    self.health = 999999
    self.max_health = self.health
    self.frame_index = 0
    self.frame_time = 0.4
    self.status = 'idle'
    self.on_left = False
    self.on_right = False
    self.on_ground = False
    self.on_ceiling =False
    self.facing_right = False
    self.scroll = 0
    self.collide = False
    self.width = 0
    self.height = 0
    self.attacking = False
    self.attack_cooldown = 0
    self.coins = 0
    self.diamonds = 0
    self.score = 0
    self.jumping_sound = pygame.mixer.Sound('./audio/Jump_copy.wav')
    self.attacking_sound = pygame.mixer.Sound('./audio/player_attack.wav')
    
  # gets the current animation to be displayed
  def animation_actions(self, action):
    
    player_actions = {'idle':[],'run':[],'jump':[],'fall':[],'attack':[], 'death':[]}
    sprite_sheet = Spritesheet('./graphics/Animation')
    sprite_sheet_1 = Spritesheet('./graphics/Animation1')
    player_actions['idle'] = sprite_sheet.get_spritelist('Idle', 10)
    player_actions['run'] = sprite_sheet.get_spritelist('Run', 10)
    player_actions['jump'] = sprite_sheet.get_spritelist('Jump', 3)
    player_actions['attack'] = sprite_sheet.get_spritelist('Attack', 4)
    player_actions['fall'] = sprite_sheet.get_spritelist('Fall', 3)
    player_actions['death'] = sprite_sheet.get_spritelist('Death', 10)
    return player_actions[action]
 
  def animations(self):
    self.frame_index += self.frame_time
    self.animations_list = self.animation_actions(self.status)
   
    if self.frame_index >= len(self.animations_list):
      self.frame_index = 0

    image = self.animations_list[int(self.frame_index)]

    if self.facing_right:
      self.image = image
      self.width = image.get_width()
      self.height = image.get_height()
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

  def attack(self, surface, enemy_sprites):
    
    if self.attacking == True and self.attack_cooldown <= 0:
      #(self.attacking)
      if self.facing_right == True:
        self.attacking_sound.play() 
        attacking_rect = pygame.Rect(self.rect.centerx , self.rect.y, self.rect.width / 2 , self.rect.height)  
        #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
 
        self.attaking = False
        #(self.attacking)
        self.attack_cooldown = 13
      
      if self.facing_right == False:
        self.attacking_sound.play() 
        attacking_rect = pygame.Rect(self.rect.centerx - self.rect.width / 2, self.rect.y, self.rect.width / 2 , self.rect.height)  
        #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
      
        self.attaking = False
        self.attack_cooldown = 13
      
      for enemy in enemy_sprites:
        if enemy.rect.colliderect(attacking_rect):
          enemy.health -= 50
    
    else :
      self.attack_cooldown -= 1
  
  def display_score(self, x, y):
    font = pygame.font.SysFont('equipmentpro', 35)
    colour = (0, 0, 0)
    img = font.render(f'SCORE:{self.score}', True, colour)
    self.display_surface.blit(img, (x, y))

  def death_animations (self, position):

    if self.status == 'death'and self.on_ground == True:
      self.frame_index += self.frame_time
      self.animations_list = self.animation_actions(self.status)

      if self.frame_index < len(self.animations_list):
        self.image = self.animations_list[int(self.frame_index)]
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
      
      else:
        self.image = self.animations_list[len(self.animations_list) - 1]
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
  
  def get_status(self):
    
      if self.health > 0: 
        if self.direction.y < 0:
          self.status = 'jump'
        elif self.direction.y > 1:
          self.status = 'fall'
        else:
          if self.direction.x != 0:
            self.status = 'run'
          else:
            self.status = 'idle'

      if self.health <= 0 and self.on_ground == True:
        self.status = 'death'

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

    if keys[pygame.K_q] :
      self.status = 'attack'
      if self.attack_cooldown <= 0 and self.attacking == False:
        
        self.attacking = True
      else: 
        self.attacking = False
        self.status = self.status
  # allow user to control player jump 
  def vertical_jump(self):
    self.jumping_sound.play()
    self.direction.y = self.jump_speed
  
  # applies gravity to the player, note adding a float < 1 to rect.x or y does happens
  #this is because it is rounded down to zero.
  def apply_gravity (self):
    
    self.direction.y += self.gravity
    self.rect.y += self.direction.y
    
  def draw(self, screen, camera_pos):
    screen.blit(self.image, (self.rect.x - camera_pos.x, self.rect.y - camera_pos.y))
  
  # Function to update player status  
  def update(self):
    self.display_score(35, 10)
    self.get_status()
    self.player_input()
    self.animations()
    
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
    self.attack_sound = pygame.mixer.Sound('./audio/enemy_attacking.wav')
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
        
      if player.rect.colliderect(attacking_rect) and player.health > 0:
          self.attack_sound.play()
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

import pygame

class Button (pygame.sprite.Sprite):
  def __init__(self, x, y, image, scale, screen_width, pressed, status):
    width = image.get_width()
    height = image.get_height()
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    self.x = (screen_width / 2) - (self.image.get_width() / 2)
    self.y = y
    self.rect = self.image.get_rect(topleft = (self.x, self.y))
    self.back_x = x
    self.status = status
    
    if status == 'back':
      self.rect = self.image.get_rect(topleft = (self.back_x, self.y))
    self.hit = False
    self.scale = scale
    self.start = image
    self.pressed_image = pressed
    self.width = self.pressed_image.get_width()
    self.height = self.pressed_image.get_height()
  
  def key_press_animation(self):
    
    if self.hit:  
      self.image = pygame.transform.scale(self.pressed_image, (int(self.width * self.scale), int(self.height * self.scale)))
    else:
      self.image = pygame.transform.scale(self.start, (int(self.width * self.scale), int(self.height * self.scale)))
    self.rect = self.image.get_rect(topleft = (self.x, self.y))
    if self.status == 'back':
        self.rect = self.image.get_rect(topleft = (self.back_x, self.y))    
  
  def draw(self, screen):
    action = False
    position = pygame.mouse.get_pos()
    
    if self.rect.collidepoint(position):
      if pygame.mouse.get_pressed()[0] == 1 and self.hit == False:
          self.hit = True
          self.key_press_animation()
          action = True
    
    if pygame.mouse.get_pressed()[0] == 0:
      self.hit = False
      self.key_press_animation()
    screen.blit(self.image, (self.rect.x, self.rect.y))
    
    if self.status == 'back':
      self.rect = self.image.get_rect(topleft = (self.back_x, self.y))
    return action

while True:
  
  for event in pygame.event.get():
    screen.fill('black')
    if event.type == pygame.QUIT: 
      pygame.quit()
      sys.exit()
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE and start == True:
        menu = 'paused'

  if level.player.status == 'death' and start == True:
    print('death')
    menu = 'death'

  if start == True:
    #background_music.play()
    level.run()
  


  if start == False and menu == 'main':  
      screen.blit(enlarged_image, (0, 0))
      draw_text('PHANTUM RUNNER', font, colour, 236, 150)
      #level = Level(level_0,screen)
      if start_button.draw(screen):
          start = True
          menu = 'start'
      if option_button.draw(screen):
          menu = 'controls'
          main_menu = True

      if exit_button.draw(screen):
          sys.exit()

  if menu == 'paused':
      screen.blit(pause_img, (0, 0))
      draw_text('PAUSE MENU', font, colour, 345, 150)
      if resume_button.draw(screen):
          start = True
          menu = 'start'
      if control_button.draw(screen):
          menu = 'controls'
          pause_menu = True

      if quit_button.draw(screen):
        sys.exit()
      if home_button.draw(screen):
        menu = 'main'
        start = False
  
  if menu == 'death':
    screen.blit(pause_img, (0, 0))
    screen.blit(saturday_detention, (455, 220))
    draw_text('SATURDAY DETENTION !!', font, colour, 130, 125)
    draw_text('DARIUS NO PROJECT !!!', font, colour, 130, 50)
    if death_home_button.draw(screen):
        level = Level(level_0, screen)
        menu = 'main'
        start = False
    if death_quit_button.draw(screen):
        sys.exit()
  
  if menu == 'controls':
      screen.blit(pause_img, (0, 0))
      draw_text('Controls', font, colour, 400, 150)
      draw_text('PRESS LEFT TO MOVE LEFT ', instruct_font, colour, 150, 300)
      draw_text('PRESS RIGHT TO MOVE RIGHT', instruct_font, colour, 150, 350)
      draw_text('PRESS SAPCE TO JUMP', instruct_font, colour, 150, 400)
      draw_text('PRESS Q TO ATTACK', instruct_font, colour, 150, 450)
      if back_button.draw(screen):
        if main_menu == True:
          menu = 'main'
        else:
          menu = 'paused'
  pygame.display.update()
  clock.tick(60)

# main game level, constain all of of the features in the final game. 
# initialieses instances of all other classes, used to check for interactions between all elements.

  

          