import pygame
import random
import settings

COLORS = {"shield": "blue", "slowE": "lightblue", "fastP": "orange"}
RADIUS = 20

class Powerup():
    def __init__(self, kind):
        self.kind = kind
        self.lifetime = 8.0
        self.pos = pygame.Vector2(0,0)
        self.move_to_random_spot()

    def move_to_random_spot(self):
        margin = RADIUS + 20
        self.pos.x = random.randint(margin, settings.WIDTH - margin)
        self.pos.y = random.randint(margin, settings.HEIGHT - margin)

    def update(self, dt):
        self.lifetime = max(0, self.lifetime - dt)

    def expired(self):
        return self.lifetime == 0

    def is_collected(self, player):
        reach = RADIUS + settings.PLAYER_SIZE / 2
        return player.center.distance_to(self.pos) < reach

    def draw(self, screen):
        pygame.draw.circle(screen, COLORS[self.kind], self.pos, RADIUS)
        pygame.draw.circle(screen, "white", self.pos, RADIUS, 2)
