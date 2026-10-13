import random
import pygame
import settings


class Enemy:
    def __init__(self):
        # the image is loaded from disk only once
        self.original = pygame.image.load(settings.asset("blazej.png")).convert_alpha()
        self.reset()

    def reset(self):
        self.size = settings.ENEMY_START_SIZE
        self.pos = pygame.Vector2(settings.WIDTH / 2, settings.HEIGHT / 2)
        self.speed_x = settings.ENEMY_START_SPEED
        self.speed_y = settings.ENEMY_START_SPEED
        self.rescale_image()

    def rescale_image(self):
        self.image = pygame.transform.scale(self.original, (self.size, self.size))

    def grow(self):
        if self.size < settings.ENEMY_MAX_SIZE:
            self.size += settings.ENEMY_GROW
            self.rescale_image()

    def update(self, dt):
        self.pos.x += self.speed_x * dt
        self.pos.y += self.speed_y * dt

        # right wall
        if self.pos.x + self.size > settings.WIDTH:
            self.pos.x = settings.WIDTH - self.size
            self.speed_x = -abs(self.speed_x)
            action = random.randint(1, 4)
            if action == 1:
                self.speed_x = -min(abs(self.speed_x) + settings.ENEMY_ACCEL,
                                    settings.ENEMY_MAX_SPEED)
            if action == 2:
                self.grow()

        # left wall
        if self.pos.x < 0:
            self.pos.x = 0
            self.speed_x = abs(self.speed_x)
            action = random.randint(1, 4)
            if action == 1:
                self.speed_x = min(abs(self.speed_x) + settings.ENEMY_ACCEL,
                                   settings.ENEMY_MAX_SPEED)
            if action == 2:
                self.grow()

        # bottom wall
        if self.pos.y + self.size > settings.HEIGHT:
            self.pos.y = settings.HEIGHT - self.size
            self.speed_y = -abs(self.speed_y)
            action = random.randint(1, 4)
            if action == 1:
                self.speed_y = -min(abs(self.speed_y) + settings.ENEMY_ACCEL,
                                    settings.ENEMY_MAX_SPEED)
            if action == 2:
                self.grow()

        # top wall
        if self.pos.y < 0:
            self.pos.y = 0
            self.speed_y = abs(self.speed_y)
            action = random.randint(1, 4)
            if action == 1:
                self.speed_y = min(abs(self.speed_y) + settings.ENEMY_ACCEL,
                                   settings.ENEMY_MAX_SPEED)
            if action == 2:
                self.grow()

    @property
    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

    def draw(self, screen):
        screen.blit(self.image, self.pos)