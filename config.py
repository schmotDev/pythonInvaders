import pygame

class Config:

    def __init__(self):

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 236)

        self.ship_speed = 1.5
        self.ship_limit = 3
        self.bullet_limit = 8

        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1

        self.score_scale = 1.5

        self.init_dynamic_settings()
    


    def init_dynamic_settings(self):
        self.alien_speed = 1.0
        self.fleet_direction = 1

        self.alien_points = 50


    def increase_speed(self):
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)









