import pygame
from settings import *
from tile import Tile
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

        self.monster_list = []
        # sprite set up
        self.create_map()

        self.pause = Pause(self.player)

    def create_map(self):
        for row_index, row in enumerate(LEVEL1):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites, self.monster_list)
        for row_index, row in enumerate(LEVEL1):
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
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.monster.update()
            debug(self.monster_list[0].status)


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