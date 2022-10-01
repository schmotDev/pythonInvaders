from lib2to3.pygram import python_grammar_no_print_statement
import sys
import pygame
from time import sleep

from config import Config
from gameStats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:

    def __init__(self):
        pygame.init()

        self.config = Config()
        self.screen=pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        self.screen_full = False

        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")




    def run_game(self):

        while True:

            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            

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


    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)



    def _fire_bullet(self):
        if self.stats.game_active:
            if len(self.bullets) < self.ship.bullet_limit:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)


    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    
    def _check_bullet_alien_collision(self):

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    
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


    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()



    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

        
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += alien.drop_speed
            alien.fleet_direction *= -1


    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)





    def _update_screen(self):
        self.screen.fill(self.config.bg_color)
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        if not self.stats.game_active:
            self.play_button.draw_button()


        # on dessine le tout
        pygame.display.flip()


if __name__=='__main__':
    ai=AlienInvasion()
    ai.run_game()
