class GameStats:

    def __init__(self, ai_game):
        self.config = ai_game.config
        self.reset_stats()

        self.game_active = False
        

# rien ici
    def reset_stats(self):
        self.ships_left = self.config.ship_limit

        