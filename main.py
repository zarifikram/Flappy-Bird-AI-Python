import pygame, random, sys, os
from bird import Bird
from pipes import Pipes
from score import Score
import neat

class main():
    def __init__(self, genomes, config):

        pygame.init()
        self.nets = []
        self.ge = []
        self.birds = []
        for g in genomes:
            net = neat.nn.FeedForwardNetwork(g, config)
            self.nets.append(net)
            self.birds.append(Bird())
            g.fitness = 0
            self.ge.append(g)
        self.height = 576//2
        self.width = 512 #1024
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.clock = pygame.time.Clock()
        self.is_active = True
        self.bg = pygame.image.load("assets/background-day.png").convert()
        self.bg = pygame.transform.scale2x(self.bg)
        self.floor = pygame.image.load("assets/base.png").convert()
        self.floor = pygame.transform.scale2x(self.floor)
        self.floorx = 0 
        self.bird = Bird()
        self.pipe = Pipes()
        self.score = self.bird.score
        
        # self.score = 0

    def draw_floor(self):
        self.screen.blit(self.floor, (self.floorx, 900//2))
        self.screen.blit(self.floor, (self.floorx + 576//2, 900//2))
        self.floorx -= 1
        # print(self.floorx)
        if self.floorx <= -576:
            self.floorx = 0
            
    def bird_progress(self):
        self.bird.move()
        self.screen.blit(self.bird.sprite, (self.bird.x, self.bird.y))
        for index, bird in enumerate(self.birds):
            bird.move()
            self.screen.blit(bird.sprite, (bird.x, bird.y))
            


    def pipe_progress(self):
        self.pipe.move()
        for pipe in self.pipe.all:
            self.screen.blit(self.pipe.sprite, pipe[0])
            flipped_pipe = pygame.transform.flip(self.pipe.sprite, False, True)
            self.screen.blit(flipped_pipe, pipe[1])
        thepipe = self.pipe.all[self.pipe.thisindex]
        for index, bird in enumerate(self.birds):
            ge[index] += 0.1
            output = self.nets[index].activate((bird.y, abs(bird.y - thepipe[0].top), abs(bird.y - thepipe[1].bottom)))
            if(output > 0.5):
                bird.flap()
           
    def score_check(self):
        # print("now")
        for pipe in self.pipe.all:
            # print(pipe.centerx, self.bird.rect.centerx)
            if pipe.centerx < self.birds[0].rect.centerx and pipe.centerx > self.birds[0].rect.centerx - 20:
                # print("fun")
                self.score.increase()
                for g in ge:
                    g.fitness += 5
            
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()
                        # print(self.bird.y)
                    if event.key == pygame.K_SPACE and not self.is_active:
                        self.is_active = True
                        self.clear()

                if event.type == self.pipe.SPAWN:
                    self.pipe.generate()
                    # print("generating")
                
                if event.type == self.score.CHECK and self.is_active:
                    self.score_check()
                        # do things
                # add more event keys as you wish
            if len(self.birds) == 0:
                break
            self.screen.blit(self.bg, (0,0))
            self.is_collided()
            # if self.is_collided():
            #     print("Noooo")
            # if self.is_active:
            self.bird_progress()
            self.pipe_progress()
            # self.score_check()
            # else:
                # print(self.score.hival)
            self.draw_floor()
            pygame.display.update()
            self.clock.tick(120)

    def is_collided(self):
        for index, bird in enumerate(self.birds):
            if bird.rect.centery >= self.height or bird.rect.center < 0:
                self.ge[index] -= 1
                self.birds.pop(index)
                self.nets.pop(index)
                self.ge.pop(index)

        for pipe in self.pipe.all:
            for index, bird in enumerate(self.birds):
                if bird.rect.colliderect(pipe):
                    self.ge[index] -= 1
                    self.birds.pop(index)
                    self.nets.pop(index)
                    self.ge.pop(index)


    def clear(self):
        self.bird.clear()
        self.pipe.clear()
        self.score.clear()

def dum():
    main = main()
    main.run()

def config_val(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(dum, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    config_val(config_path)

    # main = main()
    # main.run()
