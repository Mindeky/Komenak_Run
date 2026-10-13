import pygame
import settings
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

        # game state: "playing", "lost" or "won"
        self.state = "playing"
        self.score = 0

        # texts
        big_font = pygame.font.SysFont("arial", 72)
        self.small_font = pygame.font.SysFont("arial", 36)
        self.text_lost = big_font.render("YOU LOST!!!!!!", True, "red")
        self.text_again = big_font.render("AGAIN?? [space]", True, "black")
        self.text_won = big_font.render("LEVEL COMPLETE!", True, "green")

        # images and sound
        background = pygame.image.load(settings.asset("utekaj.jpg")).convert()
        self.background = pygame.transform.scale(
            background, (settings.WIDTH, settings.HEIGHT)
        )

        big_enemy = pygame.image.load(settings.asset("blazej.png")).convert_alpha()
        self.big_enemy = pygame.transform.scale(
            big_enemy, (settings.WIDTH, settings.HEIGHT)
        )

        self.hit_sound = pygame.mixer.Sound(settings.asset("touching.mp3"))

        # game objects
        self.player = Player(100, 100)
        self.enemy = Enemy()
        self.milk = Milk()

    def reset(self):
        self.state = "playing"
        self.score = 0
        self.player.reset()
        self.enemy.reset()
        self.milk.move_to_random_spot()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        self.player.update(self.dt, keys)
        self.enemy.update(self.dt)

        # collecting milk
        if self.milk.is_collected(self.player):
            self.score += 1
            if self.score >= settings.MILK_PER_LEVEL:
                self.state = "won"
            else:
                self.milk.move_to_random_spot()

        # collision with the enemy
        if self.enemy.rect.colliderect(self.player.rect):
            self.state = "lost"
            self.hit_sound.play()

    def draw(self):
        if self.state == "playing":
            self.screen.blit(self.background, (0, 0))
            self.milk.draw(self.screen)
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            score_text = self.small_font.render(
                f"Milk: {self.score} / {settings.MILK_PER_LEVEL}", True, "black"
            )
            self.screen.blit(score_text, (10, 10))

        elif self.state == "won":
            self.screen.blit(self.background, (0, 0))
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