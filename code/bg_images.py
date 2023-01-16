import pygame 

class background(pygame.sprite.Sprite):
  
  def __init__(self, surface):
    super().__init__()
    self.bg_images = []
    self.surface = surface
 
  bg1_img = pygame.image.load('./graphics/background/background0.png').convert_alpha()
  bg2_img = pygame.image.load('./graphics/background/background1.png').convert_alpha()
  mountain_img = pygame.image.load('./graphics/background/background2.png').convert_alpha()
  sky_img = pygame.image.load('./graphics/background/background3.png').convert_alpha()  
  
  def import_images(self):
    for i in range(4):
      bg_image = pygame.image.load(f"././graphics/background/background{i}.png").convert_alpha()
      self.width = bg_image.get_width()
      self.bg_images.append(bg_image)
        
      
  
  
  def draw_bg(self, scroll):
    for x in range(5): 
      speed = 1
      for i in self.bg_images:
        self.surface.blit(i, ((x * self.width) - (scroll * speed), 0))
        speed += 3
    
    
    


  