import pygame, sys, random
from pygame.math import Vector2
pygame.init()
pygame.display.set_caption('semata')
num_cel = 20
tamanho_celula = 32
screen = pygame.display.set_mode((num_cel * tamanho_celula, num_cel * tamanho_celula))
clock = pygame.time.Clock()

class fruta(pygame.sprite.Sprite):
        def __init__(self):
            self.randomize()
        def draw_fruit(self):
            self.image = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/fruta.png')
            fruit_rect = pygame.Rect(int(self.pos.x * tamanho_celula), int(self.pos.y * tamanho_celula), tamanho_celula, tamanho_celula)
            screen.blit(self.image, fruit_rect)
        def randomize(self):
            self.x = random.randint(0,num_cel - 1)
            self.y = random.randint(0,num_cel - 1)
            self.pos = Vector2(self.x, self.y)
class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.headN = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/headN.png')
        self.headS = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/headS.png')
        self.headO = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/headO.png')
        self.headL = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/headL.png')

        self.cauda_N = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/cauda_N.png')
        self.cauda_S = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/cauda_S.png')
        self.cauda_O = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/cauda_O.png')  
        self.cauda_L = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/cauda_L.png')  

        self.corpo_h = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/corpo_h.png')
        self.corpo_v = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/corpo_v.png')

        self.curva_NL = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/norte_leste.png')
        self.curva_NO = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/norte_oeste.png')
        self.curva_SL = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/sul_leste.png')
        self.curva_SO = pygame.image.load('C:/Users/Behael/Desktop/Projeto/trabalhos/Trabalhos/mkt-for_snake/for_code-marketing-pygame/Nova pasta/sul_oeste.png')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_cauda_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * tamanho_celula)
            y_pos = int(block.y * tamanho_celula) 
            block_rect = pygame.Rect(x_pos, y_pos, tamanho_celula, tamanho_celula)
            
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

    def movimento(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
class main:
    def __init__(self):
        self.snake = Snake()
        self.fruta = fruta()

    def update(self):
        self.snake.movimento()
        self.check_colission()
        self.check_fail()
    
    def draw_elements(self):
        screen.fill((157, 0 , 200))
        self.snake.draw_snake()
        self.fruta.draw_fruit()
        pygame.display.update()
    
    def check_colission(self):
        if self.fruta.pos == self.snake.body[0]:
            self.fruta.randomize()           
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < num_cel or not 0 <= self.snake.body[0].y < num_cel:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)
main_game = main()
Snake = main_game.snake

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    Snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    Snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    Snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    Snake.direction = Vector2(1,0)
    
    main_game.draw_elements()
    clock.tick(60)
    