import pygame as pg
import time
import os
import random
import neat
from Bird import Bird
from Pipe import Pipe
from Base import Base

pg.init()
pg.font.init()


BIRDS_SURF = [pg.transform.scale2x(pg.image.load('images/bird1.png')), pg.transform.scale2x(pg.image.load('images/bird2.png')), pg.transform.scale2x(pg.image.load('images/bird3.png'))]
PIPE_SURF = pg.transform.scale2x(pg.image.load('images/pipe.png'))
BASE_SURF = pg.transform.scale2x(pg.image.load('images/base.png'))
BG_SURF = pg.transform.scale2x(pg.image.load('images/bg.png'))
STAT_FONT = pg.font.SysFont("comicsans", 50)

WIDTH = 578
HEIGHT = 800


def draw_window(screen, bird, pipes, base, score):
    screen.blit(BG_SURF, (0, 0))

    for pipe in pipes:
        pipe.draw(screen)

    text = STAT_FONT.render(f"Score: {score}", True, "white")
    screen.blit(text, (WIDTH - 10 - text.get_width(), 10))

    base.draw(screen)
    bird.draw(screen)

    pg.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    running = True
    score = 0
    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(700))
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.cur_img.get_height() >= 700:
            pass

        # bird.move()
        base.move()
        draw_window(screen, bird, pipes, base, score)

    pg.quit()
    quit()


if __name__ == "__main__":
    main()