
import pygame
import sys
import random
from pygame.math import Vector2
from collections import deque

tamanho_cel = 32
num_cel = 20
largura_tela = tamanho_cel * num_cel
altura_tela = tamanho_cel * num_cel

FPS = 30
MOVE_UPDATE_EVENT = pygame.USEREVENT + 1
cobra_SPEED_MS = 150

roxo_1 = (182, 167, 255)
roxo_2 = (166, 148, 255)
cor_cobra = (56, 74, 12)
cor_fruta = (231, 71, 29)
cor_texto = (255, 255, 255)
cor_background = (125, 103, 234)

usr_path = 'C:/Users/wandrey.lima/Downloads/jogo/'
#temporário, esperando o path universal da arina

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("for_snake")
clock = pygame.time.Clock()
fonte_letra = pygame.font.Font(None, 25)

class fruta:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.randomize()

    def draw(self, surface):
        self.image = pygame.image.load(usr_path+'fruta.png')
        fruta_rect = pygame.Rect(
            int(self.pos.x * tamanho_cel),
            int(self.pos.y * tamanho_cel),
            tamanho_cel,
            tamanho_cel
        )
        tela.blit(self.image, fruta_rect)

    def randomize(self):
        self.x = random.randint(0, num_cel - 1)
        self.y = random.randint(0, num_cel - 1)
        self.pos = Vector2(self.x, self.y)

class cobra:
    def __init__(self):
        self.cabecaN = pygame.image.load(usr_path+'headN.png')
        self.cabecaS = pygame.image.load(usr_path+'headS.png')
        self.cabecaO = pygame.image.load(usr_path+'headO.png')
        self.cabecaL = pygame.image.load(usr_path+'headL.png')

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
        self.reset()

    def reset(self):
        self.body = deque([Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])
        self.direction = Vector2(1, 0)
        self.novo_corpo = False
        self.direction_queue = deque()

    def design_cobra(self):
        self.update_cabeca_graphics()
        self.update_cauda_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * tamanho_cel)
            y_pos = int(block.y * tamanho_cel) 
            block_rect = pygame.Rect(x_pos, y_pos, tamanho_cel, tamanho_cel)
            
            if index == 0:
                tela.blit(self.cabeca, block_rect)
            elif index == len(self.body) - 1:
                tela.blit(self.cauda, block_rect)
            else: 
                bloco_anterior = self.body[index + 1] - block
                bloco_seguinte = self.body[index - 1] - block
                if bloco_anterior.x == bloco_seguinte.x:
                    tela.blit(self.corpo_v, block_rect)
                elif bloco_anterior.y == bloco_seguinte.y:
                    tela.blit(self.corpo_h, block_rect)
                elif ((bloco_anterior.x == -1 and bloco_seguinte.y == -1) 
                      or (bloco_anterior.y == -1 and bloco_seguinte.x == -1)):
                    tela.blit(self.curva_NO, block_rect)
                elif ((bloco_anterior.x == -1 and bloco_seguinte.y == 1)
                       or (bloco_anterior.y == 1 and bloco_seguinte.x == -1)):
                    tela.blit(self.curva_SO, block_rect)
                elif ((bloco_anterior.x == 1 and bloco_seguinte.y == -1)
                       or (bloco_anterior.y == -1 and bloco_seguinte.x == 1)):
                    tela.blit(self.curva_NL, block_rect)
                elif ((bloco_anterior.x == 1 and bloco_seguinte.y == 1)
                       or (bloco_anterior.y == 1 and bloco_seguinte.x == 1)):
                    tela.blit(self.curva_SL, block_rect)

    def update_cabeca_graphics(self):
        cabeca_relation = self.body[1] - self.body[0]
        if cabeca_relation == Vector2(1,0): self.cabeca = self.cabecaO
        elif cabeca_relation == Vector2(-1,0): self.cabeca = self.cabecaL
        elif cabeca_relation == Vector2(0,1): self.cabeca = self.cabecaN
        elif cabeca_relation == Vector2(0,-1): self.cabeca = self.cabecaS

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

    def move_cobra(self):
        self.update_direction()

        if self.novo_corpo:
            new_cabeca = self.body[0] + self.direction
            self.body.appendleft(new_cabeca)
            self.novo_corpo = False
        else:
            new_cabeca = self.body[0] + self.direction
            self.body.appendleft(new_cabeca)
            self.body.pop()

    def add_block(self):
        self.novo_corpo = True

class Main:
    def __init__(self):
        self.cobra = cobra()
        self.fruta = fruta()

    def update(self):
        self.cobra.move_cobra()
        self.check_collision()
        self.check_fail()

    def design_elements(self, surface):
        self.design_fundo(surface)
        self.fruta.draw(surface)
        self.cobra.design_cobra()
        self.design_score(surface)

    def check_collision(self):
        if self.fruta.pos == self.cobra.body[0]:
            self.fruta.randomize()
            while self.fruta.pos in self.cobra.body:
                self.fruta.randomize()

            self.cobra.add_block()

    def check_fail(self):
        if not 0 <= self.cobra.body[0].x < num_cel or \
                not 0 <= self.cobra.body[0].y < num_cel:
            self.game_over()

        for block in list(self.cobra.body)[1:]:
            if block == self.cobra.body[0]:
                self.game_over()

    def game_over(self):
        self.cobra.reset()

    def design_fundo(self, surface):
        surface.fill(roxo_1)
        for row in range(num_cel):
            if row % 2 == 0:
                for col in range(num_cel):
                    if col % 2 == 0:
                        fundo_rect = pygame.Rect(
                            col * tamanho_cel, 
                            row * tamanho_cel, 
                            tamanho_cel, tamanho_cel
                                                 )
                        pygame.draw.rect(surface, roxo_2, fundo_rect)
            else:
                for col in range(num_cel):
                    if col % 2 != 0:
                        fundo_rect = pygame.Rect(col * tamanho_cel, 
                                                 row * tamanho_cel, tamanho_cel, tamanho_cel)
                        pygame.draw.rect(surface, roxo_2, fundo_rect)

    def design_score(self, surface):
        score_text = str(len(self.cobra.body) - 3)
        score_surface = fonte_letra.render(score_text, True, cor_texto)
        score_x = int(tamanho_cel * num_cel - 60)
        score_y = int(tamanho_cel * num_cel - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        bg_rect = pygame.Rect(
            score_rect.left - 6,
            score_rect.top - 6,
            score_rect.width + 12,
            score_rect.height + 12
        )
        pygame.draw.rect(surface, cor_background, bg_rect)
        pygame.draw.rect(surface, cor_texto, bg_rect, 2)
        surface.blit(score_surface, score_rect)

    def queue_input(self, direction):
        target_dir = direction
        if not self.cobra.direction_queue:
            last_dir = self.cobra.direction
        else:
            last_dir = self.cobra.direction_queue[-1]

        if target_dir != -last_dir:
            self.cobra.direction_queue.append(target_dir)

main_game = Main()
pygame.time.set_timer(MOVE_UPDATE_EVENT, cobra_SPEED_MS)

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

    main_game.design_elements(tela)
    pygame.display.update()
    clock.tick(FPS)
