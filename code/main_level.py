import pygame, sys
from settings import *
from level import Level
from game_data import level_0
from button import Button
#Pygame setp
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0,screen)

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
control_button = Button(300, 375, control, 2, screen_width, control_pressed, '')

back_button = Button( 50, 50, back, 2, screen_width, back_pressed, 'back')
# declaring font styples
font = pygame.font.SysFont('equipmentpro', 120, italic = False)
colour = '#554111'

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

def draw_text (text, font, colour, x, y):
  img = font.render(text, True, colour)
  screen.blit(img, (x, y))

while True:
  
  for event in pygame.event.get():
    screen.fill('black')
    if event.type == pygame.QUIT: 
      pygame.quit()
      sys.exit()
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE and start == True:
        menu = 'paused'

  #if level.player.health == 0:
  #  level = Level(level_0,screen)
  
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
  
  if menu == 'controls':
      screen.blit(pause_img, (0, 0))
      draw_text('Controls', font, colour, 400, 150)
      if back_button.draw(screen):
        if main_menu == True:
          menu = 'main'
        else:
          menu = 'paused'
  pygame.display.update()
  clock.tick(60)
