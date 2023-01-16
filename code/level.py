import pygame
from support import *
from settings import tile_size
import random
from enemies import *
from tiles import Tile, StaticTile, Animated_tile, coins, potions, diamonds
from settings import screen_width
from player import Player

# main game level, constain all of of the features in the final game. 
# initialieses instances of all other classes, used to check for interactions between all elements.
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
            # targets a specific sprite
            tile_surface = terrain_tile_list[int(val)]
            # determines the kind of sprite is should be
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
            sprite = troll_enemies(x, y, 1, './graphics/Troll_animations')

          if type == 'enemies' and val == '1':
            sprite = mech_enemies(x, y, 2, './graphics/Enemy_Animations')

          if type == 'constraints':
            sprite = Tile(tile_size, tile_size, x ,y)
          
          sprite_group.add(sprite)
    # returns the sprite ground
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


