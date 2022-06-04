import pygame as pg


BASE_SURF = pg.transform.scale2x(pg.image.load('images/base.png'))


class Base:
    def __init__(self, y):
        self.vel = 5
        self.width = BASE_SURF.get_width()
        self.img = BASE_SURF
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, screen):
        screen.blit(self.img, (self.x1, self.y))
        screen.blit(self.img, (self.x2, self.y))
