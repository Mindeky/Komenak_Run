import pygame
import settings

class Projectile:
    def __init__(self, x, y, vx, vy, radius=10, color="red"):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)
        self.radius = radius
        self.color = color

    def update(self, dt):
        self.pos += self.vel * dt

    @property
    def rect(self):
        r = self.radius
        return pygame.Rect(self.pos.x - r, self.pos.y - r, r * 2, r * 2)

    def is_offscreen(self):
        margin = 50
        return (self.pos.x < -margin or self.pos.x > settings.WIDTH + margin
                or self.pos.y < -margin or self.pos.y > settings.HEIGHT + margin)

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        pygame.draw.circle(screen, "white", self.pos, self.radius, 2)
