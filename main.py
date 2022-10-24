import pygame as pg
import time
import os
import random
import neat
from Bird import Bird
from Pipe import Pipe
from Base import Base
import matplotlib.pyplot as plt
import numpy as np
import warnings

pg.init()
pg.font.init()


BIRDS_SURF = [pg.transform.scale2x(pg.image.load('images/bird1.png')), pg.transform.scale2x(pg.image.load('images/bird2.png')), pg.transform.scale2x(pg.image.load('images/bird3.png'))]
PIPE_SURF = pg.transform.scale2x(pg.image.load('images/pipe.png'))
BASE_SURF = pg.transform.scale2x(pg.image.load('images/base.png'))
BG_SURF = pg.transform.scale2x(pg.image.load('images/bg.png'))
STAT_FONT = pg.font.SysFont("comicsans", 50)

WIDTH = 578
HEIGHT = 800


def draw_window(screen, birds, pipes, base, score):
    screen.blit(BG_SURF, (0, 0))

    for pipe in pipes:
        pipe.draw(screen)

    text = STAT_FONT.render(f"Score: {score}", True, "white")
    screen.blit(text, (WIDTH - 10 - text.get_width(), 10))

    base.draw(screen)
    for bird in birds:
        bird.draw(screen)

    pg.display.update()

gl_score = 0

def main(genomes, config):
    global gl_score
    nets = []
    ge = []
    birds = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append((Bird(230, 350)))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(700)]

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    running = True
    score = 0
    while running:
        clock.tick(30)
        pipe_ind = 0
        rem = []
        add_pipe = False

        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind += 1
        else:
            running = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[birds.index(bird)].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness += 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    gl_score = score

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            for g in ge:
                g.fitness += 5
            score += 1
            pipes.append(Pipe(700))

        if score > 100:
            break

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.cur_img.get_height() >= 700 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                gl_score = score

        # bird.move()
        base.move()
        draw_window(screen, birds, pipes, base, score)



def run(config_file):
    import pickle
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    choice = input("If you want to start training 1 if you want to load previous training 2\n")

    if choice == '1':
        num_gen = int(input("Enter the number of generatio\n"))

        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        winner = p.run(main, num_gen)

        with open("winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

    else:
        if os.path.exists("winner.pkl"):

            with open("winner.pkl", "rb") as f:
                genome = pickle.load(f)

            genomes = [(1, genome)]
            main(genomes, config)
        else:
            print("You must to run training at least 1 time")





if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
    print(gl_score)