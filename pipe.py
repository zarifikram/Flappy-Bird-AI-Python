import pygame
import random


class Pipe():
    GAP = 200
    VX = 5

    def __init__(self, IMG, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.img = IMG
        self.PIPE_TOP = pygame.transform.flip(self.img, False, True)
        self.PIPE_BOTTOM = IMG
        self.passed = False
        self.set_height()
        # print(self.PIPE_BOTTOM, self.PIPE_TOP)

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def generate(self):
        randompipe = random.randrange(112, 400)
        bottom = self.sprite.get_rect(midtop=(self.defaultx, randompipe))
        top = self.sprite.get_rect(midbottom=(
            self.defaultx, randompipe - self.distance))
        self.all.append([bottom, top])
        # print("generating pipes")

    def move(self):
        self.x -= self.VX

    def draw(self, win):
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        win.blit(self.PIPE_TOP, (self.x, self.top))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return b_point or t_point

    def clear(self):
        self.all.clear()

    # def draw(self):
