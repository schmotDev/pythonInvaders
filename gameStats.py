import json

class GameStats:

    def __init__(self, ai_game):
        self.config = ai_game.config
        self.reset_stats()

        self.game_active = False

        self.high_score = 0
        
        try:
            with open('save.json') as f:
                saved_data = json.load(f)
            hs = saved_data['highscore']['high']
        except:
            print("pas de fichier de sauvegarde")
        else:
            self.high_score = hs
        

# rien ici
    def reset_stats(self):
        self.ships_left = self.config.ship_limit
        self.score = 0
        self.level = 1

        