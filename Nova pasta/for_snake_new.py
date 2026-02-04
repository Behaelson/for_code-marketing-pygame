import pygame
import sys
import random
from pygame.math import Vector2
from collections import deque
import os

tamanho_cel = 25  
num_cel_x = 25
num_cel_y = 20

OFFSET = 60 

SCREEN_WIDTH = (tamanho_cel * num_cel_x) + (2 * OFFSET)
SCREEN_HEIGHT = (tamanho_cel * num_cel_y) + (2 * OFFSET)

FPS = 30
MOVE_UPDATE_EVENT = pygame.USEREVENT + 1
SNAKE_SPEED_MS = 150

GREEN_GRASS = (97, 74, 211)
DARK_GRASS = (30, 22, 71)
SNAKE_COLOR = (56, 74, 12)
FRUIT_COLOR = (231, 71, 29)
UI_BG_COLOR = (20, 15, 50)
TEXT_COLOR = (255, 255, 255)
SCORE_BG_COLOR = (167, 209, 61)
BORDER_COLOR = (255, 255, 255)
BUTTON_COLOR = (40, 30, 90)

# Caminho da pasta Downloads
usr_path = os.path.join(os.path.expanduser('~'), 'Downloads') + '/'

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("For_Snake")
clock = pygame.time.Clock()

game_font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 40)
score_font = pygame.font.Font(None, 32)

class Fruit:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.randomize()
        try:
            img = pygame.image.load(usr_path + 'fruta.png').convert_alpha()
            self.image = pygame.transform.scale(img, (tamanho_cel, tamanho_cel))
        except:
            self.image = pygame.Surface((tamanho_cel, tamanho_cel))
            self.image.fill(FRUIT_COLOR)

    def randomize(self):
        self.x = random.randint(0, num_cel_x - 1)
        self.y = random.randint(0, num_cel_y - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self, surface):
        fruit_rect = pygame.Rect(
            int(self.pos.x * tamanho_cel),
            int(self.pos.y * tamanho_cel),
            tamanho_cel,
            tamanho_cel
        )
        surface.blit(self.image, fruit_rect)
        

