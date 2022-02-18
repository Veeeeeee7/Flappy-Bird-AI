import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

bird_imgs = [pygame.transform.scale2x(pygame.image.load("C:\\Users\\helen\\Desktop\\Flappy Bird AI\\imgs\\bird1.png")), pygame.transform.scale2x(pygame.image.load("C:\\Users\\helen\\Desktop\\Flappy Bird AI\\imgs\\bird2.png")), pygame.transform.scale2x(pygame.image.load("C:\\Users\\helen\\Desktop\\Flappy Bird AI\\imgs\\bird3.png"))]
pipe_img = pygame.transform.scale2x(pygame.image.load("C:\\Users\\helen\\Desktop\\Flappy Bird AI\\imgs\\pipe.png"))
base_img = pygame.transform.scale2x(pygame.image.load("C:\\Users\\helen\\Desktop\\Flappy Bird AI\\imgs\\base.png"))
background_img = pygame.transform.scale2x(pygame.image.load("C:\\Users\\helen\\Desktop\\Flappy Bird AI\\imgs\\bg.png"))

class Bird:
    imgs = bird_imgs
    rotation_velocity = 20
    max_rotation = 25
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.velocity*self.tick_count + 1.5*self.tick_count**2
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
                self.tilt -= self.velocity

    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_time*2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation_time*4:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*4+1:
            self.img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.animation_time*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    gap = 200
    vel = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_img, False, True)
        self.pipe_bottom = pipe_img
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_suface(self.pipe_top)
        bottom_mask = pygame.mask.from_suface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bottom_point:
            return True
        return False

class Base:
    vel = 5
    width = base_img.get_width()
    img = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 = self.vel

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

def draw_window(win, bird, pipes, base):
    win.blit(background_img, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)

    pygame.display.update()

def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    draw_window(win, bird, pipes, base)
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()
        base.move()
        draw_window(win, bird, pipes, base)


    pygame.quit()
    quit()

main()