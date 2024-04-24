from contextlib import AsyncExitStack
import pygame
from settings import *
from player import Player

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, player):
        super().__init__(groups)
        # always need this for any kind of sprite
        self.image = pygame.image.load('slime.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.hitbox = self.rect
        self.move_counter = 0
        self.patrol = 0
        self.direction = pygame.math.Vector2()
        self.status = "stationary"
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.max_hp = 1
        self.atk = 1

        # graphics setup
        self.import_player_assets()

    def import_player_assets(self):
        character_path = "graphics/player/"
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation

    def attack(self):
        self.player.curr_hp -= self.atk
        return

    def pathfind(self):
        self.direction = pygame.math.Vector2(0, 0)

        #notes
        #first check for adjecent
        #next check for greater difference between x and y, unless one is 0
        #This will make it move in a diagonal
        #May be better to have it align with one axis, then another
        #need to be able to navigate obstacles

        match self.patrol:
            case 0:
                self.direction.y = -1
            case 1:
                self.direction.x = 1
            case 2:
                self.direction.y = 1
            case 3:
                self.direction.x = -1
        
        

    def move(self, speed):

        # Move counter can be BPM of Track
        if self.move_counter >= 100:
            noAttack = True
            # Every x frames, allow movement
            # Multiply hitbox x and y by the direction given from
            # input and the TILESIZE (in this case 64)
            if self.direction.y == 0:
                if (self.player.pos[0] == (self.pos[0] + self.direction.x)) and (self.player.pos[1] == self.pos[1]):
                    self.player.curr_hp -= self.atk
                    noAttack = False
                else:
                    self.hitbox.x += self.direction.x * TILESIZE
                    self.collision('horizontal')
                    self.rect.center = self.hitbox.center
            if self.direction.x == 0:
                if (self.player.pos[0] == self.pos[0]) and (self.player.pos[1] == (self.pos[1] + self.direction.y)):
                    self.player.curr_hp -= self.atk
                    noAttack = False
                else:
                    self.hitbox.y += self.direction.y * TILESIZE
                    self.collision('vertical')
                    self.rect.center = self.hitbox.center
            self.move_counter = 0
            if (noAttack):
                self.pos = (round(self.hitbox.x / 64), round(self.hitbox.y / 64))
                self.patrol += 1
                if (self.patrol == 4):
                    self.patrol = 0
        else:
            self.move_counter += 1

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
            if self.player.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0:  # moving right
                    self.hitbox.right = self.player.hitbox.left
                if self.direction.x < 0:  # moving left
                    self.hitbox.left = self.player.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
            if self.player.hitbox.colliderect(self.hitbox):
                if self.direction.y < 0:  # moving right
                    self.hitbox.top = self.player.hitbox.bottom
                if self.direction.y > 0:  # moving left
                    self.hitbox.bottom = self.player.hitbox.top

    def update(self):
        self.pathfind()
        self.move(self.speed)
