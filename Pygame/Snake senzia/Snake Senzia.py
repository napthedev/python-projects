import pygame
from pygame import mixer
import random
from tkinter import *
from tkinter import messagebox
from playsound import playsound

pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake senzia")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)
background_music = mixer.music.load("Data/background.wav")
mixer.music.play(-1)


length = 2
score = 0
ready_turning = True


class head_class(object):
    def __init__(self, row, column, direction):
        self.row = row
        self.column = column
        self.direction = direction

    def draw(self):
        if self.direction == "right":
            pygame.draw.rect(window, (0, 255, 0), (self.column * 10, self.row * 10, 5, 10))
        elif self.direction == "left":
            pygame.draw.rect(window, (0, 255, 0), (self.column * 10 + 5, self.row * 10, 5, 10))
        elif self.direction == "up":
            pygame.draw.rect(window, (0, 255, 0), (self.column * 10, self.row * 10 + 5, 10, 5))
        elif self.direction == "down":
            pygame.draw.rect(window, (0, 255, 0), (self.column * 10, self.row * 10, 10, 5))

        pygame.draw.circle(window, (0, 255, 0), (self.column * 10 + 5, self.row * 10 + 5), 5)

        if self.direction == "left" or self.direction == "right":
            pygame.draw.rect(window, (0, 0, 255), (self.column * 10 + 4, self.row * 10 + 1, 2, 3.5))
            pygame.draw.rect(window, (0, 0, 255), (self.column * 10 + 4, self.row * 10 + 6, 2, 3.5))
        else:
            pygame.draw.rect(window, (0, 0, 255), (self.column * 10 + 1, self.row * 10 + 4, 2, 3.5))
            pygame.draw.rect(window, (0, 0, 255), (self.column * 10 + 6, self.row * 10 + 4, 2, 3.5))

    def update(self):
        global food, length, body, running, score, mega_food, mega_food_time, ready_turning
        if self.direction == "left":
            self.column -= 1
        elif self.direction == "right":
            self.column += 1
        elif self.direction == "up":
            self.row -= 1
        elif self.direction == "down":
            self.row += 1

        if self.row < 0:
            self.row = 49
        elif self.row > 49:
            self.row = 0
        elif self.column < 0:
            self.column = 49
        elif self.column > 49:
            self.column = 0

        if mega_food > 0:
            if self.row == food.row and self.column == food.column:
                length += 2
                score += 1
                mega_food -= 1
                food.place()
                playsound("Data/right.wav", False)
        else:
            if (food.row == self.row or food.row + 1 == self.row) and (food.column == self.column or food.column + 1 == self.column):
                length += 2
                score += round(8 * mega_food_time / 400)
                mega_food = 8
                mega_food_time = 400
                food.place()
                playsound("Data/right.wav", False)

        for i in body:
            if self.row == i.row and self.column == i.column:
                running = False

        ready_turning = True
        self.draw()


head = head_class(24, 24, random.choice(["left", "right", "up", "down"]))


class cube(object):
    def __init__(self, row, column, direction):
        self.row = row
        self.column = column
        self.direction = direction

    def draw(self):
        global body
        if body[0] == self:
            if self.direction == "left":
                pygame.draw.rect(window, (0, 255, 0), (self.column * 10, self.row * 10, 5, 10))
            elif self.direction == "right":
                pygame.draw.rect(window, (0, 255, 0), (self.column * 10 + 5, self.row * 10, 5, 10))
            elif self.direction == "down":
                pygame.draw.rect(window, (0, 255, 0), (self.column * 10, self.row * 10 + 5, 10, 5))
            elif self.direction == "up":
                pygame.draw.rect(window, (0, 255, 0), (self.column * 10, self.row * 10, 10, 5))
            pygame.draw.circle(window, (0, 255, 0), (self.column * 10 + 5, self.row * 10 + 5), 5)
        else:
            pygame.draw.rect(window, (0, 255, 0), (self.column * 10, self.row * 10, 10, 10))


body = []


class food_class(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def draw(self):
        global mega_food
        if mega_food > 0:
            pygame.draw.circle(window, (255, 255, 0), (self.column * 10 + 5, self.row * 10 + 5), 5)
        else:
            pygame.draw.circle(window, (255, 0, 0), (self.column * 10 + 10, self.row * 10 + 10), 10)

    def place(self):
        global body, head, mega_food
        if mega_food > 0:
            self.row = random.randint(0, 49)
            self.column = random.randint(0, 49)
            duplicate = False
            for i in body:
                if self.row == i.row and self.column == i.column:
                    duplicate = True
            if self.row == head.row and self.column == head.column:
                duplicate = True
            if self.row <= 3 and self.column <= 9:
                duplicate = True
            while duplicate:
                duplicate = False
                self.row = random.randint(0, 49)
                self.column = random.randint(0, 49)
                for i in body:
                    if self.row == i.row and self.column == i.column:
                        duplicate = True
                if self.row == head.row and self.column == head.column:
                    duplicate = True
                if self.row <= 3 and self.column <= 9:
                    duplicate = True

        else:
            self.row = random.randint(0, 44)
            self.column = random.randint(0, 48)
            duplicate = False
            for i in body:
                if (self.row == i.row or self.row + 1 == i.row) and (self.column == i.column or self.column + 1 == i.column):
                    duplicate = True
            if (self.row == head.row or self.row + 1 == head.row) and (self.column == head.column or self.column + 1 == head.column):
                duplicate = True
            if self.row <= 3 and self.column <= 9:
                duplicate = True
            while duplicate:
                duplicate = False
                self.row = random.randint(0, 44)
                self.column = random.randint(0, 48)
                for i in body:
                    if (self.row == i.row or self.row + 1 == i.row) and (self.column == i.column or self.column + 1 == i.column):
                        duplicate = True
                if (self.row == head.row or self.row + 1 == head.row) and (self.column == head.column or self.column + 1 == head.column):
                    duplicate = True
                if self.row <= 3 and self.column <= 9:
                    duplicate = True


mega_food = 8
mega_food_time = 400
food = food_class(None, None)
food.place()


msg_box = True
running = True
while running:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            msg_box = False
            running = False
        elif event.type == pygame.KEYDOWN and ready_turning:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                if head.direction != "right":
                    head.direction = "left"
            elif event.key == pygame.K_RIGHT or event.key == ord("d"):
                if head.direction != "left":
                    head.direction = "right"
            elif event.key == pygame.K_UP or event.key == ord("w"):
                if head.direction != "down":
                    head.direction = "up"
            elif event.key == pygame.K_DOWN or event.key == ord("s"):
                if head.direction != "up":
                    head.direction = "down"
            ready_turning = False

    if mega_food <= 0:
        mega_food_time -= 4
        pygame.draw.rect(window, (255, 0, 0), (50, 470, mega_food_time, 15))
        if mega_food_time <= 0:
            mega_food = 8
            mega_food_time = 400
            food.place()

    body.append(cube(head.row, head.column, head.direction))
    if len(body) > length:
        body = body[len(body) - length:len(body)]
    for i in body:
        i.draw()
    head.update()
    food.draw()
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(text, (10, 10))

    clock.tick(24)
    pygame.display.update()

if msg_box:
    playsound("Data/lose.wav", False)
    tk = Tk()
    tk.withdraw()
    messagebox.showerror("You lose", f"Game over! Your score: {score}")
