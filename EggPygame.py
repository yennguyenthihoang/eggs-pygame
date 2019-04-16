import pygame
import sys
import math
from PIL import Image, ImageSequence

eggImage = pygame.image.load('images/egg.png')
grassImage = pygame.image.load('images/grass.png')

brokenEggImage = pygame.image.load('images/brokenEgg.gif')
brokenEggImage = pygame.transform.scale(brokenEggImage, (100, 120))

class Egg(object):
    def __init__(self, x, y, width, height, vx, vy, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.image = eggImage
        self.image = pygame.transform.scale(image, (width, height))
        

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.vx
        self.y += self.vy

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Paddle(object):
    def __init__(self, x, y, width, height, speed, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.speed = speed
        self.image = grassImage
        self.image = pygame.transform.scale(image, (width, height))
        

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.vx

    def key_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.vx = -self.speed
            elif event.key == pygame.K_RIGHT:
                self.vx = self.speed
        elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.vx = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)   


class Pong(object):
    COLOURS = {"WHITE": (255, 255, 255), "RED"  : (255,   0,   0)}
    def __init__(self):
        pygame.init()
        (WIDTH, HEIGHT) = (840, 680)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Eggs Pong - Group 4")
        self.egg = Egg(5, 5, 100, 120, 5, 5, eggImage)
        self.paddle = Paddle(WIDTH / 2, HEIGHT - 50, 200, 30, 3, grassImage)
        self.score = 0

    def play(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    self.paddle.key_handler(event)

            self.collision_handler()
            self.draw()

    def collision_handler(self):
        if self.egg.rect.colliderect(self.paddle.rect):
            self.egg.vy = -self.egg.vy
            self.score += 1

        if self.egg.x + self.egg.width >= self.screen.get_width():
            self.egg.vx = -(math.fabs(self.egg.vx))
        elif self.egg.x <= 0:
            self.egg.vx = math.fabs(self.egg.vx)

        if self.egg.y + self.egg.height >= self.screen.get_height():
            pygame.quit()
            sys.exit()
        elif self.egg.y <= 0:
            self.egg.vy = math.fabs(self.egg.vy)

        if self.paddle.x + self.paddle.width >= self.screen.get_width():
            self.paddle.x = self.screen.get_width() - self.paddle.width
        elif self.paddle.x <= 0:
            self.paddle.x = 0

    def draw(self):
        #set background to the screen
        backgroundImg = pygame.image.load('images/background.png')
        backgroundImg = pygame.transform.scale(backgroundImg, (840, 680))
        
        self.screen.blit(backgroundImg, (0, 0))

        font = pygame.font.Font(None, 48)
        
       
        scoreImage = pygame.image.load('images/highscore.png')
        scoreImage = pygame.transform.scale(scoreImage, (120, 70))
        self.screen.blit(scoreImage, (0, 0))
        
        score_text = font.render(str(self.score), True, Pong.COLOURS["RED"])
        self.screen.blit(score_text, (125, 20))

        self.egg.update()
        self.egg.render(self.screen)
        self.paddle.update()
        self.paddle.render(self.screen)

        pygame.display.update()

if __name__ == "__main__":
    Pong().play()