import pygame

import level
from settings import *
from debug import *
from level import *


# from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, monster_list, chest):
        super().__init__(groups)
        # always need this for any kind of sprite
        self.image = pygame.image.load('graphics/player_left_knife.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.hitbox = self.rect
        self.move_counter = 0
        self.direction = pygame.math.Vector2()
        self.status = "stationary"
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.max_hp = 3
        self.curr_hp = 3
        self.atk = 1
        self.monster_list = monster_list
        self.didKill = False
        self.BPM = 30
        self.Win = False
        self.kill_count = 0
        # graphics setup
        self.import_player_assets()
        self.mon_killed = False
        self.target = None
        self.monster_hit = False
        self.attack_thrown = False
        self.chest = chest

    def import_player_assets(self):
        character_path = "graphics/player/"
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_UP]:
            self.direction.y = -1
            # self.status = up
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            # self.status = down

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        # If both horizontal and vertical directions are pressed, prioritize one
        if self.direction.x != 0 and self.direction.y != 0:
            # Prioritize horizontal movement
            if abs(self.direction.x) > abs(self.direction.y):
                self.direction.y = 0
            # Prioritize vertical movement
            else:
                self.direction.x = 0

    def move(self, speed):
        self.mon_killed = False
        #
        if self.move_counter >= (self.BPM - 10) and self.move_counter <= (self.BPM) and (
                self.direction.x != 0 or self.direction.y != 0):
            # Every x frames, allow movement
            # Multiply hitbox x and y by the direction given from
            # input and the TILESIZE (in this case 64)
            self.target = None
            for m in self.monster_list:
                if ((self.pos[0] + self.direction.x) == m.pos[0]) and (self.pos[1] == m.pos[1]):
                    self.target = m
                    self.attack_thrown = True
                    self.move_counter = 0
                    return
                if (self.pos[0] == m.pos[0]) and ((self.pos[1] + self.direction.y) == m.pos[1]):
                    self.target = m
                    self.attack_thrown = True
                    self.move_counter = 0
                    return
            self.hitbox.x += self.direction.x * TILESIZE
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * TILESIZE
            self.collision('vertical')
            self.rect.center = self.hitbox.center
            self.move_counter = 0
            self.pos = (round(self.hitbox.x / 64), round(self.hitbox.y / 64))
        elif self.move_counter > self.BPM:
            self.target = None
            self.move_counter = 0
        else:
            self.move_counter += 1

    def attack(self):
        if self.monster_hit == False and self.target and self.attack_thrown:
            self.target.curr_hp -= self.atk
            self.target.takeDamage()
            if self.target.alive == False and self.target.counted == False:
                self.target.counted = True
                self.kill_count += 1
                self.mon_killed = True
                if self.kill_count == len(self.monster_list):
                    self.didKill = True
        self.monster_hit = False
        self.target = None
        self.attack_thrown = False

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
            for monster in self.monster_list:
                if monster.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = monster.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = monster.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
            for monster in self.monster_list:
                if monster.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = monster.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = monster.hitbox.top

    def update(self):
        debug(self.curr_hp, 10, 10)
        if self.status == "right":
            self.image = pygame.image.load('graphics/player_knife.png').convert_alpha()
            #self.rect = self.image.get_rect(topleft=self.pos)
        elif self.status == "left":
            self.image = pygame.image.load('graphics/player_left_knife.png').convert_alpha()
            #self.rect = self.image.get_rect(topleft=self.pos)
        self.input()
        self.move(self.speed)    