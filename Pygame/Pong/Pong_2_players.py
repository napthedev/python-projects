import pygame
from pygame import mixer
import random
from tkinter import *
from tkinter import messagebox
from playsound import playsound

pygame.init()
window = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)
background_music = mixer.music.load("Data/background.wav")
mixer.music.play(-1)


increament = 0


class player_object(object):
    def __init__(self, x, y, dy, score):
        self.x = x
        self.y = y
        self.dy = dy
        self.score = score

    def draw(self):
        pygame.draw.rect(window, (255, 255, 255), (self.x - 10, self.y - 50, 20, 100))

    def update(self):
        global delay
        if delay < 0:
            self.y += self.dy

            if self.y - 50 < 0:
                self.y = 50
            elif self.y + 50 > 500:
                self.y = 450

        self.draw()


player1 = player_object(50, 250, 0, 0)
player2 = player_object(750, 250, 0, 0)


class ball_object(object):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def draw(self):
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), 10)

    def update(self):
        global delay, player1, player2, increament
        if delay < 0:
            if self.dx >= 0:
                self.x += self.dx + increament
            else:
                self.x += self.dx - increament
            if self.dy >= 0:
                self.y += self.dy + increament
            else:
                self.y += self.dy - increament

            if self.y - 10 < 0:
                self.y = 10
                self.dy = -self.dy
                playsound("Data/bounce.wav", False)
            elif self.y + 10 > 500:
                self.y = 490
                self.dy = -self.dy
                playsound("Data/bounce.wav", False)
            elif self.x - 10 < 0:
                self.x = 400
                self.y = 250
                player1.y = 250
                player2.y = 250
                player2.score += 1
                self.dx = -self.dx
                delay = 7
                playsound("Data/wrong.wav", False)
            elif self.x + 10 > 800:
                self.x = 400
                self.y = 250
                player1.y = 250
                player2.y = 250
                player1.score += 1
                self.dx = -self.dx
                delay = 7
                playsound("Data/right.wav", False)

            if self.x > 55 - increament and self.x < 65 and self.y < player1.y + 60 and self.y > player1.y - 60:
                self.dx = -self.dx
                playsound("Data/bounce.wav", False)

            if self.x > 745 and self.x < 750 + increament and self.y < player2.y + 60 and self.y > player2.y - 60:
                self.dx = -self.dx
                playsound("Data/bounce.wav", False)

        self.draw()


dx = 4.5
dy = 4.5
if random.random() >= 0.5:
    dx = -dx
if random.random() >= 0.5:
    dy = -dy
ball = ball_object(400, 250, dx, dy)


delay = 7
running = True
msg_box = True
while running:
    if player1.score >= 3 or player2.score >= 3:
        running = False
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            msg_box = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2.dy = -3.5 - increament
            elif event.key == pygame.K_DOWN:
                player2.dy = 3.5 + increament
            elif event.key == ord("w"):
                player1.dy = -3.5 - increament
            elif event.key == ord("s"):
                player1.dy = 3.5 + increament
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player2.dy = 0
            elif event.key == pygame.K_DOWN:
                player2.dy = 0
            elif event.key == ord("w"):
                player1.dy = 0
            elif event.key == ord("s"):
                player1.dy = 0

    player1.update()
    player2.update()
    ball.update()
    text = font.render(f"Player 1: {player1.score}    Player 2: {player2.score}", True, (255, 255, 255))
    window.blit(text, (300, 10))

    delay -= 0.1
    if delay < 0:
        increament += 0.001
    clock.tick(64)
    pygame.display.update()


if msg_box:
    if player1.score >= 3:
        playsound("Data/win.wav", False)
        tk = Tk()
        tk.withdraw()
        messagebox.showinfo("Well done", "Player 1 wins!!!")
    else:
        tk = Tk()
        tk.withdraw()
        playsound("Data/lose.wav", False)
        messagebox.showinfo("Well done", "Player 2 wins!!!")
