import random
import pygame
import settings
from entities.attacks import Rain, Aimed, Wall


class Boss:
    SIZE = 150
    PAUSE = 2

    def __init__(self, image):
        self.original = pygame.image.load(settings.asset(image)).convert_alpha()
        self.image = pygame.transform.scale(self.original, (self.SIZE, self.SIZE))
        self.pos = pygame.Vector2(settings.WIDTH / 2 - self.SIZE / 2, 50)

        self.attack_pool = [Rain, Aimed, Wall]
        self.attack = None
        self.last_attack = None
        self.pause = self.PAUSE

    def pick_attack(self):
        options = [a for a in self.attack_pool if a is not self.last_attack] or self.attack_pool
        self.last_attack = random.choice(options)
        self.attack = self.last_attack()

    def update(self, dt, projectiles, player):
        if self.attack is None:
            self.pause -= dt
            if self.pause <= 0:
                self.pick_attack()
        else:
            self.attack.update(dt, self, projectiles, player)
            if self.attack.finished:
                self.attack = None
                self.pause = self.PAUSE

    def draw(self, screen):
        screen.blit(self.image, self.pos)

