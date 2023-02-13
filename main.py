import pygame
import random
import math

from pygame import display
from pygame import image
from pygame import font
from pygame import mixer

# Initialize the Pygame
pygame.init()

# Create the screen
screen = display.set_mode((800, 600))
# Caption and icon
display.set_caption("DH PyGame")
icon = image.load("ufo.png")
display.set_icon(icon)
# Background
background = image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

# Player
playerImg = image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemy = 6
for i in range(numOfEnemy):
    enemyImg.append(image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet
bulletImg = image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
# Ready: the bullet hasn't be fired yet so we can't see it on screen
# Fire: the bullet is moving
bulletState = "ready"

def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Score
score = 0
scorefont = font.Font("freesansbold.ttf", 32)
testX = 10
testY = 10

def showScore(x, y):
    scoreImg = scorefont.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreImg, (x, y))

# Game over text
overFont = font.Font("freesansbold.ttf", 64)
def gameOver():
    overText = overFont.render("Game over", True, (255, 255, 255))
    screen.blit(overText, (200, 250))

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Space ship movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(numOfEnemy):
        enemyX[i] += enemyX_change[i]
        if enemyX [i]<= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        # Game over
        if (enemyY[i] > 500):
            for j in range(numOfEnemy):
                enemyY[j] = 1000
            gameOver()
            break
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bulletState = "ready"
            score += 10
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletState = "ready"
        bulletY = 480
    if bulletState == "fire":
        screen.blit(bulletImg, (bulletX + 16, bulletY + 10))
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(testX, testY)
    display.update()
