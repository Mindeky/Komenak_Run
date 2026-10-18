import pygame
import levels
import settings
import random
from levels import LEVELS
from entities.player import Player
from entities.enemy import Enemy
from entities.boss import Boss
from entities.milk import Milk
from entities.powerups import Powerup
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
        self.text_again = render_text(self.big_font,"Try again? [space]", "white")
        self.text_next = render_text(self.big_font,"Next level [space]",  "white")
        self.text_paused = render_text(self.big_font,"PAUSED", "red")
        self.text_complete = render_text(self.big_font,"LEVEL COMPLETED",  "green")
        self.text_won = render_text(self.big_font,"YOU ESCAPED !!!",  "green")
        self.overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)

        #help
        help_font = pygame.font.SysFont("arial", 28)
        help_text = [
            "Move with Arrow keys ",
            "Pause the game with P",
            "Fast quit ESC (keep this in mind)",
            "Collect all milks to finish a level",
            "Touching the enemy costs you a life",
            "If the enemy touches you multiple times, i wish you luck",
            
            "Power ups:",
            "   Blue: shield - invulnerable to the enemy",
            "   Green: slowness - slows the enemy",
            "   Orange: speed - speed boost",
        ]
        self.help_lines = [render_text(help_font, t, "white", outline=2) for t in help_text]
        self.text_help_lines = render_text(self.big_font, "HELP", "white", outline=4)
        self.text_back = render_text(help_font, "[return] BACK", "white", outline=2)

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
        self.player = Player(370, 200)
        self.milk = Milk()
        self.boss = None
        self.enemies = []

        self.shield_time = 0
        self.powerup = None
        self.powerup_timer = settings.POWERUP_SPAWN_TIME
        self.powerup_kinds = []

        self.projectiles = []


        # level state
        self.level_index = 0
        self.score = 0
        self.goal = 0
        self.state = "playing"
        self.player_lives = settings.PLAYER_LIVES
        self.invulnerable_time = 0
        self.effects = {"slowE": 0, "fastP": 0}

        self.load_level()


        self.state = "menu"

    def load_level(self):
        level = LEVELS[self.level_index]
        self.goal = level["milk"]
        self.score = 0
        self.state = "playing"
        self.player_lives = settings.PLAYER_LIVES
        self.invulnerable_time = 0
        self.effects = {"slowE": 0, "fastP": 0}
        self.powerup_kinds = level.get("powerups", [])
        self.powerup = None
        self.powerup_timer = settings.POWERUP_SPAWN_TIME
        self.projectiles = []
        self.boss = Boss(**level["boss"]) if "boss" in level else None

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

            if self.state == "help":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.state = "menu"
                continue

            if self.state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    choice = self.menu_options[self.menu_index]
                    if choice == "PLAY":
                        self.state = "playing"
                    elif choice == "HELP":
                        self.state = "help"
                    elif choice == "QUIT":
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
        self.powerup_timer = max(0, self.powerup_timer - self.dt)
        self.shield_time = max(0, self.shield_time - self.dt)
        for name in self.effects:
            self.effects[name] = max(0,self.effects[name] - self.dt)

        player_dt = self.dt * (settings.SPEED_ABILITY if self.effects["fastP"] > 0 else 1)
        enemy_dt = self.dt * (settings.SLOW_ABILITY if self.effects["slowE"] > 0 else 1)

        keys = pygame.key.get_pressed()
        self.player.update(player_dt, keys)
        for enemy in self.enemies:
            enemy.update(enemy_dt)
        for i in range(len(self.enemies)):
            for j in range(i + 1,len(self.enemies)):
                self.enemies[i].bounce(self.enemies[j])

        for p in self.projectiles:
            p.update(self.dt)
        self.projectiles = [p for p in self.projectiles if not p.is_offscreen()]

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

        if self.powerup_kinds and self.powerup is None and self.powerup_timer == 0:
            self.powerup = Powerup(random.choice(self.powerup_kinds))
            self.powerup_timer = settings.POWERUP_SPAWN_TIME

        if self.powerup:
            self.powerup.update(self.dt)
            if self.powerup.is_collected(self.player):
                self.apply_powerup(self.powerup.kind)
                self.powerup = None
            elif self.powerup.expired():
                self.powerup = None

        # collision with the enemy
        if self.invulnerable_time == 0 and self.shield_time == 0:
            for enemy in self.enemies:
                if enemy.rect.colliderect(self.player.rect):
                    self.hit_player(enemy.original)
                    break
            else:
                for p in self.projectiles:
                    if p.rect.colliderect(self.player.rect):
                        self.projectiles.remove(p)
                        self.hit_player(self.boss.original if self.boss else self.enemies[0].original)
                        break

        #FINAL BOSS
        if self.boss:
            self.boss.update(enemy_dt, self.projectiles, self.player)

    def hit_player(self,image):
        self.player_lives -= 1
        if self.player_lives <= 0:
            self.big_enemy = pygame.transform.scale(image, (settings.WIDTH, settings.HEIGHT))
            self.state = "lost"
            self.hit_sound.play(-1)
        else:
            self.invulnerable_time = settings.INVULERABLE_TIME
            self.player.reset()


    def apply_powerup(self, kind):
        if kind == "shield":
            self.shield_time = settings.POWERUP_DURATION
        elif kind == "slowE":
            self.effects["slowE"] = settings.POWERUP_DURATION
        elif kind == "fastP":
            self.effects["fastP"] = settings.POWERUP_DURATION

    def draw(self):
        if self.state == "menu":
            self.screen.blit(self.big_player, (0,0))
            self.screen.blit(self.overlay, (0,0))
            self.draw_centered(self.text_title, 180)
            for i in range(len(self.menu_options)):
                text = self.menu_select[i] if i == self.menu_index else self.menu_normal[i]
                self.draw_centered(text, 320 + i * 70)

        elif self.state == "help":
            self.screen.blit(self.big_player, (0,0))
            self.screen.blit(self.overlay, (0,0))
            self.draw_centered(self.text_help_lines, 70)
            for i, line in enumerate(self.help_lines):
                self.draw_centered(line, 160 + i * 45)
                self.screen.blit(self.text_back, (600,10))

        elif self.state == "playing":
            self.screen.blit(self.background, (0, 0))
            self.milk.draw(self.screen)
            if self.powerup:
                self.powerup.draw(self.screen)
            if self.invulnerable_time == 0 or int(self.invulnerable_time * 10) % 2 == 0:
                self.player.draw(self.screen, self.shield_time > 0)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            if self.boss:
                self.boss.draw(self.screen)
            for p in self.projectiles:
                p.draw(self.screen)

            name = LEVELS[self.level_index]["name"]
            score_text = render_text(
                self.small_font, f"{name}       Milk: {self.score} / {self.goal}", "white", outline=2)
            self.screen.blit(score_text, (10,10))

            if not self.boss:
                bar_w, bar_h = 300, 20
                ratio = self.score / self.goal
                pygame.draw.rect(self.screen, "black", (10, 55, bar_w + 4, bar_h + 4),border_radius=6)
                pygame.draw.rect(self.screen, "white", (12, 57, bar_w * ratio, bar_h),border_radius=6)

            active = [
                ("Shield", self.shield_time,"blue"),
                ("Slowness", self.effects["slowE"], "lightblue"),
                ("Speed", self.effects["fastP"], "orange"),
            ]
            y = 90
            for label, remaining, color in active:
                if remaining > 0:
                    pygame.draw.circle(self.screen, color, (25, y + 12), 10)
                    pygame.draw.circle(self.screen, "white", (25, y + 12), 10,2)
                    text = render_text(self.small_font, f"{label} {remaining:.1f}s", "white", outline=2)
                    self.screen.blit(text, (45, y - 6))
                    y += 40

            if self.banner_time > 0:
                alpha = min(1,self.banner_time) * 255
                self.banner_text.set_alpha(int(alpha))
                self.draw_centered(self.banner_text, 300)

            for i in range(self.player_lives):
                pygame.draw.circle(self.screen, "red", (settings.WIDTH - 30 - i * 40,30), 14)
                pygame.draw.circle(self.screen, "white", (settings.WIDTH - 30 - i * 40, 30), 14, 2)

            if self.boss:
                hp_ratio = 1 - self.score / self.goal
                bar_w = 600
                x = (settings.WIDTH - bar_w) // 2
                y = settings.HEIGHT - 30
                pygame.draw.rect(self.screen, "black", (x - 2,y - 2, bar_w + 4, 24),border_radius=6)
                if hp_ratio > 0:
                    pygame.draw.rect(self.screen, "red", (x, y, bar_w * hp_ratio, 20), border_radius=6)
                label = render_text(self.small_font, "BOSS", "white", outline=2)
                self.screen.blit(label, (x, y - 42))

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