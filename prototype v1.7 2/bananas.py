import pygame
from pygame.locals import *
vec= pygame.math.Vector2
ACC= 1.2
FRIC = -0.10
WIDTH = 700
HEIGHT = 500

class Banana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/banana.png")
        self.rect = self.image.get_rect()
        self.pos=vec((100, 250))
        self.vel=vec(0, 0)
        self.acc=vec(0, 0)
        if self.rect.bottom<59:
            y = 59

    def update(self):
        self.acc = vec(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.acc.x = +ACC
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.acc.y = -ACC
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.acc.y = +ACC
            
        #friction and acceleration

        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #movement limits
        if self.pos.x > 650:
            self.pos.x = 650
        if self.pos.x < 50:
            self.pos.x = 50
        if self.pos.y > 400:
            self.pos.y =400
        if self.pos.y < 40:
            self.pos.y =40

        self.rect.center = self.pos
    
    def increaseSize(self):
        self.image=pygame.transform.scale(self.image, (114, 114))
    def decreaseSize(self):
        self.image=pygame.image.load("assets/banana.png")

    def reset(self):
        self.pos = vec((180, 550))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

