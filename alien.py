import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self,ai_game):

        super().__init__()
        self.screen = ai_game.screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        self.speed = 1.0
        self.drop_speed = 10
        self.fleet_direction = 1

    
    def update(self):
        self.x += self.speed*self.fleet_direction
        self.rect.x = self.x

    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True




