import sys 
import pygame 
 
from settings import Settings
from ship import Ship
from bullet import Bullet
class AlienInvasion:
    "Overall class to mange game assets and behaviour"

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen= pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))

        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # Set the background color. 
        self.bg_color = (230,230,230)

    def run_game(self):
        "Start the main loop for the game"
        while True:
            # watch for keyboard and mouse events. 
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_events()

    def _check_events(self):
        # respond to keypresses and mouse events 
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
            
    def _check_keydown_events(self,event):
        # respond to keypresses and mouse events 
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        # respond to keyreleases 
        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            
            self.ship.moving_down = False
        
    
    def _fire_bullet(self):
        # Create a new bullet and add it to the bullets group 
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_events(self):
        #update images on the screen, and fllip to the new screen 
        #redraw the screen during each pass through the loop 
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # Make the most recently drawn screen visible. 
            pygame.display.flip()
    
    def _update_bullets(self):
        #update bullet position 
        self.bullets.update()
        #get rid of bullets that have disappeared 
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

if __name__ == '__main__':
    #make a game instance, and run the game. 
    ai = AlienInvasion()
    ai.run_game()
