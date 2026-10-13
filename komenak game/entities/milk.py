import random
import pygame
import settings


class Milk:
    def __init__(self):
        image = pygame.image.load(settings.asset("mlieko.png")).convert_alpha()
        diameter = settings.MILK_RADIUS * 2
        self.image = pygame.transform.scale(image, (diameter, diameter))
        self.pos = pygame.Vector2(0, 0)
        self.move_to_random_spot()

    def move_to_random_spot(self):
        margin = settings.MILK_RADIUS + 20
        self.pos.x = random.randint(margin, settings.WIDTH - margin)
        self.pos.y = random.randint(margin, settings.HEIGHT - margin)

    def is_collected(self, player):
        reach = settings.MILK_RADIUS + settings.PLAYER_SIZE / 2
        return player.center.distance_to(self.pos) < reach

    def draw(self, screen):
        r = settings.MILK_RADIUS
        screen.blit(self.image, (self.pos.x - r, self.pos.y - r))