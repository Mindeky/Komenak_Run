import pygame
import settings
from levels import LEVELS
from entities.player import Player
from entities.enemy import Enemy
from entities.milk import Milk
from ui import render_text


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Komenak Run")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        # texts
        self.big_font = pygame.font.SysFont("arial", 72)
        self.small_font = pygame.font.SysFont("arial", 36)
        self.text_title = render_text(self.big_font,"KOMENAK RUN", "white")
        self.text_lost = render_text(self.big_font,"YOUR EXPELLED!!!!!!", "red")
        self.text_again = render_text(self.big_font,"AGAIN?? [space]", "white")
        self.text_next = render_text(self.big_font,"NEXT LEVEL [space]",  "white")
        self.text_paused = render_text(self.big_font,"PAUSED", "red")
        self.text_complete = render_text(self.big_font,"LEVEL COMPLETED",  "green")
        self.text_won = render_text(self.big_font,"YOU HAVE SURVIVED",  "green")
        self.overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)

        #level name
        self.banner_text = None
        self.banner_time = 0

        #menu
        self.menu_options = ["PLAY", "QUIT", "HELP"]
        self.menu_index = 0
        self.title_text =render_text(self.big_font,"KOMENAK RUN", "white", outline=4)
        self.menu_normal = [
            render_text(self.small_font, option, "white") for option in self.menu_options]
        self.menu_select = [
            render_text(self.small_font, f"> {option} < ", "yellow") for option in self.menu_options
        ]

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
        self.player_lives = settings.PLAYER_LIVES
        self.invulnerable_time = 0

        self.load_level()


        self.state = "menu"

    def load_level(self):
        level = LEVELS[self.level_index]
        self.goal = level["milk"]
        self.score = 0
        self.state = "playing"
        self.player_lives = settings.PLAYER_LIVES
        self.invulnerable_time = 0
        self.hit_sound.stop()

        count = len(level["enemies"])
        self.enemies = []
        for i, config in enumerate(level["enemies"]):
            x = settings.WIDTH * (i+1) / (count + 1)
            self.enemies.append(Enemy(x=x, **config))

        self.player.reset()
        self.milk.move_to_random_spot(self.player)

        self.banner_text = render_text(self.big_font, level["name"], "white")
        self.banner_time = 2.0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            if self.state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.menu_options[self.menu_index] == "PLAY":
                        self.state = "playing"
                    else:
                        self.running = False
                continue


            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if self.state == "playing":
                    self.state = "paused"
                elif self.state == "paused":
                    self.state = "playing"

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

        self.invulnerable_time = max(0, self.invulnerable_time - self.dt)

        self.banner_time = max(0, self.banner_time - self.dt)

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
                self.milk.move_to_random_spot(self.player)

        # collision with the enemy
        if self.invulnerable_time == 0:
            for enemy in self.enemies:
                if enemy.rect.colliderect(self.player.rect):
                    self.player_lives -= 1
                    if self.player_lives <= 0:
                        self.big_enemy = pygame.transform.scale(
                            enemy.original, (settings.WIDTH, settings.HEIGHT)
                        )
                        self.state = "lost"
                        self.hit_sound.play(-1)
                    else:
                        self.invulnerable_time = settings.INVULERABLE_TIME
                        self.player.reset()
                    break


    def draw(self):
        if self.state == "menu":
            self.screen.blit(self.big_player, (0,0))
            self.screen.blit(self.overlay, (0,0))
            self.draw_centered(self.text_title, 180)
            for i in range(len(self.menu_options)):
                text = self.menu_select[i] if i == self.menu_index else self.menu_normal[i]
                self.draw_centered(text, 320 + i * 70)

        elif self.state == "playing":
            self.screen.blit(self.background, (0, 0))
            self.milk.draw(self.screen)
            if self.invulnerable_time == 0 or int(self.invulnerable_time * 10) % 2 == 0:
                self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            name = LEVELS[self.level_index]["name"]
            score_text = render_text(
                self.small_font, f"{name}       Milk: {self.score} / {self.goal}", "white", outline=2)
            self.screen.blit(score_text, (10,10))

            bar_w, bar_h = 300, 20
            ratio = self.score / self.goal
            print(self.score, self.goal,ratio)
            pygame.draw.rect(self.screen, "black", (10, 55, bar_w + 4, bar_h + 4),border_radius=6)
            pygame.draw.rect(self.screen, "white", (12, 57, bar_w * ratio, bar_h),border_radius=6)

            if self.banner_time > 0:
                alpha = min(1,self.banner_time) * 255
                self.banner_text.set_alpha(int(alpha))
                self.draw_centered(self.banner_text, 300)

            for i in range(self.player_lives):
                pygame.draw.circle(self.screen, "red", (settings.WIDTH - 30 - i * 40,30), 14)
                pygame.draw.circle(self.screen, "white", (settings.WIDTH - 30 - i * 40, 30), 14, 2)

        elif self.state == "paused":
            self.screen.blit(self.overlay, (0, 0))
            self.draw_centered(self.text_paused, 400)

        elif self.state == "complete":
            self.screen.blit(self.big_player, (0,0)),
            self.screen.blit(self.overlay, (0,0))
            self.draw_centered(self.text_complete, 270)
            self.draw_centered(self.text_next, 530)

        elif self.state == "won":
            self.screen.blit(self.big_player, (0,0))
            self.screen.blit(self.overlay, (0, 0))
            self.draw_centered(self.text_won, 270)
            self.draw_centered(self.text_again, 530)

        else:  # lost
            self.screen.blit(self.big_enemy, (0, 0))
            self.screen.blit(self.overlay, (0, 0))
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