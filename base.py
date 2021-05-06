import pygame
import sys
import random


class Base:
    VX = 5

    def __init__(self, IMG, y):
        self.img = IMG
        self.WIDTH = self.img.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VX
        self.x2 -= self.VX
        if self.x1 + self.WIDTH <= 0:
            self.x1 += self.WIDTH
            self.x2 += self.WIDTH

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))
