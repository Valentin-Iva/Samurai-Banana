import pygame
from pygame.locals import *

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #position is set from the top left corner
        self.clicked = False
    def draw(self,screen):

        action = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked=False

        

        return action