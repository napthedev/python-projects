import pygame
import random

pygame.init()

window = pygame.display.set_mode((300, 400))
pygame.display.set_caption("Flappy bird")
icon = pygame.image.load("Data/bird-1.jpg")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
font = pygame.font.Font('Data/flappybird.ttf', 30)

bird_1_img = pygame.image.load("Data/bird-1.jpg")
bird_2_img = pygame.image.load("Data/bird-2.jpg")
background_img = pygame.image.load("Data/background.jpg")


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class bird_class(object):
    def __init__(self, y, dy, rotation, rotate_speed):
        self.y = y
        self.dy = dy
        self.rotation = rotation
        self.rotate_speed = rotate_speed

    def draw(self):
        global bird_1_img, time, lose
        if not lose:
            if round(time) % 2 == 0:
                display_img = rot_center(bird_1_img, self.rotation)
                window.blit(display_img, (50, self.y))
            else:
                display_img = rot_center(bird_2_img, self.rotation)
                window.blit(display_img, (50, self.y))
        else:
            display_img = rot_center(bird_1_img, self.rotation)
            window.blit(display_img, (50, self.y))

    def update(self):
        global start, lose

        if start and not lose:

            self.dy += 1
            self.rotate_speed -= 0.7

            if self.rotation < -60:
                self.rotation = -60
            elif self.rotation > 20:
                self.rotation = 20

            if self.y > 300:
                lose = True

            self.rotation += self.rotate_speed

            if self.y < -5:
                self.y = -5
                self.dy = 0
                self.rotate_speed = 0
            if self.dy < 30:
                self.y += self.dy

        self.draw()


bird = bird_class(184, 0, 0, 0)


class pipe_class(object):
    def __init__(self, x, dx, top, bottom):
        self.x = x
        self.dx = dx
        self.top = top
        self.bottom = bottom

    def draw(self):
        pygame.draw.rect(window, (1, 184, 6), (self.x, 0, 20, self.top))
        pygame.draw.rect(window, (0, 0, 0), (self.x, 0, 20, self.top), 2)
        pygame.draw.rect(window, (1, 184, 6),
                         (self.x, self.bottom, 20, 340 - self.bottom))
        pygame.draw.rect(window, (0, 0, 0),
                         (self.x, self.bottom, 20, 340 - self.bottom), 2)
        pygame.draw.rect(window, (1, 184, 6),
                         (self.x - 5, self.top - 20, 30, 20))
        pygame.draw.rect(window, (0, 0, 0),
                         (self.x - 5, self.top - 20, 30, 20), 2)
        pygame.draw.rect(window, (1, 184, 6),
                         (self.x - 5, self.bottom, 30, 20))
        pygame.draw.rect(window, (0, 0, 0), (self.x - 5, self.bottom, 30, 20),
                         2)

    def update(self):
        global bird, lose
        if self.x < 82 and self.x + 20 > 50 and (self.top > bird.y + 6 or self.bottom < bird.y + 30):
            lose = True

        if not lose:
            self.x += self.dx
        self.draw()


def generate():
    top = random.randint(50, 200)
    bottom = top + 80
    pipes.append(pipe_class(310, -3, top, bottom))


pipes = []
response = 3
start = False

time = 0
running = True
lose = False
speed = -3
while running:
    window.blit(background_img, (0, 0))

    if response < 0:
        response = 8 + speed
        generate()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord("w") or event.key == pygame.K_SPACE:
                if start is False:
                    start = True
                if lose is True:
                    lose = False
                    bird.y = 200
                    bird.rotation = 0
                    pipes = []
                    response = 3
                    score = 0
                    speed = -3

                bird.dy = -9
                bird.rotate_speed = 10 - bird.rotation * 0.1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not start:
                start = True
            if lose:
                lose = False
                bird.y = 200
                bird.rotation = 0
                pipes = []
                response = 3
                score = 0
                speed = -3

            bird.dy = -9
            bird.rotate_speed = 10 - bird.rotation * 0.1

    score = 0
    for pipe in pipes:
        pipe.update()
        if pipe.x < 30:
            score += 1
        pipe.dx = speed

    score_text = font.render(f"{score}", True, (255, 255, 255))
    if not lose:
        score_text_rect = score_text.get_rect(center=(150, 40))
    else:
        score_text_rect = score_text.get_rect(center=(150, 210))
    window.blit(score_text, score_text_rect)

    if not start:
        start_text = font.render("PRESS TO START", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(150, 150))
        window.blit(start_text, start_text_rect)

    if lose:
        lose_text = font.render("YOU LOSE", True, (255, 255, 255))
        lose_text_rect = lose_text.get_rect(center=(150, 170))
        window.blit(lose_text, lose_text_rect)

    if start:
        time += 0.2
        response -= 0.1

    if speed > -6:
        speed -= 0.003
    bird.update()
    clock.tick(24)
    pygame.display.update()
