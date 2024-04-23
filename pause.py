import pygame
from settings import *


class Pause:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

    def display(self):
        self.display_surface.fill('black')
