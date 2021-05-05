import pygame 
import sys
import random
from scores import Score

class Bird():
    def __init__(self):
        self.x = 100//2
        self.y = 512//2
        self.low = 440
        self.high = 0
        self.vx = 10 
        self.vy = 0
        self.gravity = 0.25
        self.sprite = pygame.image.load("assets/bluebird-downflap.png").convert()
        self.rect = self.sprite.get_rect(center = (self.x, self.y))
        self.score = Score()

    def flap(self):
        self.vy = 0
        self.vy -= 6

    def move(self):
        self.vy += self.gravity
        self.y += self.vy
        if(self.y > self.low):
            self.y = self.low
        self.rect.centery = self.y

    def clear(self):
        self.y = 512//2
        self.vy = 0
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

    

