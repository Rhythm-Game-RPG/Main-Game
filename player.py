import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        # always need this for any kind of sprite
        self.image = pygame.image.load('graphics/player/right_idle/right_idle.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.hitbox = self.rect
        self.move_counter = 0
        self.direction = pygame.math.Vector2()
        self.status = "stationary"
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

        # graphics setup
        self.import_player_assets()

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
            # self.status = right
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            # self.status = left
        # If both horizontal and vertical directions are pressed, prioritize one
        if self.direction.x != 0 and self.direction.y != 0:
            # Prioritize horizontal movement
            if abs(self.direction.x) > abs(self.direction.y):
                self.direction.y = 0
            # Prioritize vertical movement
            else:
                self.direction.x = 0

    def move(self, speed):

        # Move counter can be BPM of Track
        if self.move_counter >= 25:
            # Every x frames, allow movement
            # Multiply hitbox x and y by the direction given from
            # input and the TILESIZE (in this case 64)
            self.hitbox.x += self.direction.x * TILESIZE
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * TILESIZE
            self.collision('vertical')
            self.rect.center = self.hitbox.center
            self.move_counter = 0
            self.pos = (round(self.hitbox.x / 64), round(self.hitbox.y / 64))
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
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):
        self.input()
        self.move(self.speed)
