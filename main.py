import pygame
import random
import sys
import os
import ctypes
from bird import Bird
from pipe import Pipe
from base import Base
import neat
WIN_WIDTH = 500
WIN_HEIGHT = 800
pygame.init()
pygame.font.init()
ctypes.windll.user32.SetProcessDPIAware()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(
    "imgs/bird{}.png".format(i))) for i in range(1, 4)]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("imgs/pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("imgs/base.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load("imgs/bg.png"))
STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    for bird in birds:
        bird.draw(win)
    base.draw(win)
    text = STAT_FONT.render("Score " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    for pipe in pipes:
        pipe.draw(win)

    pygame.display.update()
        


def main(genomes, config):
    birds = []
    ge = []
    nnets = []
    for index, genome in genomes:
        birds.append(Bird(BIRD_IMGS, 230, 350))
        genome.fitness = 0
        ge.append(genome)
        nnet = neat.nn.FeedForwardNetwork.create(genome, config)
        nnets.append(nnet)
    
    base = Base(BASE_IMG, 730)
    pipes = [Pipe(PIPE_IMG, 700)]
    score = 0
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 0 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            break
        print(len(birds))
        for bird in birds:
            ge[birds.index(bird)].fitness += 0.1
            bird.move()

            output = nnets[birds.index(bird)].activate((bird.y, abs(
                bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))
            if output[0] > 0.5:
                bird.jump()

        base.move()
        rem = []
        add_pipe = False

        for pipe in pipes:
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                # pipes.pop(pipes.index(pipe))
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1
                    ge.pop(birds.index(bird))
                    nnets.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(PIPE_IMG, 700)) 
            for genome in ge:
                genome.fitness += 5
        
        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                ge[birds.index(bird)].fitness -= 1
                ge.pop(birds.index(bird))
                nnets.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score)
        
def run(config_dir):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_dir)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.run(main, 50)


if __name__ == "__main__":
    local_dir = os.getcwd()
    print(local_dir)
    config_dir = os.path.join(local_dir, "config-feedforward.txt")
    run(config_dir)
    
