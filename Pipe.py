import pygame as pg
import random
PIPE_SURF = pg.transform.scale2x(pg.image.load('images/pipe.png'))


class Pipe:
    def __init__(self, x):
        self.gap = 200
        self.vel = 5
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.pipe_top = pg.transform.flip(PIPE_SURF, False, True)
        self.pipe_bottom = PIPE_SURF
        self.passed = False
        self.set_height()

    def set_height(self):
        gap = random.randrange(54, 100)
        self.height = random.randrange(150, 450)
        self.top = self.height - self.pipe_top.get_height() - gap
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, screen):
        screen.blit(self.pipe_top, (self.x, self.top))
        screen.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.pipe_top)
        bottom_mask = pg.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if t_point or b_point:
            return True
        return False

