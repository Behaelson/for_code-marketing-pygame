import pygame
import sys
import random
from pygame.math import Vector2
from collections import deque

tamanho_cel = 32
num_cel = 20
SCREEN_WIDTH = tamanho_cel * num_cel
SCREEN_HEIGHT = tamanho_cel * num_cel

FPS = 30
MOVE_UPDATE_EVENT = pygame.USEREVENT + 1
SNAKE_SPEED_MS = 150

GREEN_GRASS = (175, 215, 70)
DARK_GRASS = (167, 209, 61)
SNAKE_COLOR = (56, 74, 12)
FRUIT_COLOR = (231, 71, 29)
TEXT_COLOR = (56, 74, 12)
SCORE_BG_COLOR = (167, 209, 61)

usr_path = 'C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/'
#temporário

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Snake - Smart Architecture")
clock = pygame.time.Clock()

game_font = pygame.font.Font(None, 25)


class Fruit:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.randomize()

    def randomize(self):
        self.x = random.randint(0, num_cel - 1)
        self.y = random.randint(0, num_cel - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self, surface):
        self.image = pygame.image.load(usr_path+'fruta.png')
        fruit_rect = pygame.Rect(
            int(self.pos.x * tamanho_cel),
            int(self.pos.y * tamanho_cel),
            tamanho_cel,
            tamanho_cel
        )
        screen.blit(self.image, fruit_rect)


class Snake:
    def __init__(self):
        self.reset()
        # self.crunch_sound = pygame.mixer.Sound('Sound_crunch.wav')
        self.headN = pygame.image.load(usr_path+'headN.png')
        self.headS = pygame.image.load(usr_path+'headS.png')
        self.headO = pygame.image.load(usr_path+'headO.png')
        self.headL = pygame.image.load(usr_path+'headL.png')

        self.cauda_N = pygame.image.load(usr_path+'cauda_N.png')
        self.cauda_S = pygame.image.load(usr_path+'cauda_S.png')
        self.cauda_O = pygame.image.load(usr_path+'cauda_O.png')  
        self.cauda_L = pygame.image.load(usr_path+'cauda_L.png')  

        self.corpo_h = pygame.image.load(usr_path+'corpo_h.png')
        self.corpo_v = pygame.image.load(usr_path+'corpo_v.png')

        self.curva_NL = pygame.image.load(usr_path+'norte_leste.png')
        self.curva_NO = pygame.image.load(usr_path+'norte_oeste.png')
        self.curva_SL = pygame.image.load(usr_path+'sul_leste.png')
        self.curva_SO = pygame.image.load(usr_path+'sul_oeste.png')

    def reset(self):
        self.body = deque([Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.direction_queue = deque()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_cauda_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * tamanho_cel)
            y_pos = int(block.y * tamanho_cel) 
            block_rect = pygame.Rect(x_pos, y_pos, tamanho_cel, tamanho_cel)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.cauda, block_rect)
            else: 
                bloco_anterior = self.body[index + 1] - block
                bloco_seguinte = self.body[index - 1] - block
                if bloco_anterior.x == bloco_seguinte.x:
                    screen.blit(self.corpo_v, block_rect)
                elif bloco_anterior.y == bloco_seguinte.y:
                    screen.blit(self.corpo_h, block_rect)
                elif (bloco_anterior.x == -1 and bloco_seguinte.y == -1) or (bloco_anterior.y == -1 and bloco_seguinte.x == -1):
                    screen.blit(self.curva_NO, block_rect)
                elif (bloco_anterior.x == -1 and bloco_seguinte.y == 1) or (bloco_anterior.y == 1 and bloco_seguinte.x == -1):
                    screen.blit(self.curva_SO, block_rect)
                elif (bloco_anterior.x == 1 and bloco_seguinte.y == -1) or (bloco_anterior.y == -1 and bloco_seguinte.x == 1):
                    screen.blit(self.curva_NL, block_rect)
                elif (bloco_anterior.x == 1 and bloco_seguinte.y == 1) or (bloco_anterior.y == 1 and bloco_seguinte.x == 1):
                    screen.blit(self.curva_SL, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headO
        elif head_relation == Vector2(-1,0): self.head = self.headL
        elif head_relation == Vector2(0,1): self.head = self.headN
        elif head_relation == Vector2(0,-1): self.head = self.headS

    def update_cauda_graphics(self):
        cauda_relation = self.body[-2] - self.body[-1]
        if cauda_relation == Vector2(1,0): self.cauda = self.cauda_O
        elif cauda_relation == Vector2(-1,0): self.cauda = self.cauda_L
        elif cauda_relation == Vector2(0,1): self.cauda = self.cauda_N
        elif cauda_relation == Vector2(0,-1): self.cauda = self.cauda_S

    def update_direction(self):
        if self.direction_queue:
            new_dir = self.direction_queue.popleft()
            if new_dir != -self.direction:
                self.direction = new_dir

    def move_snake(self):
        self.update_direction()

        if self.new_block:
            new_head = self.body[0] + self.direction
            self.body.appendleft(new_head)
            self.new_block = False
        else:
            new_head = self.body[0] + self.direction
            self.body.appendleft(new_head)
            self.body.pop()

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        pass


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self, surface):
        self.draw_grass(surface)
        self.fruit.draw(surface)
        self.snake.draw_snake()
        self.draw_score(surface)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            while self.fruit.pos in self.snake.body:
                self.fruit.randomize()

            self.snake.add_block()
            self.snake.play_crunch_sound()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < num_cel or \
                not 0 <= self.snake.body[0].y < num_cel:
            self.game_over()

        for block in list(self.snake.body)[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self, surface):
        surface.fill(GREEN_GRASS)
        for row in range(num_cel):
            if row % 2 == 0:
                for col in range(num_cel):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * tamanho_cel, row * tamanho_cel, tamanho_cel, tamanho_cel)
                        pygame.draw.rect(surface, DARK_GRASS, grass_rect)
            else:
                for col in range(num_cel):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * tamanho_cel, row * tamanho_cel, tamanho_cel, tamanho_cel)
                        pygame.draw.rect(surface, DARK_GRASS, grass_rect)

    def draw_score(self, surface):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, TEXT_COLOR)
        score_x = int(tamanho_cel * num_cel - 60)
        score_y = int(tamanho_cel * num_cel - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        bg_rect = pygame.Rect(
            score_rect.left - 6,
            score_rect.top - 6,
            score_rect.width + 12,
            score_rect.height + 12
        )
        pygame.draw.rect(surface, SCORE_BG_COLOR, bg_rect)
        pygame.draw.rect(surface, TEXT_COLOR, bg_rect, 2)
        surface.blit(score_surface, score_rect)

    def queue_input(self, direction):
        target_dir = direction
        if not self.snake.direction_queue:
            last_dir = self.snake.direction
        else:
            last_dir = self.snake.direction_queue[-1]

        if target_dir != -last_dir:
            self.snake.direction_queue.append(target_dir)

main_game = Main()
pygame.time.set_timer(MOVE_UPDATE_EVENT, SNAKE_SPEED_MS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOVE_UPDATE_EVENT:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.queue_input(Vector2(0, -1))
            if event.key == pygame.K_DOWN:
                main_game.queue_input(Vector2(0, 1))
            if event.key == pygame.K_LEFT:
                main_game.queue_input(Vector2(-1, 0))
            if event.key == pygame.K_RIGHT:
                main_game.queue_input(Vector2(1, 0))

    main_game.draw_elements(screen)
    pygame.display.update()

    clock.tick(FPS)
