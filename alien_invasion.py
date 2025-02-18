import sys 
from time import sleep 
import pygame 
 
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
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
        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #make the play button 
        self.play_button = Button(self,"Play")
        # Set the background color. 
        self.bg_color = (230,230,230)

    def run_game(self):
        "Start the main loop for the game"
        while True:
            # watch for keyboard and mouse events. 
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_events()

    def _check_events(self):
        # respond to keypresses and mouse events 
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
    
    def _check_play_button(self,mouse_pos):
        #button clicks capture 
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings. 
            self.settings.initialize_dynamic_settings()
            #reset the game statistics 
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            #get rid of any remaining aliens and bullets 
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship 
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

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
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _start_game(self):
        #start game with keydown
        if not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True

            #get rid of any remaining aliens and bullets 
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship 
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

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
            self.aliens.draw(self.screen)

            # Draw the score information.
            self.sb.show_score()

            #draw the play button if the game is inactive 
            if not self.stats.game_active:
                self.play_button.draw_button()
            pygame.display.flip()
    
    def _update_bullets(self):
        #update bullet position 
        self.bullets.update()
        #get rid of bullets that have disappeared 
        
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        #respond to bullet-alien that have collided.
        
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet. 
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase leve. 
            self.stats.level += 1 
            self.sb.prep_level()

    def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the row 
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

        self.aliens.add(alien)
        
    def _create_fleet(self):
        """Create the Fleet of aliens"""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_sapce_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_sapce_x // (2 * alien_width)
        # determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height 
        available_space_y = (self.settings.screen_height -
                        (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create the first row of aliens 
        for row_number in range (number_rows):
            for alien_number in range(number_aliens_x):
                #Create an alien an place it in the row 
                self._create_alien(alien_number,row_number)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self):
        #Update the positions of all aliens in the fleet 
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets.
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

if __name__ == '__main__':
    #make a game instance, and run the game. 
    ai = AlienInvasion()
    ai.run_game()
