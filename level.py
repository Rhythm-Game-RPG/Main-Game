import sys

import pygame
from settings import *
from tile import Tile
from floor import Floor
from player import Player
from debug import debug
from pause import Pause
from monster import Monster
from slime import Slime
from skeleton import Skeleton
from bat import Bat
from minotaur import Minotaur


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        # sprite group set up
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.worlds = [LEVEL1, LEVEL2, LEVEL3, LEVEL4]
        self.monster_list = []
        # sprite set up

        self.counter = 0
        pygame.mixer.init()
        self.m_val = 0
        self.create_map(self.counter)
        self.monster_count = 0
        self.pause = Pause(self.player)
        self.moved_level = False

    def create_map(self, x):
        level = []
        if self.counter == 0:
            level = LEVEL1.copy()
        elif self.counter == 1:
            level = LEVEL2.copy()
        elif self.counter == 2:
            level = LEVEL3.copy()
        elif self.counter == 3:
            level = LEVEL4.copy()

        for row_index, row in enumerate(level):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != 'x':
                    Floor((x, y), [self.visible_sprites])
        for row_index, row in enumerate(level):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites, self.monster_list)
        for row_index, row in enumerate(level):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'm':
                    self.monster = (Minotaur((x, y), [self.visible_sprites], self.obstacles_sprites, self.player))
                    self.player.monster_list.append(self.monster)
                if col == 'k':
                    self.monster = (Skeleton((x, y), [self.visible_sprites], self.obstacles_sprites, self.player))
                    self.player.monster_list.append(self.monster)
                if col == 's':
                    self.monster = (Slime((x, y), [self.visible_sprites], self.obstacles_sprites, self.player))
                    self.player.monster_list.append(self.monster)
                if col == 'b':
                    self.monster = (Bat((x, y), [self.visible_sprites], self.obstacles_sprites, self.player))
                    self.player.monster_list.append(self.monster)

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        if self.game_paused:
            self.pause.display()
            # display pause menu
        else:
            if self.player.didKill:
                var = self.player.curr_hp
                self.next_level()
                self.player.curr_hp = var
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.monster.update()

    def next_level(self):
        self.counter += 1
        if self.counter == 4:
            pygame.quit()
            sys.exit()
        self.visible_sprites.empty()
        self.obstacles_sprites.empty()
        self.monster_list.clear()
        self.player = None
        self.monster = None
        self.create_map(self.counter)
        self.player.didKill = False
        self.moved_level = True


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
