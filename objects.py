import pygame

class ScrollingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
                 
    def update(self):
        self.rect.x -= self.speed


class Flower(ScrollingObject):
    def __init__(self, x, y, speed):
        ScrollingObject.__init__(self,x,y,speed,"assets/flower.png")
       

class Bomb(ScrollingObject):
    def __init__(self, x, y, speed):
        ScrollingObject.__init__(self,x,y,speed,"assets/bomb.png")
                
class Mushroom(ScrollingObject):
    def __init__(self, x, y, speed):
        ScrollingObject.__init__(self,x,y,speed,"assets/mushroom1.png")

class BlueMushroom(ScrollingObject):
    def __init__(self, x, y, speed):
        ScrollingObject.__init__(self,x,y,speed,"assets/mushroom2.png")





