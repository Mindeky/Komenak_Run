import pygame
import random
import os

BASE_DIR = os.path.dirname(__file__)

pygame.init()
okno = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Komenak Run")
radius = 20
running = True
kolizia = False
nazive = True
clock = pygame.time.Clock()
dt = 0
akcia = 1

font = pygame.font.SysFont("arial", 72)
font_male = pygame.font.SysFont("arial", 36)
prehra = font.render("PREHRAL SI!!!!!!", True, "red")
znova = font.render("ZNOVA?? [space]", True, "black")
level_done = font.render("LEVEL DOKONCENY!", True, "green")

hrac_obrazok = pygame.image.load(os.path.join(BASE_DIR, "sayne.jpg"))
hrac_obrazok = pygame.transform.scale(hrac_obrazok, (50,50))

nepriatel_obrazok = pygame.image.load(os.path.join(BASE_DIR, "blazej.png"))
nepriatel_obrazok = pygame.transform.scale(nepriatel_obrazok, (100,100))
nepriatel_obrazok_velky = pygame.transform.scale(nepriatel_obrazok, (800,600))
nepriatel_velkost = 100

pozadie_obrazok = pygame.image.load(os.path.join(BASE_DIR, "utekaj.jpg"))
pozadie_obrazok = pygame.transform.scale(pozadie_obrazok, (800,600))

dotyk_hraca = pygame.mixer.Sound(os.path.join(BASE_DIR, "touching.mp3"))

stvorec_pos = pygame.Vector2(25,25)
stvorec_vel = 30

hrac_pos = pygame.Vector2(100,100)

nepriatel_pos = pygame.Vector2(okno.get_width() / 2, okno.get_height() / 2)
nepriatel_rych_x = 300
nepriatel_rych_y = 300
max_rych_x = 1000
max_rych_y = 1000
max_velkost = 400

# --- GULKY ---
GULKA_POLOMER = 50
GULKY_NA_LEVEL = 15
skore = 0
vyhral = False

mliecko_obrazok = pygame.image.load(os.path.join(BASE_DIR, "mlieko.png"))
mliecko_obrazok = pygame.transform.scale(mliecko_obrazok, (GULKA_POLOMER * 2, GULKA_POLOMER * 2))

def nova_gulka():
    x = random.randint(GULKA_POLOMER + 20, 800 - GULKA_POLOMER - 20)
    y = random.randint(GULKA_POLOMER + 20, 600 - GULKA_POLOMER - 20)
    return pygame.Vector2(x, y)

