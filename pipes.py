import pygame, random

class Pipes():
    def __init__(self):
        self.all = []
        self.sprite = pygame.image.load("assets/pipe-green.png")
        self.SPAWN = pygame.USEREVENT
        self.defaultx = 350
        self.distance = 100
        self.vx = 3
        pygame.time.set_timer(self.SPAWN, 1200)
        self.thisindex = 0
        # print("creating pipes")

    def generate(self):
        randompipe = random.randrange(112, 400)
        bottom = self.sprite.get_rect(midtop = (self.defaultx, randompipe))
        top = self.sprite.get_rect(midbottom = (self.defaultx, randompipe - self.distance))
        self.all.append([bottom, top])
        # print("generating pipes")

    def move(self):
        for pipe in self.all:
            pipe[0].centerx -= self.vx
            pipe[1].centerx -= self.vx
        
        visible_pipes = [pipe for pipe in self.all if pipe[0].right > -25]
        self.all = visible_pipes
        for index, pipe in enumerate(self.all):
            if pipe[0].right < 130:
                self.thisindex = index
                break

    def clear(self):
        self.all.clear()

        

    # def draw(self): 
