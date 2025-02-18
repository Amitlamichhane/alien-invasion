import pygame 
from pygame.sprite import Sprite


class Ship(Sprite):
    "class to manage the ship"

    def __init__(self,ai_game):
        "initialize the ship and set its starting position"
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #load the ship and get is rect. 
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #start each new ship the bottom centre of the screen. 
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        #movement flag 
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left>0 :
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top >0:           
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom  :
            self.y += self.settings.ship_speed
        #ypdate rect obect from self.x 
        self.rect.x = self.x
        self.rect.y = self.y
    
    def blitme(self):
        "draw the ship at its current location "
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        #updating  x and y axis 
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)