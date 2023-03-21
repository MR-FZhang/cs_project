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
    self.jump_speed = - 29
    self.health = 999999999999999999
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

  
