import pygame, sys, Obstacles
from player import player
from Alien import alien, extra
from random import choice, randint
from laser import laser

class game:
    def __init__(self):
        #player's setup
        player_sprite = player((screen_width / 2 , screen_height), screen_width , 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #obstacles' setup
        self.shape = Obstacles.shape
        self.block_size = 5
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_position = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_position, x_start = screen_width / 15, y_start = 480)

        #alien's setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        #Extra's setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        #Health & score setup
        self.lives = 3
        self.live_surf = pygame.image.load('Graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('Graphics/prstart.ttf', 20)

        # Audio's setup

        music = pygame.mixer.Sound('Graphics/2019-12-11_-_Retro_Platforming_-_David_Fesliyan.mp3')
        music.set_volume(0.6)
        music.play(loops = -1)

        self.exS = pygame.mixer.Sound('Graphics/verycoolandopbeatupexplosionsound.wav')
        self.exS.set_volume(0.11)

        
        self.pl_music = pygame.mixer.Sound('Graphics/veryopandstronglaserbeamthatsoundlikeagun.mp3')
        self.pl_music.set_volume(0.55)
    
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Obstacles.Block(self.block_size, (241,79,80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset,  x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x )

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:    alien_sprite = alien('yellow',x,y)

                elif 1 <= row_index <= 2:   alien_sprite = alien('green', x,y)

                else: alien_sprite = alien('red',x,y)

                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()

        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)

            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.pl_music.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1

        if self.extra_spawn_time <= 0:
            self.extra.add(extra(choice(['right', 'left']),screen_width))
            self.extra_spawn_time = randint(400, 800)

    def check_collision(self):

        #player's lasers
        if self.player.sprite.laser:
            for laser in self.player.sprite.laser:
                #obstacles' collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                    self.exS.play()

                #aliens' collision
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)

                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.exS.play()

                #extra's collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()
                    self.score += 500
                    self.exS.play()

                if pygame.sprite.spritecollide(laser, self.alien_lasers, True):
                    laser.kill()
                    self.exS.play()

        #aliens' laser

        if self.alien_lasers:
            for laser in self.alien_lasers:

                #obstacles' collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                    self.exS.play()

                #player's collision
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1

                    if self.lives <= 0:
                        self.exS.play()
                        pygame.quit()
                        sys.exit()

        #aliens

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):

            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))

            screen.blit(self.live_surf, (x,8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (0,0))
        screen.blit(score_surf, score_rect)

    def victory_screen(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won!', False, 'white')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self):

        #Update
        self.player.update()
        self.alien_lasers.update()
        self.aliens.update(self.alien_direction)
        self.extra.update()

        self.alien_position_checker()
        self.extra_alien_timer()
        self.check_collision()

        #Player's
        self.player.sprite.laser.draw(screen)
        self.player.draw(screen)

        #Block's
        self.blocks.draw(screen)

        #Alien's
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)

        #Score and lives
        self.display_lives()
        self.display_score()
        self.victory_screen()

class CRT(game):
    def __init__(self):
        self.tv = pygame.image.load('Graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)

        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))

if __name__ == '__main__':
    pygame.init()

    screen_width = 600
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    caption = pygame.display.set_caption('Space Invader')
    icon = pygame.image.load('Graphics/SI_icon.ico')
    setIcon = pygame.display.set_icon(icon)

    game = game()
    crt = CRT()

    alienlaser = pygame.USEREVENT + 1
    pygame.time.set_timer(alienlaser, 800)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == alienlaser:
                game.alien_shoot()

        screen.fill((30,30,30))

        game.run()
        crt.draw()

        pygame.display.flip()

        clock.tick(60)