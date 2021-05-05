import pygame 
import sys
import random
from score import Score

class Bird():
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    def __init__(self, IMGS, x, y):
        self.IMGS = IMGS
        self.img = self.IMGS[0]
        self.x = x
        self.y = y
        self.jumpy = self.y
        self.tilt = 0
        self.tilt_count = 0
        self.tick_count = 0
        self.img_count = 0
        self.low = 440
        self.high = 0
        self.vx = 10 
        self.vy = 0
        self.gravity = 3
        # print(1111111111)
        self.sprite = pygame.image.load("assets/bluebird-downflap.png").convert()
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

        self.score = Score()

    def jump(self):
        self.vy = -7
        self.tick_count = 0
        self.jumpy = self.y

    def move(self):
        self.tick_count += 1
        # self.tilt_count += 1
        d = self.vy*self.tick_count + 0.5*self.gravity*self.tick_count**2
        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y < self.jumpy + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

        self.vy += self.gravity
        self.y += self.vy
       
        # self.rect.centery = self.y

    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        else:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_imgae = pygame.transform.rotate(self.img, self.tilt)
        self.rect = rotated_imgae.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_imgae, self.rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    

    def clear(self):
        self.y = 512//2
        self.vy = 0
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

    