class Snake:
    def __init__(self):
        self.reset()
        self.load_images()

    def load_images(self):
        def load_scale(name):
            try:
                img = pygame.image.load(usr_path + name).convert_alpha()
                return pygame.transform.scale(img, (tamanho_cel, tamanho_cel))
            except:
                return None

        self.headN = load_scale('headN.png')
        self.headS = load_scale('headS.png')
        self.headO = load_scale('headO.png')
        self.headL = load_scale('headL.png')
        self.cauda_N = load_scale('cauda_N.png')
        self.cauda_S = load_scale('cauda_S.png')
        self.cauda_O = load_scale('cauda_O.png')
        self.cauda_L = load_scale('cauda_L.png')
        self.corpo_h = load_scale('corpo_h.png')
        self.corpo_v = load_scale('corpo_v.png')
        self.curva_NL = load_scale('norte_leste.png')
        self.curva_NO = load_scale('norte_oeste.png')
        self.curva_SL = load_scale('sul_leste.png')
        self.curva_SO = load_scale('sul_oeste.png')

    def reset(self):
        self.body = deque([Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.direction_queue = deque()

    def draw_snake(self, surface):
        self.update_head_graphics()
        self.update_cauda_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * tamanho_cel)
            y_pos = int(block.y * tamanho_cel) 
            block_rect = pygame.Rect(x_pos, y_pos, tamanho_cel, tamanho_cel)
            
            if hasattr(self, 'headN') and self.headN is not None:
                if index == 0:
                    surface.blit(self.head, block_rect)
                elif index == len(self.body) - 1:
                    surface.blit(self.cauda, block_rect)
                else: 
                    bloco_anterior = self.body[index + 1] - block
                    bloco_seguinte = self.body[index - 1] - block
                    if bloco_anterior.x == bloco_seguinte.x:
                        surface.blit(self.corpo_v, block_rect)
                    elif bloco_anterior.y == bloco_seguinte.y:
                        surface.blit(self.corpo_h, block_rect)
                    elif (bloco_anterior.x == -1 and bloco_seguinte.y == -1) or (bloco_anterior.y == -1 and bloco_seguinte.x == -1):
                        surface.blit(self.curva_NO, block_rect)
                    elif (bloco_anterior.x == -1 and bloco_seguinte.y == 1) or (bloco_anterior.y == 1 and bloco_seguinte.x == -1):
                        surface.blit(self.curva_SO, block_rect)
                    elif (bloco_anterior.x == 1 and bloco_seguinte.y == -1) or (bloco_anterior.y == -1 and bloco_seguinte.x == 1):
                        surface.blit(self.curva_NL, block_rect)
                    elif (bloco_anterior.x == 1 and bloco_seguinte.y == 1) or (bloco_anterior.y == 1 and bloco_seguinte.x == 1):
                        surface.blit(self.curva_SL, block_rect)
            else:
                pygame.draw.rect(surface, SNAKE_COLOR, block_rect)

    def update_head_graphics(self):
        if not hasattr(self, 'headN') or self.headN is None: return
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headO
        elif head_relation == Vector2(-1,0): self.head = self.headL
        elif head_relation == Vector2(0,1): self.head = self.headN
        elif head_relation == Vector2(0,-1): self.head = self.headS

    def update_cauda_graphics(self):
        if not hasattr(self, 'headN') or self.headN is None: return
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
        
        # Dimensões totais da área de jogo (grid)
        self.game_width = num_cel_x * tamanho_cel
        self.game_height = num_cel_y * tamanho_cel
        self.game_surface = pygame.Surface((self.game_width, self.game_height))
        self.high_score = 0
        
        
        self.bg_image = None
        try:
            bg_source = pygame.image.load(usr_path + 'Grid for_snake.png').convert()
            self.bg_image = pygame.transform.scale(bg_source, (670, self.game_height))
            print("SUCESSO: Fundo do grid carregado!")
        except Exception as e:
            print(f"AVISO: Fundo não carregado. Usando padrão. Erro: {e}")
        # -------------------------------------
        
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self, main_screen):
        main_screen.fill(UI_BG_COLOR)
        
        # Desenha o jogo na superfície interna
        self.draw_grass(self.game_surface)
        self.fruit.draw(self.game_surface)
        self.snake.draw_snake(self.game_surface)
        
        # Posiciona o jogo no centro da moldura
        game_rect = self.game_surface.get_rect(topleft=(OFFSET, OFFSET))
        
        main_screen.blit(self.game_surface, game_rect)
        pygame.draw.rect(main_screen, BORDER_COLOR, game_rect, 2)
        
        # Desenha toda a UI no topo
        self.draw_ui(main_screen)

    def draw_grass(self, surface):
        if self.bg_image is not None:
            surface.blit(self.bg_image, (-23, 0))
        else:
            # Se não existir imagem, desenha o xadrez antigo
            surface.fill(GREEN_GRASS)
            for row in range(num_cel_y):
                for col in range(num_cel_x):
                    if (row + col) % 2 == 0:
                        grass_rect = pygame.Rect(col * tamanho_cel, row * tamanho_cel, tamanho_cel, tamanho_cel)
                        pygame.draw.rect(surface, DARK_GRASS, grass_rect)
       

    def draw_ui(self, surface):
        mid_y = OFFSET // 2

        score_val = str(len(self.snake.body) - 3)
        score_text = score_font.render(f"SCORE: {score_val}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(midleft=(60, mid_y)) 
        surface.blit(score_text, score_rect)

        title_surf = title_font.render("FOR_SNAKE", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, mid_y))
        surface.blit(title_surf, title_rect)

        hs_text = score_font.render(f"BEST: {self.high_score}", True, TEXT_COLOR)
        hs_rect = hs_text.get_rect(midright=(SCREEN_WIDTH - 60, mid_y)) 
        surface.blit(hs_text, hs_rect)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            while self.fruit.pos in self.snake.body:
                self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < num_cel_x or not 0 <= self.snake.body[0].y < num_cel_y:
            self.game_over()
        for block in list(self.snake.body)[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        current_score = len(self.snake.body) - 3
        if current_score > self.high_score:
            self.high_score = current_score
        self.snake.reset()

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