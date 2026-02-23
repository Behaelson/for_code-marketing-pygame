import pygame
import sys
import random
from pygame.math import Vector2
from collections import deque
from pathlib import Path

# Path
base_dir = Path(__file__).resolve().parent #pega caminho da pasta onde o jogo esta
usr_path = base_dir / 'assets'
sounds_dir = base_dir / 'sounds'
class Caminhos:
    def __init__(self, folder_path):
       path = Path(folder_path)
       for f in path.rglob("*"):
           if f.is_file():
               self.__dict__[f.stem] = f

    def __getattr__(self, name):
        raise AttributeError(f"ERRO: arquivo '{name}' não encontrado.")
caminho = Caminhos(usr_path)

tamanho_cel = 25  
num_cel_x = 25
num_cel_y = 20
offset = 60 

largura_tela = (tamanho_cel * num_cel_x) + (2 * offset)
altura_tela = (tamanho_cel * num_cel_y) + (2 * offset)

FPS = 30
MOVE_UPDATE_EVENT = pygame.USEREVENT + 1
velocidade_cobra_ms = 150

roxo_1      =  (97, 74, 211)
roxo_2      =  (30, 22, 71)
cor_cobra   =  (56, 74, 12)
cor_fruta   =  (231, 71, 29)
UI_BG_COLOR =  (20, 15, 50)
cor_texto   =  (255, 255, 255)
cor_score   =  (167, 209, 61)
cor_borda   =  (255, 255, 0)
cor_botao   =  (40, 30, 90)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
sounds_dir.mkdir(exist_ok=True)

def carregar_som(nome_arquivo, volume=1.0):
    if not pygame.mixer.get_init():
        return None
    arquivo_som = sounds_dir / nome_arquivo
    if not arquivo_som.exists():
        print(f"arquivo de som não encontrado: {arquivo_som.name}")
        return None
    try:
        som = pygame.mixer.Sound(str(arquivo_som))
        som.set_volume(volume)
        return som
    except Exception as e:
        print(f"AVISO: Som '{arquivo_som.name}' não carregado. Erro: {e}")
        return None

def tocar_som(som):
    if som is None:
        return
    try:
        som.play()
    except Exception as e:
        print(f"AVISO: Não foi possível tocar um efeito sonoro. Erro: {e}")

def iniciar_soundtrack():
    if not pygame.mixer.get_init():
        return
    arquivo_trilha = sounds_dir / "soundtrack.mp3"
    if not arquivo_trilha.exists():
        print(f"AVISO: trilha sonora não encontrada: {arquivo_trilha.name}")
        return
    try:
        pygame.mixer.music.load(str(arquivo_trilha))
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"AVISO: Trilha sonora não carregada. Erro: {e}")

som_comer_a_maca = carregar_som("comer_a_maca.mp3", 0.7)
som_bater_na_parede = carregar_som("bater_na_parede.mp3", 0.8)
som_iniciar_jogo = carregar_som("iniciar_jogo.mp3", 0.9)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("FOR_SNAKE")
clock = pygame.time.Clock()

game_font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 40)
score_font = pygame.font.Font(None, 32)

class fruta:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.randomize()
        try:
            img = pygame.image.load(caminho.fruta).convert_alpha()
            self.image = pygame.transform.scale(img, (tamanho_cel, tamanho_cel))
        except:
            self.image = pygame.Surface((tamanho_cel, tamanho_cel))
            self.image.fill(cor_fruta)

    def randomize(self):
        self.x = random.randint(0, num_cel_x - 1)
        self.y = random.randint(0, num_cel_y - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self, surface):
        fruta_rect = pygame.Rect(
            int(self.pos.x * tamanho_cel),
            int(self.pos.y * tamanho_cel),
            tamanho_cel,
            tamanho_cel
        )
        surface.blit(self.image, fruta_rect)      

