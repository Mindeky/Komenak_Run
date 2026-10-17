import pygame
import settings


class Player:
    def __init__(self, x, y):
        image = pygame.image.load(settings.asset("sayne.jpg")).convert()
        self.image = pygame.transform.scale(
            image, (settings.PLAYER_SIZE, settings.PLAYER_SIZE)
        )
        self.image_shield = self.image.copy()
        self.image_shield.fill((0,80,160))
        self.start_x = x
        self.start_y = y
        self.pos = pygame.Vector2(x, y)

    def reset(self):
        self.pos = pygame.Vector2(self.start_x, self.start_y)

    def update(self, dt, keys):
        step = settings.PLAYER_SPEED * dt
        if keys[pygame.K_UP] and self.pos.y > 0:
            self.pos.y -= step
        if keys[pygame.K_DOWN] and self.pos.y + settings.PLAYER_SIZE < settings.HEIGHT:
            self.pos.y += step
        if keys[pygame.K_LEFT] and self.pos.x > 0:
            self.pos.x -= step
        if keys[pygame.K_RIGHT] and self.pos.x + settings.PLAYER_SIZE < settings.WIDTH:
            self.pos.x += step

    @property
    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y,
                           settings.PLAYER_SIZE, settings.PLAYER_SIZE)

    @property
    def center(self):
        half = settings.PLAYER_SIZE / 2
        return pygame.Vector2(self.pos.x + half, self.pos.y + half)

    def draw(self, screen, shielded= False):
        image = self.image_shield if shielded else self.image
        screen.blit(image, self.pos)