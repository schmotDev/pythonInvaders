from lib2to3.pygram import python_grammar_no_print_statement
import sys
import pygame
from config import Config
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:

    def __init__(self):
        pygame.init()

        self.config = Config()
        self.screen=pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        self.screen_full = False

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        

    def run_game(self):

        while True:

            self._check_events()
            self.ship.update()
            self._update_bullets()

            self._update_screen()


    def _check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_TAB:
            self._change_screen()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _change_screen(self):
        if self.screen_full:
            self.screen=pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
            self.ship.screen_rect = self.screen.get_rect()
            self.screen_full = False
        else:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.ship.screen_rect = self.screen.get_rect()
            self.screen_full = True


    def _fire_bullet(self):
        if len(self.bullets) < self.ship.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    
    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        max_aliens_in_row = (self.config.screen_width-2*alien_width)//(2*alien_width)
        aliens_row = 5

        for row_number in range (aliens_row):
            for alien_number in range (max_aliens_in_row):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2*alien.rect.height*row_number

        self.aliens.add(alien)


    def _update_screen(self):
        self.screen.fill(self.config.bg_color)
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

            
        # on dessine le tout
        pygame.display.flip()


if __name__=='__main__':
    ai=AlienInvasion()
    ai.run_game()
