class Settings :
    """A class to store all settings for Alien Invasion
    """

    def __init__(self):
        #initilaize the game's settings.
        # Screen settings 
        self.screen_width = 1200 
        self.screen_height = 800 
        self.bg_color = (230,230,230)
        #ship settings 
        self.ship_speed = 6.0
        self.ship_limit = 3 
        # bullet settings 
        self.bullet_speed = 15.0
        self.bullet_width = 1 
        self.bullet_height = 5
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        #alien settings 
        self.alien_speed = 2.0 
        #fleet direction 
        self.fleet_drop_speed = 10 
        self.fleet_direction = 1 
