import pygame
from settings import *


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # always need this for any kind of sprite
        self.image = pygame.image.load('graphics/ChestClose.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.pos=pos
    #def open (self):
        