import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, ai_game):
        
        super().__init__()

        self.screen = ai_game.screen
        #self.config = ai_game.config

        self.speed = 1.0
        self.width = 3
        self.height = 15
        self.color = (60, 60, 60)

        self.rect = pygame.Rect(0,0, self.width, self.height)

        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)


    def update(self):
        self.y -= self.speed
        self.rect.y = self.y


    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)




