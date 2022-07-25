import pygame
from laser import laser

class player(pygame.sprite.Sprite): #When drawing the player remember to draw it 30.30 pix

    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('Graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

        self.pl_music = pygame.mixer.Sound('Graphics/veryopandstronglaserbeamthatsoundlikeagun.mp3')
        self.pl_music.set_volume(0.55)
        
        self.laser = pygame.sprite.Group()

    def get_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.laser.add(laser(self.rect.center, -8, self.rect.bottom))
        self.pl_music.play()

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.laser.update()