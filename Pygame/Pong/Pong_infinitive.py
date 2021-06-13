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


class computer_object(object):
    def __init__(self, x, y, dy, score, serve):
        self.x = x
        self.y = y
        self.dy = dy
        self.score = score
        self.serve = serve

    def draw(self):
        pygame.draw.rect(window, (255, 255, 255), (self.x - 10, self.y - 50, 20, 100))

    def update(self):
        global delay, predict, increament
        if delay < 0:
            if self.serve:
                if abs(self.y - predict) < 15:
                    self.dy = 0
                elif self.y - 15 < predict:
                    self.dy = 3.5 + increament
                elif self.y + 15 > predict:
                    self.dy = -3.5 - increament
            else:
                if self.y < ball.y:
                    self.dy = 3.5 + increament
                elif self.y > ball.y:
                    self.dy = -3.5 - increament

            self.y += self.dy

            if self.y - 50 < 0:
                self.y = 50
            elif self.y + 50 > 500:
                self.y = 450

        self.draw()


computer1 = computer_object(50, 250, 0, 0, False)
computer2 = computer_object(750, 250, 0, 0, False)

predict = 250


class ball_object(object):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def draw(self):
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), 10)

    def update(self):
        global delay, computer1, computer2, predict
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
                computer1.y = 250
                computer2.y = 250
                predict = 250
                computer1.serve = False
                computer2.serve = False
                computer2.score += 1
                self.dx = -self.dx
                delay = 7
                playsound("Data/wrong.wav", False)
            elif self.x + 10 > 800:
                self.x = 400
                self.y = 250
                computer1.y = 250
                computer2.y = 250
                predict = 250
                computer1.serve = False
                computer2.serve = False
                computer1.score += 1
                self.dx = -self.dx
                delay = 7
                playsound("Data/right.wav", False)

            if self.x > 55 - increament and self.x < 60 and self.y < computer1.y + 60 and self.y > computer1.y - 60:
                self.dx = -self.dx
                playsound("Data/bounce.wav", False)
                computer1.serve = False
                computer2.serve = True
                if self.dy >= 0:
                    predict = abs(300 - self.y)
                else:
                    predict = 700 - self.y
                    if predict > 500:
                        predict = 1000 - predict

            if self.x > 745 and self.x < 750 + increament and self.y < computer2.y + 60 and self.y > computer2.y - 60:
                self.dx = -self.dx
                playsound("Data/bounce.wav", False)
                computer1.serve = True
                computer2.serve = False
                if self.dy >= 0:
                    predict = abs(300 - self.y)
                else:
                    predict = 700 - self.y
                    if predict > 500:
                        predict = 1000 - predict

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
    if computer1.score >= 3 or computer2.score >= 3:
        running = False
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            msg_box = False
            running = False

    computer1.update()
    computer2.update()
    ball.update()
    text = font.render(f"Computer 1: {computer1.score}    Computer 2: {computer2.score}", True, (255, 255, 255))
    window.blit(text, (250, 10))

    delay -= 0.1
    if delay < 0:
        increament += 0.002
    clock.tick(64)
    pygame.display.update()


if msg_box:
    if computer1.score >= 3:
        playsound("Data/win.wav", False)
        tk = Tk()
        tk.withdraw()
        messagebox.showinfo("Well done", "Computer 1 wins!!!")
    else:
        tk = Tk()
        tk.withdraw()
        playsound("Data/lose.wav", False)
        messagebox.showinfo("Well done", "Computer 2 wins!!!")
