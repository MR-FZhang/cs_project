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
    
