import pygame
import random
import math

scr_row = 20
scr_col = 10
block_size = 25
pad_left = 150
pad_right = 150

pygame.init()

window = pygame.display.set_mode((scr_col * block_size + pad_left + pad_right, scr_row * block_size))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 20)
font2 = pygame.font.Font("freesansbold.ttf", 50)

S = [[[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]]
Z = [[[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]]
I = [[[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]]
O = [[[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
J = [[[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]], [[0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]]]
L = [[[0, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0]], [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]], [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]]]
T = [[[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], [[0, 1, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

board = [[(0, 0, 0) for i in range(scr_col)] for i in range(scr_row)]


class particle(object):
    def __init__(self, row, col, shape):
        self.row = row
        self.col = col
        self.shape = shape
        self.rotation = shape
        self.color = shape


def convert_shape(current_particle):
    positions = []
    rotate_position = shapes[current_particle.shape][current_particle.rotation % len(shapes[current_particle.shape])]
    for row in range(len(rotate_position)):
        for col in range(len(rotate_position[row])):
            if rotate_position[row][col] == 1:
                positions.append((current_particle.row + row, current_particle.col + col))

    return positions


current_particle = particle(-2, round(scr_col / 2) - 2, random.randint(0, 6))


def valid_location(particle):
    global next_shape, current_particle, next_shape_delay
    current_particle_position = convert_shape(particle)
    corners = get_shape_side(current_particle_position)
    if corners["left"] < 0:
        return False
    if corners["right"] >= scr_col:
        return False
    if corners["bottom"] >= scr_row:
        if not is_quick_drop:
            next_shape_delay = 0
        return False
    for i, j in current_particle_position:
        if board[int(i)][int(j)] != (0, 0, 0) and direction == "down":
            if not is_quick_drop:
                next_shape_delay = 0
            return False
    for i, j in current_particle_position:
        if board[int(i)][int(j)] != (0, 0, 0):
            return False

    return True


def check_lose(board):
    for col in range(scr_col):
        if board[0][col] != (0, 0, 0):
            return True
    return False


def get_shape_side(positions):
    horizontal_positions = sorted(list(positions), key=lambda x: x[1])
    vertical_positions = sorted(list(positions), key=lambda x: x[0])
    corners = {
        "left": horizontal_positions[0][1],
        "right": horizontal_positions[::-1][0][1],
        "top": vertical_positions[0][0],
        "bottom": vertical_positions[::-1][0][0]
    }
    return corners


def generate_next_shape():
    global is_quick_drop
    is_quick_drop = False
    next_shape = random.randint(0, 6)
    while next_shape == current_particle.shape:
        next_shape = random.randint(0, 6)
    return next_shape


next_shape = generate_next_shape()


def switch_next_shape():
    global next_shape, score
    current_particle_position = convert_shape(current_particle)
    for row in range(scr_row):
        for col in range(scr_col):
            if (row, col) in current_particle_position:
                board[row][col] = shape_colors[current_particle.color]
    current_particle.row = -1
    current_particle.col = round(scr_col / 2) - 2
    current_particle.shape = next_shape
    current_particle.color = next_shape
    current_particle.rotation = 0
    next_shape = generate_next_shape()
    if is_quick_drop:
        score += 20
    else:
        score += 10


def quick_drop():
    while valid_location(current_particle):
        current_particle.row += 1
        direction = "down"
    current_particle.row -= 1


def clear_row(board):
    is_clearing = False
    global score, cleared_row
    temp_board = board.copy()
    for row in range(scr_row - 1, -1, -1):
        if not (0, 0, 0) in board[row]:
            temp_board = [[(0, 0, 0) for i in range(scr_col)]] + board[0:row] + board[row + 1:scr_row]
            is_clearing = True
            score += 100
            cleared_row += 1
            break
    while is_clearing:
        for row in range(scr_row - 1, -1, -1):
            if not (0, 0, 0) in temp_board[row]:
                temp_board = [[(0, 0, 0) for i in range(scr_col)]] + temp_board[0:row] + temp_board[row + 1:scr_row]
                is_clearing = True
                score += 100
                cleared_row += 1
                break
            is_clearing = False
    return temp_board


def draw_next_shape(next_shape):
    next_shape_text = font.render("Next shape", True, (255, 255, 255))
    text_width = next_shape_text.get_width()
    window.blit(next_shape_text, (pad_left + scr_col * block_size + pad_right / 2 - text_width / 2, scr_row * block_size / 2 - 50))
    positions = []
    rotate_position = shapes[next_shape][0]
    for row in range(len(rotate_position)):
        for col in range(len(rotate_position[row])):
            if rotate_position[row][col] == 1:
                pygame.draw.rect(window, shape_colors[next_shape], (pad_left + scr_col * block_size + pad_right / 2 - 2 * block_size + col * block_size + 1, scr_row * block_size / 2 + row * block_size + 1 - 20, block_size - 2, block_size - 2))


def draw(board):
    pygame.draw.rect(window, (255, 255, 255), (pad_left, 0, scr_col * block_size, scr_row * block_size), 1)
    for row in range(1, scr_row):
        pygame.draw.line(window, (100, 100, 100), (0 + pad_left, row * block_size), (scr_col * block_size + pad_left, row * block_size))
    for col in range(1, scr_col):
        pygame.draw.line(window, (100, 100, 100), (col * block_size + pad_left, 0), (col * block_size + pad_left, scr_row * block_size))

    current_particle_position = convert_shape(current_particle)
    for row in range(scr_row):
        for col in range(scr_col):
            if (row, col) in current_particle_position:
                pygame.draw.rect(window, shape_colors[current_particle.color], (col * block_size + 1 + pad_left, row * block_size + 1, block_size - 2, block_size - 2))
            else:
                pygame.draw.rect(window, board[row][col], (col * block_size + 1 + pad_left, row * block_size + 1, block_size - 2, block_size - 2))
    draw_next_shape(next_shape)


running = True
delay = 100
speed = 3
direction = "down"
next_shape_delay = -math.inf
is_quick_drop = False
score = 0
cleared_row = 0
while running:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not check_lose(board):
            if event.key == pygame.K_LEFT:
                current_particle.col -= 1
                direction = "left"
                if not valid_location(current_particle):
                    current_particle.col += 1
            if event.key == pygame.K_RIGHT:
                current_particle.col += 1
                direction = "right"
                if not valid_location(current_particle):
                    current_particle.col -= 1
            if event.key == pygame.K_UP:
                current_particle.rotation += 1
                direction = "up"
                if not valid_location(current_particle):
                    current_particle.rotation -= 1
            if event.key == pygame.K_DOWN:
                current_particle.row += 1
                direction = "down"
                if not valid_location(current_particle):
                    current_particle.row -= 1
            if event.key == pygame.K_SPACE:
                is_quick_drop = True
                quick_drop()
                switch_next_shape()

    draw(board)
    score_text = font.render("Score", True, (255, 255, 255))
    window.blit(score_text, (pad_left / 2 - score_text.get_width() / 2, scr_row * block_size / 2 - 100))
    score_value = font2.render(f"{score}", True, (255, 255, 255))
    window.blit(score_value, (pad_left / 2 - score_value.get_width() / 2, scr_row * block_size / 2 - 70))
    cleared_row_text = font.render("Lines", True, (255, 255, 255))
    window.blit(cleared_row_text, (pad_left / 2 - cleared_row_text.get_width() / 2, scr_row * block_size / 2))
    cleared_row_value = font2.render(f"{cleared_row}", True, (255, 255, 255))
    window.blit(cleared_row_value, (pad_left / 2 - cleared_row_value.get_width() / 2, scr_row * block_size / 2 + 30))

    board = clear_row(board)

    if check_lose(board):
        game_over_text = font2.render("Game Over!", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=((scr_col * block_size + pad_left + pad_right) / 2, scr_row * block_size / 2))
        window.blit(game_over_text, game_over_text_rect)

    speed -= clock.get_rawtime() / 100000
    delay += clock.get_rawtime()
    next_shape_delay += clock.get_rawtime()
    if delay / 10 >= speed and not check_lose(board):
        current_particle.row += 1
        direction = "down"
        if not valid_location(current_particle):
            current_particle.row -= 1

        delay = 0
    if next_shape_delay / 10 >= 0.5:
        switch_next_shape()
        next_shape_delay = -math.inf

    clock.tick(24)
    pygame.display.update()
