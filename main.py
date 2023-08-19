import pygame
import math
import os
import time
from random import randint

# Initialize the pygame
pygame.init()
FPS = 120
CLOCK = pygame.time.Clock()


# Create the screen
SCREEN = pygame.display.set_mode((800, 600))

# BACKGROUND
BACKGROUND = pygame.image.load(os.path.join("space_invader_project/assets", "background.png"))


# Title and Icon
pygame.display.set_caption("Space Invader")
ICON = pygame.image.load(os.path.join("space_invader_project/assets", "ufo.png"))
pygame.display.set_icon(ICON)

# score
score_value = 0
FONT = pygame.font.Font("freesansbold.ttf", 32)
TEST_X = 10
TEST_Y = 10


def show_score(x, y):
    score = FONT.render("Score: " + str(score_value), True, (255, 255, 255))
    SCREEN.blit(score, (x, y))


# Game over
GAME_OVER_FONT = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    game_over = GAME_OVER_FONT.render("GAME OVER", True, (255, 255, 255))
    SCREEN.blit(game_over, (200, 250))


# Player
player_img = pygame.image.load(os.path.join("space_invader_project/assets", "spaceship.png"))
playerX = 370
playerY = 480
change_playerX = 0


def player(x, y):
    SCREEN.blit(player_img, (x, y))


# Alien
alien_img = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alien_down = []
num_aliens = 6
for i in range(num_aliens):
    alien_img.append(pygame.image.load("space_invader_project/assets\\alien.png"))
    alienX.append(randint(0, 735))
    alienY.append(randint(50, 150))
    alienX_change.append(1)
    alienY_change.append(40)
    alien_down.append(False)

def alien(x, y):
    SCREEN.blit(alien_img[i], (x, y))

# Boss
boss_img = []
bossX = []
bossY = []
bossX_change = 1.5
bossY_change = []

boss_img.append(pygame.image.load("space_invader_project/assets\\boss.png"))
bossX.append(300)
bossY.append(30)

def boss(x, y):
    SCREEN.blit(boss_img[0], (x, y))



# Bullet
bullet_img = pygame.image.load("space_invader_project/assets\\bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8.5
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    SCREEN.blit(bullet_img, (x + 16, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(
        (math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2))
    )
    if distance < 27:
        return True
    return False


# The program
running = True
while running:
    # Clock
    CLOCK.tick(FPS)

    # RGB
    SCREEN.fill((0, 0, 0))

    # BACKGROUND
    SCREEN.blit(BACKGROUND, (0, 0))

    # Check if not quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawning enemies
    for i in range(num_aliens):
        # Game Over
        if alienY[i] > 440:
            for j in range(num_aliens):
                alienY[j] = 9999
            game_over_text()
            break

        alienX[i] += alienX_change[i]

        if alienX[i] > 736:
            alienX_change[i] *= -1
            alienX[i] = 736
            alienY[i] += alienY_change[i]
        elif alienX[i] < 0:
            alienX_change[i] *= -1
            alienX[i] = 0
            alienY[i] += alienY_change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            alienX[i] = randint(0, 735)
            alienY[i] = randint(50, 150)
            score_value += 1
        alien(alienX[i], alienY[i])

    # Spawning Boss
    if score_value > 1:
        num_aliens = 0
        boss(bossX[0], bossY[0])

    bossX[0] += bossX_change

    if bossX[0] > 600:
        bossX_change *= -1
        bossX[0] = 600
    elif bossX[0] < 0:
        bossX_change *= -1
        bossX[0] = 0

    # Player
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            change_playerX = -2
        if event.key == pygame.K_RIGHT:
            change_playerX = 2
        if event.key == pygame.K_CAPSLOCK and bullet_state == "ready":
            bulletX = playerX
            fire_bullet(bulletX, bulletY)

    if event.type == pygame.K_UP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            change_playerX = 1
    playerX += change_playerX

    if playerX <= 10 or playerX >= 726:
        change_playerX *= -1

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(TEST_X, TEST_Y)
    pygame.display.update()
