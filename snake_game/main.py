import pygame
import sys
import random
from pygame import Vector2

pygame.init()
pygame.mixer.init()

shell = 25
num_block = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode((shell * num_block, shell * num_block))

SCREEN_EVENT = pygame.USEREVENT
pygame.time.set_timer(SCREEN_EVENT, 150)

pygame.display.set_caption("SSNAKE")

# GRAPHICS
apple_image = pygame.image.load("graphics/apple.png").convert_alpha()

head_up = pygame.image.load("graphics/head_up.png").convert_alpha()
head_down = pygame.image.load("graphics/head_down.png").convert_alpha()
head_right = pygame.image.load("graphics/head_right.png").convert_alpha()
head_left = pygame.image.load("graphics/head_left.png").convert_alpha()

tail_up = pygame.image.load("graphics/tail_up.png").convert_alpha()
tail_down = pygame.image.load("graphics/tail_down.png").convert_alpha()
tail_right = pygame.image.load("graphics/tail_right.png").convert_alpha()
tail_left = pygame.image.load("graphics/tail_left.png").convert_alpha()

body_up_down = pygame.image.load("graphics/body_up_down.png").convert_alpha()
body_left_right = pygame.image.load("graphics/body_left_right.png").convert_alpha()

angle_down_left = pygame.image.load("graphics/up_right.png").convert_alpha()
angle_right_down = pygame.image.load("graphics/right_down.png").convert_alpha()
angle_down_right = pygame.image.load("graphics/down_right.png").convert_alpha()
angle_left_up = pygame.image.load("graphics/left_up.png").convert_alpha()

# MUSIC
pygame.mixer.music.load("music/play.mp3")
pygame.mixer.music.play(loops=-1)
sound_eat = pygame.mixer.Sound("music/eat.wav")
sound_lose = pygame.mixer.Sound("music/lose.wav")


class Main:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()

    def draw(self):
        # IF APPLE TAKES SNAKE POSITION
        for i in self.snake.snake_body:
            if self.apple.position == i:
                self.apple.randomize()
            else:
                self.apple.draw()
        self.snake.draw()

    def move(self):
        self.snake.move()
        self.eat()

    def eat(self):
        if self.snake.snake_body[0] == self.apple.position:
            self.apple.randomize()
            self.snake.add_block()
            sound_eat.play()

    def fail(self):
        if not 0 <= self.snake.snake_body[0].x < num_block or not 0 <= self.snake.snake_body[0].y < num_block:
            self.snake.reset()
            sound_lose.play()
            self.lose()
        for block in self.snake.snake_body[1:]:
            if self.snake.snake_body[0] == block:
                self.snake.reset()
                sound_lose.play()
                self.lose()

    def grid_back(self):
        for i in range(20):
            for y in range(20):
                grid = pygame.Rect(y * shell, i * shell, shell, shell)
                if i % 2 == 0:
                    if y % 2 == 0:
                        pygame.draw.rect(screen, (156, 234, 101), grid)
                if i % 2 == 1:
                    if y % 2 == 1:
                        pygame.draw.rect(screen, (156, 234, 101), grid)

    def score(self):
        self.snake.score()

    def lose(self):
        over_cover = pygame.Surface((500, 500))
        over_cover.fill((225, 225, 225))
        over_cover.set_alpha(200)
        rect_over_cover = over_cover.get_rect(center=(250, 250))
        screen.blit(over_cover, rect_over_cover)

        font = pygame.font.Font("font/zag.ttf", 50)
        text = font.render("GAME OVER", True, (0, 0, 0), None)
        rect_text = text.get_rect(center=(250, 250))
        screen.blit(text, rect_text)
        pygame.display.flip()

        over = True
        while over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    over = False


class Apple:
    def __init__(self):
        self.randomize()

    def draw(self):
        pos_x = self.position.x * shell
        pos_y = self.position.y * shell
        rect_apple = pygame.Rect(pos_x, pos_y, shell, shell)
        screen.blit(apple_image, rect_apple)

    def randomize(self):
        x = random.randint(0, num_block - 1)
        y = random.randint(0, num_block - 1)
        self.position = Vector2((x, y))


