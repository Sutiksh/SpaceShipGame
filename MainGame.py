import pygame, os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGTH = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Spaceship Game")
WHITE = (255, 255, 255)
SKYBLUE = (100, 100, 255)
SPACE = (23, 23, 23)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
BULLET_VEL = 8
MAX_BULLETS = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BORDER = pygame.Rect(445, 0, 10, 500)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90,
)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270,
)
SPACE_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGTH)
)


def draw_window(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth):
    WIN.blit(SPACE_IMAGE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    red_Health_text = HEALTH_FONT.render("Health: " + str(redHealth), 1, WHITE)
    yellow_Health_text = HEALTH_FONT.render("Health: " + str(yellowHealth), 1, WHITE)
    WIN.blit(yellow_Health_text, (10, 10))
    WIN.blit(red_Health_text, (WIDTH - red_Health_text.get_width() - 10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellowBullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_movement(yellow, keys_pressed):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width <= BORDER.x + 6:
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGTH - 10:
        yellow.y += VEL


def red_movement(red, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + 15:
        red.x -= VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width <= WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGTH - 10:
        red.y += VEL


def handle_bullets(yellowBullets, yellow, redBullets, red):
    for bullet in yellowBullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellowBullets.remove(bullet)

    for bullet in redBullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redBullets.remove(bullet)
        elif bullet.x < 0:
            redBullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH // 2 - draw_text.get_width() // 2,
            HEIGTH // 2 - draw_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(600, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    redBullets = []
    yellowBullets = []

    redHealth = 10
    yellowHealth = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowBullets) < MAX_BULLETS:
                    ybullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + (yellow.height // 2) - 2,
                        10,
                        5,
                    )
                    yellowBullets.append(ybullet)
                    BULLET_FIRE_SOUND.play()

                elif event.key == pygame.K_RCTRL and len(redBullets) < MAX_BULLETS:
                    rbullet = pygame.Rect(
                        red.x,
                        red.y + (red.height // 2) - 2,
                        10,
                        5,
                    )
                    redBullets.append(rbullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                redHealth -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellowHealth -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if redHealth < 0:
            winner_text = "Yellow Wins!!"

        if yellowHealth < 0:
            winner_text = "Red Wins!!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # print(yellowBullets)
        # print(redBullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(yellow, keys_pressed)
        red_movement(red, keys_pressed)

        handle_bullets(yellowBullets, yellow, redBullets, red)
        draw_window(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth)

    main()


if __name__ == "__main__":
    main()
