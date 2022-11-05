class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, pos, size, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (pos[0],pos[1] + 30))
        self.image.fill('red')
        self.rect.center = (pos)
        self.direction = direction

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        #check for collision with level
        for tile in level.tiles:
            if tile.colliderect(self.rect):
                self.kill()

        #check collision with characters
        if pygame.sprite.spritecollide(level.player, level.enemies.bullet_group, False):
          level.player.health -= 5
          self.kill()

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
    def shoot(self):
      bullet = Bullet((self.rect.centerx,self.rect.centery), 5, self.direction)  