import pygame
import settings
import random
from entities.projectile import Projectile

class Attack:
    duration = 6.0

    def __init__(self):
        self.time = 0

    @property
    def finished(self):
       return self.time >= self.duration

    def update(self,dt,boss,projectiles,player):
        self.time += dt
        self.run(dt,boss,projectiles,player)

    def run(self,dt,boss,projectiles,player):
        pass

class Rain(Attack):
    def __init__(self):
        super().__init__()
        self.timer = 0

    def run(self,dt,boss,projectiles,player):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = 0.10
            x = random.randint(0,settings.WIDTH)
            projectiles.append(Projectile(x, -10, 0, 450))

class Aimed(Attack):

    def __init__(self):
        super().__init__()
        self.timer = 0.5

    def run(self, dt, boss, projectiles, player):
        self.timer -= dt
        if self.timer > 0:
            return
        self.timer = 0.6

        start = pygame.Vector2(boss.pos.x + boss.SIZE / 2,boss.pos.y + boss.SIZE / 2 )
        direction = player.center - start
        if direction.length() == 0:
            return
        direction = direction.normalize()

        for angle in (-40,-20,0,20,40):
            vel = direction.rotate(angle) * 350
            projectiles.append(Projectile(start.x, start.y, vel.x, vel.y, color="orange"))

class Wall(Attack):
    def __init__(self):
        super().__init__()
        self.timer = 0.3

    def run(self,dt,boss,projectiles,player):
        self.timer -= dt
        if self.timer > 0:
            return
        self.timer = 0.5

        spacing = 30
        gap_start = random.randint(100, settings.HEIGHT - 260)
        gap_end = gap_start + 150

        y = 0
        while y <= settings.HEIGHT:
            if not (gap_start <= y <= gap_end):
                projectiles.append(Projectile(-10,y,800,0, color="purple"))
            y += spacing