class cobra:
    def __init__(self):
        self.reset()
        self.carregar_sprite()

    def carregar_sprite(self):
        def carregar_escala(name_or_path):
            try:
                if isinstance(name_or_path, Path):
                    path = name_or_path
                else:
                    path = caminho[name_or_path]
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (tamanho_cel, tamanho_cel))
            except Exception:
                surf = pygame.Surface((tamanho_cel, tamanho_cel), pygame.SRCALPHA)
                surf.fill(cor_cobra)
                return surf

        self.headN = carregar_escala(caminho.headN)
        self.headS = carregar_escala(caminho.headS)
        self.headO = carregar_escala(caminho.headO)
        self.headL = carregar_escala(caminho.headL)

        self.head_cN = carregar_escala(caminho.head_cN)
        self.head_cS = carregar_escala(caminho.head_cS)
        self.head_cO = carregar_escala(caminho.head_cO)
        self.head_cL = carregar_escala(caminho.head_cL)

        self.cauda_N = carregar_escala(caminho.cauda_N)
        self.cauda_S = carregar_escala(caminho.cauda_S)
        self.cauda_O = carregar_escala(caminho.cauda_O)
        self.cauda_L = carregar_escala(caminho.cauda_L)
        
        self.corpo_h = carregar_escala(caminho.corpo_h)
        self.corpo_v = carregar_escala(caminho.corpo_v)

        self.curva_NL = carregar_escala(caminho.curva_NL)
        self.curva_NO = carregar_escala(caminho.curva_NO)
        self.curva_SL = carregar_escala(caminho.curva_SL)
        self.curva_SO = carregar_escala(caminho.curva_SO)

    def reset(self):
        self.body = deque([Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.direction_queue = deque()

    def design_cobra(self, surface, fruta_pos):
        self.update_head_graphics()
        self.update_cauda_graphics()
        self.sprite_head_comer(fruta_pos)

        for index, block in enumerate(self.body):
            x_pos = int(block.x * tamanho_cel)
            y_pos = int(block.y * tamanho_cel) 
            block_rect = pygame.Rect(x_pos, y_pos, tamanho_cel, tamanho_cel)
            
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
        
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headO
        elif head_relation == Vector2(-1,0): self.head = self.headL
        elif head_relation == Vector2(0,1): self.head = self.headN
        elif head_relation == Vector2(0,-1): self.head = self.headS

    def sprite_head_comer(self, fruta_pos):
        # Calcula a diferença entre a cabeça e a fruta
        distancia_vetor = fruta_pos - self.body[0]
        
        # Se a distância for de apenas 1 célula (adjacente)
        if distancia_vetor.length() == 1:
            if distancia_vetor == Vector2(0, -1): self.head = self.head_cN
            elif distancia_vetor == Vector2(0, 1): self.head = self.head_cS
            elif distancia_vetor == Vector2(-1, 0): self.head = self.head_cO
            elif distancia_vetor == Vector2(1, 0): self.head = self.head_cL

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
        tocar_som(som_comer_a_maca)

class Main:
    def __init__(self):
        self.cobra = cobra()
        self.fruta = fruta()
        
        # Dimensões totais da área de jogo (grid)
        self.game_width = num_cel_x * tamanho_cel
        self.game_height = num_cel_y * tamanho_cel
        self.game_surface = pygame.Surface((self.game_width, self.game_height))
        self.high_score = 0
        
        
        self.bg_image = None
        try:
            bg_source = pygame.image.load(caminho.grid).convert()
            self.bg_image = pygame.transform.scale(bg_source, (670, self.game_height))
            print("SUCESSO: Fundo do grid carregado!")
        except Exception as e:
            print(f"AVISO: Fundo não carregado. Usando padrão. Erro: {e}")
        # -------------------------------------
        
    def update(self):
        self.cobra.move_cobra()
        self.check_collision()
        self.check_fail()

    def draw_elements(self, main_tela):
        main_tela.fill(UI_BG_COLOR)
        
        # Desenha o jogo na superfície interna
        self.draw_fundo(self.game_surface)
        self.fruta.draw(self.game_surface)
        self.cobra.design_cobra(self.game_surface, self.fruta.pos)
        
        # Posiciona o jogo no centro da moldura
        game_rect = self.game_surface.get_rect(topleft=(offset, offset))
        
        main_tela.blit(self.game_surface, game_rect)
        pygame.draw.rect(main_tela, cor_borda, game_rect, 2)
        
        # Desenha toda a UI no topo
        self.draw_ui(main_tela)

    def draw_fundo(self, surface):
        if self.bg_image is not None:
            surface.blit(self.bg_image, (-23, 0))
        else:
            # Se não existir imagem, desenha o xadrez antigo
            surface.fill(roxo_1)
            for row in range(num_cel_y):
                for col in range(num_cel_x):
                    if (row + col) % 2 == 0:
                        fundo_rect = pygame.Rect(col * tamanho_cel, row * tamanho_cel, tamanho_cel, tamanho_cel)
                        pygame.draw.rect(surface, roxo_2, fundo_rect)
       

    def draw_ui(self, surface):
        mid_y = offset // 2

        score_val = str(len(self.cobra.body) - 3)
        score_text = score_font.render(f"PONTUAÇÃO: {score_val}", True, cor_texto)
        score_rect = score_text.get_rect(midleft=(60, mid_y)) 
        surface.blit(score_text, score_rect)

        title_surf = title_font.render("FOR_SNAKE", True, cor_borda)
        title_rect = title_surf.get_rect(center=(largura_tela // 2, mid_y))
        surface.blit(title_surf, title_rect)

        hs_text = score_font.render(f"RECORDE: {self.high_score}", True, cor_texto)
        hs_rect = hs_text.get_rect(midright=(largura_tela - 60, mid_y)) 
        surface.blit(hs_text, hs_rect)

    def check_collision(self):
        if self.fruta.pos == self.cobra.body[0]:
            self.fruta.randomize()
            while self.fruta.pos in self.cobra.body:
                self.fruta.randomize()
            self.cobra.add_block()
            self.cobra.play_crunch_sound()

    def check_fail(self):
        if not 0 <= self.cobra.body[0].x < num_cel_x or not 0 <= self.cobra.body[0].y < num_cel_y:
            tocar_som(som_bater_na_parede)
            self.game_over()
        for block in list(self.cobra.body)[1:]:
            if block == self.cobra.body[0]:
                self.game_over()

    def game_over(self):
        current_score = len(self.cobra.body) - 3
        if current_score > self.high_score:
            self.high_score = current_score
        self.cobra.reset()

    def queue_input(self, direction):
        target_dir = direction
        if not self.cobra.direction_queue:
            last_dir = self.cobra.direction
        else:
            last_dir = self.cobra.direction_queue[-1]
        if target_dir != -last_dir:
            self.cobra.direction_queue.append(target_dir)

main_game = Main()
iniciar_soundtrack()
tocar_som(som_iniciar_jogo)
pygame.time.set_timer(MOVE_UPDATE_EVENT, velocidade_cobra_ms)

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

    main_game.draw_elements(tela)
    pygame.display.update()
    clock.tick(FPS)
