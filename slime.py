from contextlib import AsyncExitStack
import pygame
from settings import *
from player import Player
from monster import Monster

class Slime(Monster):
    def __init__(self, pos, groups, obstacle_sprites, player):
        super().__init__(pos, groups, obstacle_sprites, player)
        # always need this for any kind of sprite
        self.image = pygame.image.load('slime.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.hitbox = self.rect
        self.move_counter = 0
        self.patrol = 0
        self.direction = pygame.math.Vector2()
        self.status = "patrol"
        self.patrol_length = 8
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.alive = True
        self.player = player
        self.max_hp = 2
        self.curr_hp = 2
        self.atk = 1
        self.idle_frame = 0
        self.idle = False

        # graphics setup
        self.import_monster_assets()

    def import_monster_assets(self):
        character_path = "graphics/player/"
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation

    def pathfind(self):
        self.direction = pygame.math.Vector2(0, 0)

        #notes
        #The slime bounces around in a circle and attacks only if the player steps
        #in its way
        #it uses the patrol field to dictate which direction it moves
        #which counts up in move() every time it take a move action
        #it does not count up when it makes an attack

        match self.patrol:
            case 0:
                self.direction.y = -1
            case 1:
                self.direction.y = 0
            case 2:
                self.direction.x = 1
            case 3:
                self.direction.x = 0
            case 4:
                self.direction.y = 1
            case 5:
                self.direction.y = 0
            case 6:
                self.direction.x = -1
            case 7:
                self.direction.x = 0
        
        

    def move(self, speed):

        # Move counter can be BPM of Track
        if self.move_counter >= 30:
            noAttack = True
            if(self.idle_frame == 0):
                self.image = pygame.image.load('slimeIdleTwo.png').convert_alpha()
                self.idle_frame = 1
            else:
                self.image = pygame.image.load('slime.png').convert_alpha()
                self.idle_frame = 0
            if self.idle:
                self.idle = False
                self.move_counter = 0
                if self.alive == False:
                    self.checkStatus()
                return
            # Every x frames, allow movement
            # Multiply hitbox x and y by the direction given from
            # input and the TILESIZE (in this case 64)
            if self.direction.y == 0:
                if (self.player.pos[0] == (self.pos[0] + self.direction.x)) and (self.player.pos[1] == self.pos[1]):
                    self.player.curr_hp -= self.atk
                    self.image = pygame.image.load('slimeAttack.png').convert_alpha()
                    self.idle = True
                    self.idle_frame = 1
                    noAttack = False
                else:
                    self.hitbox.x += self.direction.x * TILESIZE
                    self.collision('horizontal')
                    self.rect.center = self.hitbox.center
            if self.direction.x == 0:
                if (self.player.pos[0] == self.pos[0]) and (self.player.pos[1] == (self.pos[1] + self.direction.y)):
                    self.player.curr_hp -= self.atk
                    self.image = pygame.image.load('slimeAttack.png').convert_alpha()
                    self.idle = True
                    self.idle_frame = 1
                    noAttack = False
                else:
                    self.hitbox.y += self.direction.y * TILESIZE
                    self.collision('vertical')
                    self.rect.center = self.hitbox.center
            self.move_counter = 0
            if (noAttack):
                self.pos = (round(self.hitbox.x / 64), round(self.hitbox.y / 64))
                self.patrol += 1
                if (self.patrol == self.patrol_length):
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

    def takeDamage(self):
        self.idle = True
        if self.curr_hp < 1:
            self.alive = False
            self.idle = True
            self.image = pygame.image.load('slimeDeath.png').convert_alpha()
        else:
            self.image = pygame.image.load('slimeTakeDamage.png').convert_alpha()
        

    def checkStatus(self):
        if self.alive == False:
            self.hitbox.x += 100 * TILESIZE
            self.hitbox.y += 100 * TILESIZE
            self.pos = (round(self.hitbox.x / 64), round(self.hitbox.y / 64))
            self.rect.center = self.hitbox.center

    def update(self):
        self.pathfind()
        self.move(self.speed)
        

