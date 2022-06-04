import pygame as pg
BIRDS_SURF = [pg.transform.scale2x(pg.image.load('images/bird1.png')), pg.transform.scale2x(pg.image.load('images/bird2.png')), pg.transform.scale2x(pg.image.load('images/bird3.png'))]


class Bird:
    def __init__(self, x, y):
        self.imgs = BIRDS_SURF
        self.max_rotation = 25
        self.rot_vel = 20
        self.animation_time = 5
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = y
        self.img_count = 0
        self.cur_img = self.imgs[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel

    def draw(self, screen):
        self.img_count += 1
        if self.img_count < self.animation_time:
            self.cur_img = self.imgs[0]
        elif self.img_count < self.animation_time * 2:
            self.cur_img = self.imgs[1]
        elif self.img_count < self.animation_time*3:
            self.cur_img = self.imgs[2]
        elif self.img_count < self.animation_time*4:
            self.cur_img = self.imgs[1]
        elif self.img_count == self.animation_time*4 + 1:
            self.cur_img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.cur_img = self.imgs[1]
            self.img_count = self.animation_time*2

        rotated_image = pg.transform.rotate(self.cur_img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.cur_img.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pg.mask.from_surface(self.cur_img)