class Snake:
    def __init__(self):
        self.snake_body = [Vector2(7, 5), Vector2(6, 5), Vector2(5, 5)]
        self.direction = Vector2(1, 0)
        self.eat = 0

    def draw(self):
        for index, i in enumerate(self.snake_body):
            if i == self.snake_body[0]:
                # DRAWING HEAD
                rect_snake = pygame.Rect(i.x * shell, i.y * shell, shell, shell)
                if self.direction == Vector2(0, 0):
                    screen.blit(head_right, rect_snake)
                elif self.direction == Vector2(1, 0):
                    screen.blit(head_right, rect_snake)
                elif self.direction == Vector2(-1, 0):
                    screen.blit(head_left, rect_snake)
                elif self.direction == Vector2(0, 1):
                    screen.blit(head_down, rect_snake)
                elif self.direction == Vector2(0, -1):
                    screen.blit(head_up, rect_snake)
            elif i == self.snake_body[-1]:
                # DRAWING TAIL
                rect_snake = pygame.Rect(i.x * shell, i.y * shell, shell, shell)
                if self.snake_body[-2].x - self.snake_body[-1].x == 1:
                    screen.blit(tail_right, rect_snake)
                elif self.snake_body[-2].x - self.snake_body[-1].x == -1:
                    screen.blit(tail_left, rect_snake)
                elif self.snake_body[-2].y - self.snake_body[-1].y == -1:
                    screen.blit(tail_up, rect_snake)
                elif self.snake_body[-2].y - self.snake_body[-1].y == 1:
                    screen.blit(tail_down, rect_snake)
            else:
                # DRAWING ANGLE
                rect_snake = pygame.Rect(i.x * shell, i.y * shell, shell, shell)
                if (self.snake_body[index] - self.snake_body[index - 1]) + (
                        self.snake_body[index] - self.snake_body[index + 1]) == Vector2(1, 1):
                    screen.blit(angle_down_right, rect_snake)
                elif (self.snake_body[index] - self.snake_body[index - 1]) + (
                        self.snake_body[index] - self.snake_body[index + 1]) == Vector2(-1, -1):
                    screen.blit(angle_down_left, rect_snake)
                elif (self.snake_body[index] - self.snake_body[index - 1]) + (
                        self.snake_body[index] - self.snake_body[index + 1]) == Vector2(1, -1):
                    screen.blit(angle_right_down, rect_snake)
                elif (self.snake_body[index] - self.snake_body[index - 1]) + (
                        self.snake_body[index] - self.snake_body[index + 1]) == Vector2(-1, 1):
                    screen.blit(angle_left_up, rect_snake)
                # DRAWING BODY
                elif self.snake_body[index] - self.snake_body[index + 1] == Vector2(1, 0):
                    screen.blit(body_left_right, rect_snake)
                elif self.snake_body[index] - self.snake_body[index + 1] == Vector2(-1, 0):
                    screen.blit(body_left_right, rect_snake)
                elif self.snake_body[index] - self.snake_body[index + 1] == Vector2(0, 1):
                    screen.blit(body_up_down, rect_snake)
                elif self.snake_body[index] - self.snake_body[index + 1] == Vector2(0, -1):
                    screen.blit(body_up_down, rect_snake)

    def move(self):
        if self.eat == 1:
            copy_snake = self.snake_body[:]
            copy_snake.insert(0, copy_snake[0] + self.direction)
            self.snake_body = copy_snake
            self.eat = 0
        else:
            copy_snake = self.snake_body[:-1]
            copy_snake.insert(0, copy_snake[0] + self.direction)
            self.snake_body = copy_snake

    def add_block(self):
        self.eat = 1

    def reset(self):
        self.snake_body = [Vector2(7, 5), Vector2(6, 5), Vector2(5, 5)]
        self.direction = Vector2(1, 0)

    def score(self):
        score = pygame.font.Font("font/zag.ttf", 32)
        text = score.render(str(len(self.snake_body) - 3), True, (0, 0, 0), (147, 225, 92))
        rect_scale = text.get_rect(center=(475, 475))
        screen.blit(text, rect_scale)


main = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_EVENT:
            main.move()
            main.fail()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1, 0)

    screen.fill((147, 225, 92))
    main.grid_back()
    main.draw()
    main.score()
    clock.tick(60)
    pygame.display.update()
