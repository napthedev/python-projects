import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame import mixer
from playsound import playsound
import random
import math
from tkinter import messagebox
from tkinter import *


pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("Data/ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load("Data/background.png")

background_music = mixer.music.load("Data/background.wav")
mixer.music.play(-1)

player_img = pygame.image.load("Data/player.png")


class player_class(object):
    def __init__(self, x, y, dx):
        self.x = x - 32
        self.y = y - 32
        self.dx = dx

    def draw(self):
        window.blit(player_img, (self.x, self.y))

    def update(self):
        if self.x < 0:
            self.x = 0
        elif self.x + 64 > 800:
            self.x = 736
        self.x += self.dx
        self.draw()


player = player_class(400, 480, 0)

lives = 3
lives_img = pygame.image.load("Data/life.png")


enemy_img = pygame.image.load("Data/enemy.png")


class enemy_class(object):
    def __init__(self, x, y, dy):
        self.x = x - 32
        self.y = y - 32
        self.dy = dy

    def draw(self):
        window.blit(enemy_img, (self.x, self.y))

    def update(self):
        global lives, enemies
        if self.y > 568:
            lives -= 1
            delete_index = 0
            for i in range(len(enemies)):
                if enemies[i] == self:
                    delete_index = i
            del enemies[delete_index]
            playsound("Data/wrong.wav", False)
        self.y += self.dy
        self.draw()


spawning_time = 1
enemies = []
enemies.append(enemy_class(random.randint(32, 768), -32, 0.05))


bullet_img = pygame.image.load("Data/bullet.png")


class bullet_class(object):
    def __init__(self, x, y, dy):
        self.x = x - 8
        self.y = y - 8
        self.dy = dy

    def draw(self):
        window.blit(bullet_img, (self.x, self.y))

    def update(self):
        global bullet_status, enemies, score
        enemies_delete = []
        for i in range(len(enemies)):
            distance = math.hypot(enemies[i].x + 24 - self.x, enemies[i].y - self.y) - 32
            if distance < 1:
                bullet_status = True
                self.x = -100
                self.y = -100
                enemies_delete.append(i)
                score += 1
                playsound("Data/explosion.wav", False)
        for i in enemies_delete:
            del enemies[i]

        if self.y - 8 < 0:
            bullet_status = True
        self.y += self.dy
        self.draw()


bullet_status = True
bullet = bullet_class(-100, -100, -1)

font = pygame.font.Font('freesansbold.ttf', 32)
score = 0

running = True
msg_box = True
while running:
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            msg_box = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.dx = -0.3
            elif event.key == pygame.K_RIGHT:
                player.dx = 0.3
            elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                if bullet_status:
                    bullet.x = player.x + 24
                    bullet.y = player.y
                    bullet_status = False
                    playsound("Data/laser.wav", False)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.dx = 0

    if lives == 3:
        window.blit(lives_img, (680, 10))
        window.blit(lives_img, (720, 10))
        window.blit(lives_img, (760, 10))
    elif lives == 2:
        window.blit(lives_img, (680, 10))
        window.blit(lives_img, (720, 10))
    elif lives == 1:
        window.blit(lives_img, (680, 10))
    else:
        running = False

    spawning_time -= 0.001
    if spawning_time <= 0:
        enemies.append(enemy_class(random.randint(32, 764), -64, 0.05 + score * 0.005))
        spawning_time = 1 - score * 0.01
    player.update()
    for enemy in enemies:
        enemy.update()
    bullet.update()

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(text, (10, 10))

    pygame.display.update()


if msg_box:
    playsound("Data/lose.wav", False)
    tk = Tk()
    tk.withdraw()
    messagebox.showerror("You lose", f"Game over! Your score: {score}")
