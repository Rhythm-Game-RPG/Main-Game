import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        # always need this for any kind of sprite
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2()
        # self.status = "stationary"
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            # self.status = up
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            # self.status = down
        else:
            self.direction.y = 0
            # self.status = stationary

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            # self.status = right
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            # self.status = left
        else:
            self.direction.x = 0

    def move(self, speed):
        # check if vector has a length for diagonal speed
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

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