gulka_pos = nova_gulka()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nazive = True
                kolizia = False
                vyhral = False
                skore = 0
                hrac_pos.x = 100
                hrac_pos.y = 100
                nepriatel_pos.x = okno.get_width() / 2
                nepriatel_pos.y = okno.get_height() / 2
                nepriatel_rych_x = 300
                nepriatel_rych_y = 300
                nepriatel_velkost = 100
                nepriatel_obrazok = pygame.image.load(os.path.join(BASE_DIR, "blazej.png"))
                nepriatel_obrazok = pygame.transform.scale(nepriatel_obrazok, (100, 100))
                gulka_pos = nova_gulka()

    if nazive and not vyhral:

        keys = pygame.key.get_pressed()

        okno.blit(pozadie_obrazok, (0,0))

        okno.blit(mliecko_obrazok, (int(gulka_pos.x) - GULKA_POLOMER, int(gulka_pos.y) - GULKA_POLOMER))

        okno.blit(hrac_obrazok, (hrac_pos.x, hrac_pos.y))
        okno.blit(nepriatel_obrazok, (nepriatel_pos.x, nepriatel_pos.y))

        # Zobrazime skore
        skore_text = font_male.render(f"Mliecka: {skore} / {GULKY_NA_LEVEL}", True, "black")
        okno.blit(skore_text, (10, 10))

        nepriatel_pos.x += nepriatel_rych_x * dt
        nepriatel_pos.y += nepriatel_rych_y * dt

        if nepriatel_pos.x + nepriatel_velkost > okno.get_width():
            nepriatel_pos.x = okno.get_width() - nepriatel_velkost
            nepriatel_rych_x = -abs(nepriatel_rych_x)
            akcia = random.randint(1, 4)

            if akcia == 1:
                nepriatel_rych_x -= 50
                if abs(nepriatel_rych_x) > max_rych_x:
                    nepriatel_rych_x = -max_rych_x
                nepriatel_rych_x = -abs(nepriatel_rych_x)

            if akcia == 2 and nepriatel_velkost < max_velkost:
                nepriatel_velkost += 20
                nepriatel_obrazok = pygame.transform.scale(
                    pygame.image.load(os.path.join(BASE_DIR, "blazej.png")),
                    (nepriatel_velkost, nepriatel_velkost)
                )

            print(nepriatel_rych_x, "x vpravo")
            print(nepriatel_velkost, "velkost")


        if nepriatel_pos.x < 0:
            nepriatel_pos.x = 0
            nepriatel_rych_x = abs(nepriatel_rych_x)
            akcia = random.randint(1, 4)

            if akcia == 1:
                nepriatel_rych_x += 50
                if abs(nepriatel_rych_x) > max_rych_x:
                    nepriatel_rych_x = max_rych_x
                nepriatel_rych_x = abs(nepriatel_rych_x)

            if akcia == 2 and nepriatel_velkost < max_velkost:
                nepriatel_velkost += 20
                nepriatel_obrazok = pygame.transform.scale(
                    pygame.image.load(os.path.join(BASE_DIR, "blazej.png")),
                    (nepriatel_velkost, nepriatel_velkost)
                )

            print(nepriatel_rych_x, "x vlavo")
            print(nepriatel_velkost, "velkost")


        if nepriatel_pos.y + nepriatel_velkost > okno.get_height():
            nepriatel_pos.y = okno.get_height() - nepriatel_velkost
            nepriatel_rych_y = -abs(nepriatel_rych_y)
            akcia = random.randint(1, 4)

            if akcia == 1:
                nepriatel_rych_y -= 50
                if abs(nepriatel_rych_y) > max_rych_y:
                    nepriatel_rych_y = -max_rych_y
                nepriatel_rych_y = -abs(nepriatel_rych_y)

            if akcia == 2 and nepriatel_velkost < max_velkost:
                nepriatel_velkost += 20
                nepriatel_obrazok = pygame.transform.scale(
                    pygame.image.load(os.path.join(BASE_DIR, "blazej.png")),
                    (nepriatel_velkost, nepriatel_velkost)
                )

            print(nepriatel_rych_y, "y dole")
            print(nepriatel_velkost, "velkost")

        if nepriatel_pos.y < 0:
            nepriatel_pos.y = 0
            nepriatel_rych_y = abs(nepriatel_rych_y)
            akcia = random.randint(1, 4)

            if akcia == 1:
                nepriatel_rych_y += 50
                if abs(nepriatel_rych_y) > max_rych_y:
                    nepriatel_rych_y = max_rych_y
                nepriatel_rych_y = abs(nepriatel_rych_y)

            if akcia == 2 and nepriatel_velkost < max_velkost:
                nepriatel_velkost += 20
                nepriatel_obrazok = pygame.transform.scale(
                    pygame.image.load(os.path.join(BASE_DIR, "blazej.png")),
                    (nepriatel_velkost, nepriatel_velkost)
                )

            print(nepriatel_rych_y, "y hore")
            print(nepriatel_velkost, "velkost")

        if keys[pygame.K_UP] and hrac_pos.y > 0:
            hrac_pos.y -= 800 * dt
        if keys[pygame.K_DOWN] and hrac_pos.y + 50 < 600:
            hrac_pos.y += 800 * dt
        if keys[pygame.K_LEFT] and hrac_pos.x > 0:
            hrac_pos.x -= 800 * dt
        if keys[pygame.K_RIGHT] and hrac_pos.x + 50 < 800:
            hrac_pos.x += 800 * dt

        # Kolízia hráča s guľkou
        hrac_stred = pygame.Vector2(hrac_pos.x + 25, hrac_pos.y + 25)
        if hrac_stred.distance_to(gulka_pos) < GULKA_POLOMER + 25:
            skore += 1
            if skore >= GULKY_NA_LEVEL:
                vyhral = True
            else:
                gulka_pos = nova_gulka()

        rect_nepriatel = pygame.Rect(nepriatel_pos.x, nepriatel_pos.y, nepriatel_velkost, nepriatel_velkost)
        rect_hrac = pygame.Rect(hrac_pos.x, hrac_pos.y, 50, 50)

        if rect_nepriatel.colliderect(rect_hrac):
            if not kolizia:
                kolizia = True
        else:
            kolizia = False

        if kolizia:
            nazive = False

    elif vyhral:
        okno.blit(pozadie_obrazok, (0,0))
        okno.blit(level_done, (80, 240))
        okno.blit(znova, (225, 500))

    else:
        dotyk_hraca.play()
        okno.blit(nepriatel_obrazok_velky, (0,0))
        okno.blit(prehra, (150,240))
        okno.blit(znova, (225,500))


    pygame.display.update()

    dt = clock.tick(60) / 1000

pygame.quit()

#LEVELY :
# 1. blazkova bez powers
# 2. blazkova s powers
# 3. blazkova + chamilka
# 4. blazkova + chamilka nerfed
# 5. macura boss fight
