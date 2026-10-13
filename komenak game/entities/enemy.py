import random
import pygame
import settings
from settings import ENEMY_START_SPEED, ENEMY_MAX_SPEED, ENEMY_MAX_SIZE


class Enemy:
    def __init__(self,image,x=settings.WIDTH / 2, powers=True,
                 start_speed = ENEMY_START_SPEED,
                 max_speed = ENEMY_MAX_SPEED,
                 max_size = ENEMY_MAX_SIZE):
        self.original = pygame.image.load(settings.asset(image)).convert_alpha()
        self.start_x = x
        self.powers = powers
        self.start_speed = start_speed
        self.max_speed = max_speed
        self.max_size = max_size
        self.reset()

    def reset(self):
        self.size = settings.ENEMY_START_SIZE
        self.pos = pygame.Vector2(self.start_x, settings.HEIGHT / 2)
        self.speed_x = self.start_speed
        self.speed_y = self.start_speed
        self.rescale_image()

    def rescale_image(self):
        self.image = pygame.transform.scale(self.original, (self.size, self.size))

    def grow(self):
        if self.size < self.max_size:
            self.size += settings.ENEMY_GROW
            self.rescale_image()

    def random_action(self):
        if not self.powers:
            return 0
        return random.randint(1, 4)

    def update(self, dt):
        self.pos.x += self.speed_x * dt
        self.pos.y += self.speed_y * dt

        # right wall
        if self.pos.x + self.size > settings.WIDTH:
            self.pos.x = settings.WIDTH - self.size
            self.speed_x = -abs(self.speed_x)
            action = self.random_action()
            if action == 1:
                self.speed_x = -min(abs(self.speed_x) + settings.ENEMY_ACCEL,
                                        self.max_speed)
            if action == 2:
                self.grow()

        # left wall
        if self.pos.x < 0:
            self.pos.x = 0
            self.speed_x = abs(self.speed_x)
            action = self.random_action()
            if action == 1:
                self.speed_x = min(abs(self.speed_x) + settings.ENEMY_ACCEL,
                                       self.max_speed)
            if action == 2:
                self.grow()

        # bottom wall
        if self.pos.y + self.size > settings.HEIGHT:
            self.pos.y = settings.HEIGHT - self.size
            self.speed_y = -abs(self.speed_y)
            action = self.random_action()
            if action == 1:
                self.speed_y = -min(abs(self.speed_y) + settings.ENEMY_ACCEL,
                                        self.max_speed)
            if action == 2:
                self.grow()

        # top wall
        if self.pos.y < 0:
            self.pos.y = 0
            self.speed_y = abs(self.speed_y)
            action = self.random_action()
            if action == 1:
                self.speed_y = min(abs(self.speed_y) + settings.ENEMY_ACCEL,
                                       self.max_speed)
            if action == 2:
                self.grow()

    @property
    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

    def draw(self, screen):
        screen.blit(self.image, self.pos)