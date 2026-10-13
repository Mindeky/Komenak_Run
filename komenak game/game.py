import pygame
import settings
from levels import LEVELS
from entities.player import Player
from entities.enemy import Enemy
from entities.milk import Milk


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Komenak Run")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        # texts
        big_font = pygame.font.SysFont("arial", 72)
        self.small_font = pygame.font.SysFont("arial", 36)
        self.text_lost = big_font.render("YOUR EXPELLED!!!!!!", True, "red")
        self.text_again = big_font.render("AGAIN?? [space]", True, "black")
        self.text_next = big_font.render("NEXT LEVEL?? [n]", True, "black")
        self.text_won = big_font.render("YOU'VE SURVIVED", True, "green")





        # images and sound
        background = pygame.image.load(settings.asset("utekaj.jpg")).convert()
        self.background = pygame.transform.scale(
            background, (settings.WIDTH, settings.HEIGHT)
        )

        self.big_enemy = None

        big_player = pygame.image.load(settings.asset("sayne.jpg")).convert_alpha()
        self.big_player = pygame.transform.scale(
            big_player, (settings.WIDTH, settings.HEIGHT)
        )

        self.hit_sound = pygame.mixer.Sound(settings.asset("touching.mp3"))

        # game objects
        self.player = Player(100, 100)
        self.milk = Milk()
        self.enemies = []

        # level state

        self.level_index = 0
        self.score = 0
        self.goal = 0
        self.state = "playing"
        self.load_level()

    def load_level(self):
        level = LEVELS[self.level_index]
        self.goal = level["milk"]
        self.score = 0
        self.state = "playing"

        count = len(level["enemies"])
        self.enemies = []
        for i, config in enumerate(level["enemies"]):
            x = settings.WIDTH * (i+1) / (count + 1)
            self.enemies.append(Enemy(x=x, **config))

    def reset(self):
        self.hit_sound.stop()
        self.state = "playing"
        self.score = 0
        self.player.reset()
        self.enemy.reset()
        self.milk.move_to_random_spot()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.state == "lost":
                    self.load_level()
                if self.state == "complete":
                    self.level_index += 1
                    self.load_level()
                if self.state == "won":
                    self.level_index = 0
                    self.load_level()

    def update(self):
        if self.state != "playing":
            return

        self.hit_sound.stop()

        keys = pygame.key.get_pressed()
        self.player.update(self.dt, keys)
        for enemy in self.enemies:
            enemy.update(self.dt)

        # collecting milk
        if self.milk.is_collected(self.player):
            self.score += 1
            if self.score >= self.goal:
                if self.level_index == len(LEVELS) - 1:
                    self.state = "won"
                else:
                    self.state = "complete"
            else:
                self.milk.move_to_random_spot()

        # collision with the enemy
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.big_enemy = pygame.transform.scale(
                    enemy.original, (settings.WIDTH, settings.HEIGHT)
                )
                self.state = "lost"
                self.hit_sound.play(-1)
                break

    def draw(self):
        if self.state == "playing":
            self.screen.blit(self.background, (0, 0))
            self.milk.draw(self.screen)
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            name = LEVELS[self.level_index]["name"]
            score_text = self.small_font.render(
                f"{name}    Milk: {self.score} / {self.goal}", True, "black"
            )
            self.screen.blit(score_text, (10, 10))

        elif self.state == "complete":
            self.screen.blit(self.big_player, (0,0)),
            self.draw_centered(self.text_won, 270)
            self.draw_centered(self.text_again, 530)

        elif self.state == "won":
            self.screen.blit(self.big_player, (0,0)),
            self.draw_centered(self.text_won, 270)
            self.draw_centered(self.text_again, 530)

        else:  # lost
            self.screen.blit(self.big_enemy, (0, 0))
            self.draw_centered(self.text_lost, 270)
            self.draw_centered(self.text_again, 530)

        pygame.display.update()

    def draw_centered(self, text, y):
        rect = text.get_rect(center=(settings.WIDTH // 2, y))
        self.screen.blit(text, rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(settings.FPS) / 1000
        pygame.quit()