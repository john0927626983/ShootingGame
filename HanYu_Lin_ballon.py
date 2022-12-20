import sys
import math
import time
import random
import pygame
from pygame.locals import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BALLONIMAGEWIDTH = 45
BALLONIMAGEHEIGHT = 66
CANNONIMAGEWIDTH = 74
CANNONIMAGEHEIGHT = 9
BULLETIMAGEWIDTH = 17
BULLETIMAGEHEIGHT = 14
FPS = 60

class Ballon(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        # Load image.
        self.raw_image = pygame.image.load('./asserts/Red_Ballon_strip1.png').convert_alpha()
        # Scale image.
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        # Position.
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = width
        self.height = height
        # For ballon animation.
        self.animation_number = 1
        self.explosion_number = 0
        # Moving speed.
        self.speed = 3
    
    def update(self):
        # Animation.
        self.animation_number += 1
        # Load image.
        self.raw_image = pygame.image.load(f"./asserts/Red_Ballon_strip{self.animation_number % 4}.png").convert_alpha()
        # Scale image.
        self.image = pygame.transform.scale(self.raw_image, (BALLONIMAGEWIDTH, BALLONIMAGEHEIGHT))
    
    def explosion_animate(self):
        # Animation.
        self.raw_image = pygame.image.load(f"./asserts/tank_explosion{self.explosion_number % 3}.png").convert_alpha()
        self.explosion_number += 1
        # Scale image.
        self.image = pygame.transform.scale(self.raw_image, (BALLONIMAGEWIDTH, BALLONIMAGEHEIGHT))

    def move(self):
        # Move within boundary.        
        if 60 < self.rect.centery < 500:
            self.rect = self.rect.move(0, self.speed)
        elif self.rect.centery == 500:
            self.rect = self.rect.move(0, -3)
        else:
            self.rect = self.rect.move(0, 3)
    
    def random_direction(self):
        # Move up or down randomly.
        if random.randint(0, 1) == 0:
            self.speed *= 1
        else:
            self.speed *= -1
    
    def isCollision(self, Rect):
        # Collision detect.
        if(pygame.Rect.colliderect(self.rect, Rect)):
            return True
        return False
        
class Cannon(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.raw_image = pygame.image.load('./asserts/tanks_turret4_1.png').convert_alpha()
        # Scale image.
        self.image_original = pygame.transform.scale(self.raw_image, (width, height))
        self.image = self.image_original.copy()
        # Position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = width
        self.height = height
        # Rotation angle.
        self.angle = 0
        # Create a group for bullets.
        self.bullets = pygame.sprite.Group()
      
    def rotate(self, direction):
        # Limit the rotation angle.
        if direction == True and self.angle > -40:
            self.angle -= 1
        elif direction == False and self.angle < 1:
            self.angle += 1
        # Rotate the image
        new_image = pygame.transform.rotate(self.image_original, self.angle)
        # Store old center.
        old_center = self.rect.center 
        # Assign to self.image.      
        self.image = new_image              
        self.rect = self.image.get_rect()
        # Assign the original center. 
        self.rect.center = old_center
    
    def fire(self):
        # Create a bullet when firing.
        bullet = Bullet(BULLETIMAGEWIDTH, BULLETIMAGEHEIGHT, self.rect.x, self.rect.y, self.angle)
        # Rotate basic on cannon angle.
        bullet.rotate()
        # 10 times speed of ballon.
        bullet.speed = -30
        self.bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, angle):
        super().__init__()
        # Load image.
        self.raw_image = pygame.image.load('./asserts/tank_bullet5.png').convert_alpha()
        # Scale image.
        self.image_original = pygame.transform.scale(self.raw_image, (width, height))
        self.image = self.image_original.copy()
        # Position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = width
        self.height = height
        # Rotation angle and initial speed.
        self.angle = angle
        self.speed = 0

    def move(self):
        # Flying when speed is not 0.
        if self.speed != 0:
            if self.angle != 0:
                # Calculate x,y basic on tangential velocity.
                x = self.speed * math.cos(-1 * self.angle * math.pi / 180)
                y = self.speed * math.sin(-1 * self.angle * math.pi / 180)
                self.rect = self.rect.move(x, y)
            else:
                # Flying when there is no angle. 
                self.rect = self.rect.move(self.speed, 0)

    def rotate(self):
        # Rotate the bullet.
        new_image = pygame.transform.rotate(self.image_original, self.angle)
        old_center = self.rect.center      
        self.image = new_image              
        self.rect = self.image.get_rect()   
        self.rect.center = old_center

    def update(self):
        # Kill sprite when it is out of boundary.
        if self.rect.centerx < 10 or self.rect.centery < 10:
            self.kill()

def main():
    # Initiate.
    pygame.init()
    pygame.mixer.init()
    # Load sound effects.
    background_music = pygame.mixer.Sound("./asserts/Will2Pwr.mp3")
    explosion_sound = pygame.mixer.Sound("./asserts/Explosion.mp3")
    fire_sound = pygame.mixer.Sound("./asserts/Gunfire.mp3")
    start_sound = pygame.mixer.Sound("./asserts/StoneDrop.mp3")
    background_music.set_volume(0.6)
    background_music.play(-1)
    # Create a window with 800x600.
    window_surface = pygame.display.set_mode((800, 600))
    # Set the title of the game.
    pygame.display.set_caption('Ballon Shooting !')
    # Background color.
    window_surface.fill(WHITE)
    # Set event for animation and movement.
    ballon_animation = USEREVENT + 1
    ballon_movement_1 = USEREVENT + 2
    ballon_movement_2 = USEREVENT + 3
    pygame.time.set_timer(ballon_animation, 150)
    pygame.time.set_timer(ballon_movement_1, 300)
    pygame.time.set_timer(ballon_movement_2, 500)
    # Load tank and ballon.
    tank = pygame.image.load("./asserts/tanks_tankGrey_body2.png")
    ballon = Ballon(BALLONIMAGEWIDTH, BALLONIMAGEHEIGHT, 10, 50)
    cannon = Cannon(CANNONIMAGEWIDTH, CANNONIMAGEHEIGHT, 693, 503)
    head_font = pygame.font.SysFont(None, 20)
    text_surface = head_font.render('Number of Missed Shots:', True, (0, 0, 0))

    main_clock = pygame.time.Clock()
    start_game = False
    # Event processing.
    while True:
        # Starting scene.
        start_font = pygame.font.SysFont(None, 60)
        start_surface = start_font.render('Press any key to start or esc to quit', True, (0, 0, 0))
        window_surface.fill(WHITE)
        window_surface.blit(start_surface, (WINDOW_WIDTH / 14, WINDOW_HEIGHT / 2  - 30))
        # Record number of missed bullet.
        number_of_missed = 0
        pygame.display.update()
        # Quit the game or play.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                start_sound.play()
                start_game = True

        while start_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # Event for ballon animation.
                elif event.type == ballon_animation:
                    ballon.update()
                # Event for random movement of ballon.
                elif event.type == ballon_movement_1:
                    ballon.random_direction()
                elif event.type == ballon_movement_2:
                    ballon.random_direction()
                # Event when fire.
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    number_of_missed += 1
                    fire_sound.play()
                    cannon.fire()
            # Event for user control up and down.
            if pygame.key.get_pressed()[pygame.K_UP]:
                cannon.rotate(True)
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                cannon.rotate(False)

            ballon.move()
            # Drawing.
            window_surface.fill(WHITE)
            window_surface.blit(text_surface, (10, 10))
            window_surface.blit(ballon.image, ballon.rect)
            window_surface.blit(cannon.image, cannon.rect)
            # Behavior for every bullet.
            for i, bullet in enumerate(cannon.bullets):
                if bullet.speed != 0:
                    bullet.move()
                    window_surface.blit(bullet.image, bullet.rect)
                # Hit the ballon.
                if ballon.isCollision(bullet.rect):
                    explosion_sound.play()
                    # Explosion animation.
                    for i in range(3):
                        ballon.explosion_animate()
                        window_surface.blit(ballon.image, ballon.rect)
                        pygame.display.update()
                        time.sleep(0.04)
                    ballon.update()
                    ballon.kill()
                    bullet.kill()
                    # Scene for display result.
                    window_surface.fill(WHITE)
                    missed_surface = head_font.render(f'Number of Missed Shots: {number_of_missed - 1}', True, (0, 0, 0))
                    window_surface.blit(missed_surface, (10, 10))
                    end_surface = start_font.render('Press any key to continue', True, (0, 0, 0))
                    window_surface.blit(end_surface, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2  - 30))
                    # Game end.
                    start_game = False
                    pygame.display.update()
                    flag = True
                    # Wait until user input.
                    while flag:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                start_sound.play()
                                flag = False
                
                bullet.update()
            
            window_surface.blit(tank, (710, 500))
            # Update screen.
            pygame.display.update()
            main_clock.tick(FPS)

if __name__ == '__main__':    
    main()