import pygame
import random
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Assault")

nave_img = pygame.image.load("nave.png")
meteoro_p = pygame.image.load("meteorop.png")
meteoro_m = pygame.image.load("meteorom.png")
meteoro_g = pygame.image.load("meteorog.png")
tiro_img = pygame.image.load("tiro.png")
background_img = pygame.image.load("background.jpg")

nave_width = nave_img.get_width()
nave_height = nave_img.get_height()
tiro_width = tiro_img.get_width()
tiro_height = tiro_img.get_height()

nave_img = pygame.transform.scale(nave_img, (int(nave_width * 0.5), int(nave_height * 0.5)))

nave_width = nave_img.get_width()
nave_height = nave_img.get_height()

clock = pygame.time.Clock()


def display_text(text, font_size, color, x, y, center=False):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if center:
        x = (SCREEN_WIDTH - text_rect.width) // 2
    screen.blit(text_surface, (x, y))


def show_menu():
    while True:
        screen.fill(BLACK)
        display_text("Asteroid Assault", 64, WHITE, 0, 100, center=True)
        display_text("1. Fácil", 48, WHITE, 0, 200, center=True)
        display_text("2. Difícil", 48, WHITE, 0, 300, center=True)
        display_text("3. Star Wars", 48, WHITE, 0, 400, center=True)
        display_text("Escolha sua dificuldade (1/2/3):", 32, WHITE, 0, 500, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "facil"
                if event.key == pygame.K_2:
                    return "dificil"
                if event.key == pygame.K_3:
                    return "star_wars"


def game_loop(dificuldade):
    nave_x = SCREEN_WIDTH // 2 - nave_width // 2
    nave_y = SCREEN_HEIGHT - nave_height - 10
    nave_speed = 7

    meteoros = []

    tiros = []

    if dificuldade == "facil":
        meteoro_speed = 2
        spawn_rate = 30
    elif dificuldade == "dificil":
        meteoro_speed = 4
        spawn_rate = 20
    elif dificuldade == "star_wars":
        meteoro_speed = 6
        spawn_rate = 10

    score = 0
    game_over = False

    while not game_over:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tiros.append([nave_x + nave_width // 2 - tiro_width // 2, nave_y])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and nave_x > 10:
            nave_x -= nave_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and nave_x < SCREEN_WIDTH - nave_width:
            nave_x += nave_speed

        if random.randint(1, spawn_rate) == 1:
            meteoro_tipo = random.choice(["pequeno", "medio", "grande"])
            meteoro_x = random.randint(0, SCREEN_WIDTH - meteoro_g.get_width())

            if meteoro_tipo == "pequeno":
                meteoros.append({
                    "tipo": "pequeno",
                    "x": meteoro_x,
                    "y": -meteoro_p.get_height(),
                    "speed": meteoro_speed + 2,
                    "img": meteoro_p,
                    "pontos": 100
                })
            elif meteoro_tipo == "medio":
                meteoros.append({
                    "tipo": "medio",
                    "x": meteoro_x,
                    "y": -meteoro_m.get_height(),
                    "speed": meteoro_speed,
                    "img": meteoro_m,
                    "pontos": 200
                })
            else:
                meteoros.append({
                    "tipo": "grande",
                    "x": meteoro_x,
                    "y": -meteoro_g.get_height(),
                    "speed": meteoro_speed - 1,
                    "img": meteoro_g,
                    "pontos": 300
                })

        for meteoro in meteoros:
            meteoro["y"] += meteoro["speed"]

            if (meteoro["x"] < nave_x + nave_width and
                    meteoro["x"] + meteoro["img"].get_width() > nave_x and
                    meteoro["y"] < nave_y + nave_height and
                    meteoro["y"] + meteoro["img"].get_height() > nave_y):
                game_over = True

        meteoros = [meteoro for meteoro in meteoros if meteoro["y"] < SCREEN_HEIGHT]

        for tiro in tiros:
            tiro[1] -= 10

        tiros = [tiro for tiro in tiros if tiro[1] > 0]

        for tiro in tiros:
            for meteoro in meteoros:
                if (tiro[0] < meteoro["x"] + meteoro["img"].get_width() and
                        tiro[0] + tiro_width > meteoro["x"] and
                        tiro[1] < meteoro["y"] + meteoro["img"].get_height() and
                        tiro[1] + tiro_height > meteoro["y"]):
                    score += meteoro["pontos"]
                    meteoros.remove(meteoro)
                    tiros.remove(tiro)
                    break

        screen.blit(nave_img, (nave_x, nave_y))
        for meteoro in meteoros:
            screen.blit(meteoro["img"], (meteoro["x"], meteoro["y"]))
        for tiro in tiros:
            screen.blit(tiro_img, (tiro[0], tiro[1]))

        display_text(f"Score: {score}", 36, WHITE, 10, 10)

        pygame.display.update()
        clock.tick(60)

    show_game_over(score)


def show_game_over(score):
    while True:
        screen.fill(BLACK)
        display_text("GAME OVER", 64, RED, 0, 300, center=True)
        display_text(f"Sua pontuação: {score}", 48, WHITE, 0, 400, center=True)
        display_text("Pressione Enter para voltar ao menu", 36, WHITE, 0, 500, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


def main():
    while True:
        dificuldade = show_menu()
        game_loop(dificuldade)


if __name__ == "__main__":
    main()
