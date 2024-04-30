from contextlib import AsyncExitStack
import pygame
from settings import *
from player import Player
from monster import Monster

class Minotaur(Monster):
    def __init__(self, pos, groups, obstacle_sprites, player):
        super().__init__(pos, groups, obstacle_sprites, player)
        # always need this for any kind of sprite
        self.image = pygame.image.load('minotaur.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.hitbox = self.rect
        self.move_counter = 0
        self.patrol = 0
        self.direction = pygame.math.Vector2()
        self.status = "sleep"
        self.patrol_length = 6
        self.detect_range = 3
        self.speed = 50
        self.obstacle_sprites = obstacle_sprites
        self.alive = True
        self.player = player
        self.go = False
        self.dizzy_count = 0
        self.dizzy_end = 3
        self.max_hp = 5
        self.curr_hp = 5
        self.atk = 2

        # graphics setup
        self.import_monster_assets()

    def import_monster_assets(self):
        character_path = "graphics/player/"
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation

    def patrol_path(self):
        #notes

        if self.status == "sleep":
            if (abs(self.player.pos[0] - self.pos[0]) <= self.detect_range) and (abs(self.player.pos[1] - self.pos[1]) <= self.detect_range):
                self.status = "wakeup"
                #Lets add a waking up effect here

    def pursue(self):
        self.direction = pygame.math.Vector2(0, 0)
        if self.status == "moveX":
            if self.player.pos[0] == self.pos[0]:
                self.status = "chargeY"
                self.direction = pygame.math.Vector2(0, 0)
            elif self.player.pos[0] > self.pos[0]:
                self.direction.x = 1
            else:
                self.direction.x = -1
        elif self.status == "moveY":
            if self.player.pos[1] == self.pos[1]:
                self.status = "chargeX"
                self.direction = pygame.math.Vector2(0, 0)
            elif self.player.pos[1] > self.pos[1]:
                self.direction.y = 1
            else:
                self.direction.y = -1
        elif (self.status == "chargeX") and self.go:
            self.speed = 25
            if self.player.pos[0] > self.pos[0]:
                self.status = "chargeR"
            else:
                self.status = "chargeL"
        elif (self.status == "chargeY") and self.go:
            self.speed = 25
            if self.player.pos[1] > self.pos[1]:
                self.status = "chargeD"
            else:
                self.status = "chargeU"
        elif self.status == "chargeR":
            self.direction.x = 1
        elif self.status == "chargeL":
            self.direction.x = -1
        elif self.status == "chargeD":
            self.direction.y = 1
        elif self.status == "chargeU":
            self.direction.y = -1
        elif self.status == "pursue":
            if abs(self.player.pos[0] - self.pos[0]) <= abs(self.player.pos[1] - self.pos[1]):
                self.status = "moveX"
            else:
                self.status = "moveY"

    def move(self, speed):

        # Move counter can be BPM of Track
        if self.move_counter >= speed:
            noAttack = True
            if self.status == "idle":
                self.status = "pursue"
                return
            if self.status == "chargeX":
                if self.go == False:
                    self.go = True
                    return
            if self.status == "chargeY":
                if self.go == False:
                    self.go = True
                    return
            if self.status == "dizzy":
                if self.dizzy_count == self.dizzy_end:
                    self.status = "pursue"
                else:
                    self.dizzy_count += 1
            # Every x frames, allow movement
            # Multiply hitbox x and y by the direction given from
            # input and the TILESIZE (in this case 64)
            if self.direction.y == 0:
                if (self.player.pos[0] == (self.pos[0] + self.direction.x)) and (self.player.pos[1] == self.pos[1]):
                    if (self.status == "chargeR") or (self.status == "chargeL"):
                        self.player.curr_hp -= self.atk
                        noAttack = False
                        self.status = "idle"
                        self.speed = 50
                else:
                    self.hitbox.x += self.direction.x * TILESIZE
                    self.collision('horizontal')
                    self.rect.center = self.hitbox.center
            if self.direction.x == 0:
                if (self.player.pos[0] == self.pos[0]) and (self.player.pos[1] == (self.pos[1] + self.direction.y)):
                    if (self.status == "chargeD") or (self.status == "chargeU"):
                        self.player.curr_hp -= self.atk
                        noAttack = False
                        self.status = "idle"
                        self.speed = 50
                else:
                    self.hitbox.y += self.direction.y * TILESIZE
                    self.collision('vertical')
                    self.rect.center = self.hitbox.center
            self.move_counter = 0
            if (noAttack):
                self.pos = (round(self.hitbox.x / 64), round(self.hitbox.y / 64))
            if self.status == "wakeup":
                self.status = "pursue"
        else:
            self.move_counter += 1

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                        if self.status == "chargeR":
                            self.status = "dizzy"
                            self.speed = 50
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                        if self.status == "chargeL":
                            self.status = "dizzy"
                            self.speed = 50
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
                        if self.status == "chargeU":
                            self.status = "dizzy"
                            self.speed = 50
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                        if self.status == "chargeD":
                            self.status = "dizzy"
                            self.speed = 50
            if self.player.hitbox.colliderect(self.hitbox):
                if self.direction.y < 0:  # moving right
                    self.hitbox.top = self.player.hitbox.bottom
                if self.direction.y > 0:  # moving left
                    self.hitbox.bottom = self.player.hitbox.top

    def checkStatus(self):
        if self.curr_hp < 1:
            self.alive = False
            self.hitbox.x += 100 * TILESIZE
            self.hitbox.y += 100 * TILESIZE
            self.pos = (round(self.hitbox.x / 64), round(self.hitbox.y / 64))
            self.rect.center = self.hitbox.center

    def update(self):
        if self.status != "sleep":
            self.pursue()
        self.patrol_path()
        self.move(self.speed)
        self.checkStatus()



