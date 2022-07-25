import pygame

class alien(pygame.sprite.Sprite): #When drawing the alien remember to draw it 28.28 pix
    def __init__(self, color, x, y):
        super().__init__()
        file_path = 'Graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        else: self.value = 300

    def update(self, direction):
        self.rect.x += direction

class extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('Graphics/ES.png').convert_alpha()

        if side == 'right':
            x = screen_width + 50
            self.speed = -3

        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x, 50))

    def update(self):
        self.rect.x += self.speed