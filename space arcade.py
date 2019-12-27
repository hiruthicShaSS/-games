import pygame
import random
import time
import math
from pygame import mixer

cnt = 0

pygame.init()
"""                            wi dth - height"""
screen = pygame.display.set_mode((800, 600))
# BG = pygame.image.load('bgEarth.jpg')
BG_ = []
explode = []
try:
    for name in range(1, 215):
        file = f'frame/frame ({name}).jpg'
        BG_.append(file)
    for name in range(1, 22524):
        file = f'frame/frames ({name}).jpg'
        BG_.append(file)
    for name in range(215, 4750):
        file = f'frame/frame ({name}).jpg'
        BG_.append(file)
    for name in range(1, 1237):
        file = f'frame/dami/dami ({name}).jpg'
        BG_.append(file)
    for missile in range(1, 1087):
        file = f'missile/missile ({missile}).jpg'
        BG_.append(file)
    print(BG_[-1])
except pygame.error:
    print("Something went wrong while reading the file")
print("<= = = Background loaded successfully = = =>")

bg_sound = mixer.Sound("sounds/bg.wav")
bg_sound.play()

pygame.display.set_caption('                                                                                                        space invaders')
ICON = pygame.image.load('img/favicon.ico')
pygame.display.set_icon(ICON)

# player
playerImg = pygame.image.load('img/craft.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
NUM_OF_ENEMIES = 6

for i in range(NUM_OF_ENEMIES):
    enemyImg.append(pygame.image.load('img/ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.7)
    enemyY_change = 40

# bullet
bulletImg = pygame.image.load('img/bullets.png')
sparkImg = pygame.image.load('img/stars.png')
bulletX = 0
bulletY = 80
bulletX_change = 1
bulletY_change = 15
bullet_state = "ready"

# missile
missileImg = pygame.image.load("img/missile.png")
missileX = 0
missileY = 20
missileX_change = 1
missileY_change = 1
missile_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

over = pygame.font.Font("freesansbold.ttf", 10)


def display_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))
    # print(str(x) +" "+ str(y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 2, y + 10))
    screen.blit(bulletImg, (x + 40, y + 20))
    screen.blit(sparkImg, (x + 2 + random.randint(1, 10), y + 25 + random.randint(1, 10)))
    screen.blit(sparkImg, (x + 40 + random.randint(1, 10), y + 25 + random.randint(1, 10)))


def fire_missile(x, y):
    global missile_state
    global running
    global BG_
    missile_state = "fire"
    screen.blit(missileImg, (x + 2, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX + 15 - bulletX + 3, 2)) + (math.pow(enemyY + 3 - bulletY + 3, 2)))
    distance1 = math.sqrt((math.pow(enemyX - 15 - bulletX - 3, 2)) + (math.pow(enemyY - 3 - bulletY - 3, 2)))
    if distance < 27 or distance1 < 27:
        return True
    return False


def game_over():
    over_score = f"SCORE: {score_value}"
    over_dis = font.render("GAME OVER!", True, (255, 255, 255))
    over_score = font.render(over_score, True, (255, 255, 255))
    screen.blit(over_dis, (200, 250))
    screen.blit(over_score, (250, 300))

def delete_all():
    mixer.Sound.set_volume(bg_sound, 10)
    blast_sound = mixer.Sound("sounds/blast.wav")
    mixer.Sound.set_volume(blast_sound, 100)
    blast_sound.play()
    global playerImg, enemyX, missileImg, bulletX_change, cnt
    for i in range(NUM_OF_ENEMIES):
        enemyX[i] = 1000
        playerImg = pygame.image.load("img/trans.png")
        missileImg = pygame.image.load("img/trans.png")
        screen.blit(playerImg, (0, 0))
        pygame.mixer.Sound.stop(missile_sound)

    bulletX_change = 1000
    if cnt < 28508:
        cnt = 28508



running = True
while running:
    BG = pygame.image.load(BG_[cnt])
    screen.fill((255, 255, 255))
    if missile_state == "fire":
        screen.blit(BG, (missileX, missileY))
    screen.blit(BG, (0, 0))
    # playerY -= 0.1
    # playerX -= 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("sounds/shot.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                if missile_state == "ready":
                    missileX = playerX
                    fire_missile(missileX, 0)
                    if missileY == 20:
                        continue
                    else:
                        missile_sound = mixer.Sound("sounds/alert.wav")
                        missile_sound.play()

    playerX += playerX_change

    # player movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missileY == 188:
        missileY = 480
        delete_all()



    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    player(playerX, playerY)

    # enemy movement
    for i in range(NUM_OF_ENEMIES):

        # game over
        if enemyY[i] > 440:
            for j in range(NUM_OF_ENEMIES):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if int(enemyX[i]) <= 0:
            enemyX_change[i] += 0.7
            enemyY[i] += enemyY_change
        elif int(enemyX[i]) >= 736:
            enemyX_change[i] -= 0.7
            enemyY[i] += enemyY_change

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision = mixer.Sound("sounds/bomb.wav")
            collision.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
        display_score(textX, textY)
    cnt += 1
    pygame.display.update()
