import pygame
import sys

import random #

#sem essa biblioteca nao vai funcionar a função de redes sociais
import webbrowser


# 1. Configurações Iniciais
pygame.init()
LARGURA =(25 * 25) + (2 * 60)
ALTURA = (25 * 20) + (2 * 60)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("For_Snake")

imagem_titulo = pygame.image.load('titulo.png')
cor_fundo = (0x1e, 0x16, 0x47)
cor_botao = (0xFF, 0xFF, 0x00)

#imagem dos icones 
################################3###############
imagem_insta = pygame.image.load('Instagram.png')
imagem_github = pygame.image.load('Github.webp')
imagem_linkedin = pygame.image.load('Youtube.png')#todo lugar que se referir ao linkedin, agora e o toutube, mudei so o essencial pra funcionar por enquanto

lado_logo = 40
margem_logo = 40

imagem_insta = pygame.transform.smoothscale(imagem_insta, (lado_logo, lado_logo))
imagem_github = pygame.transform.smoothscale(imagem_github, (lado_logo, lado_logo))
imagem_linkedin = pygame.transform.smoothscale(imagem_linkedin, (lado_logo, lado_logo))


rect_botao_insta = imagem_insta.get_rect(bottomleft=(margem_logo, ALTURA -20))
rect_botao_linkedin = imagem_linkedin.get_rect(bottomleft=((margem_logo*2) + lado_logo, ALTURA -20))
rect_botao_github = imagem_github.get_rect(bottomleft=((margem_logo*3) + (lado_logo*2), ALTURA -20))

#####################################################

asterisco = pygame.image.load('asterisco.png')
asterisco = pygame.transform.smoothscale(asterisco, (lado_logo, lado_logo))






# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
VERMELHO = (255, 0, 0)
VERDE_BOTAO = (0, 200, 0)

# Fontes
fonte_titulo = pygame.font.SysFont("arial", 60)
#fonte_botao = pygame.font.SysFont("arial", 40)
fonte_botao = pygame.font.Font(None, 40)



#PONTOS e busca do arquivo ###############################
game_font = pygame.font.Font(None, 24)
score_tabela = pygame.Rect(LARGURA/2 - 100, ALTURA - 150, 200, 50)

lista_de_linhas = []
try:
    with open("score.txt", "r", encoding="utf-8") as arquivo:
        texto_completo = arquivo.read()
        lista_de_linhas = texto_completo.splitlines() #essa linha ta separando uma lista de linhas do arquivo
        arquivo.close() 
except FileNotFoundError:
    with open('score.txt', 'x', encoding='utf-8') as arquivo:
        arquivo.write("0")
        arquivo.close() 
        pass
    
        
################################

# --- DEFINIÇÃO DO BOTÃO ---
# Criamos um retângulo: (x, y, largura, altura)
botao_play = pygame.Rect(LARGURA/2 - 100, ALTURA/2 - 25, 200, 50)

# Variável de Estado (Começa no Menu)
estado_jogo = "MENU" 

# Loop Principal
relogio = pygame.time.Clock()
FPS = 10
#contador_fps = 0


while True:
    tela.fill(PRETO) # Limpa a tela a cada frame
    
    # --- GERENCIAMENTO DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Eventos Específicos do MENU
        if estado_jogo == "MENU":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clique esquerdo
                    # Se o mouse colidir com o retângulo do botão
                    if botao_play.collidepoint(evento.pos):
                        estado_jogo = "JOGO" # Troca o estado para o jogo
                    
                    #paginas da web
                    if rect_botao_insta.collidepoint(evento.pos):
                        webbrowser.open("https://www.instagram.com/forcodeufrj/")
                    
                    if rect_botao_linkedin.collidepoint(evento.pos):
                        webbrowser.open("https://www.youtube.com/@for_code/featured")

                    if rect_botao_github.collidepoint(evento.pos):
                        webbrowser.open("https://github.com/forcodeufrj")
                
    
    
    if estado_jogo == "MENU":
        
        tela.fill(cor_fundo)
        
        
        n = random.randint(1, 20)
        for i in range(n):
            tela.blit(asterisco, (random.randint(1, LARGURA),random.randint(1, ALTURA)))
        contador_fps=0  
            
        tela.blit(imagem_titulo, ((LARGURA - imagem_titulo.get_width()) // 2, ALTURA / 2 - 250))  

        
        tela.blit(imagem_titulo, ((LARGURA - imagem_titulo.get_width()) // 2, ALTURA / 2 - 250))  
        tela.blit(imagem_insta,rect_botao_insta)
        tela.blit( imagem_linkedin, rect_botao_linkedin)
        tela.blit(imagem_github,rect_botao_github)
        
        #Botão
        pygame.draw.rect(tela, cor_botao, botao_play)
        
        # Texto do Botão
        texto_botao = fonte_botao.render("START", True, PRETO)
        rect_texto_botao = texto_botao.get_rect(center=botao_play.center)
        tela.blit(texto_botao, rect_texto_botao)


        
        pygame.draw.rect(tela, cor_botao, score_tabela)
        texto_score = game_font.render(f"SCORE:\n{lista_de_linhas[-1]}", True, PRETO)
        rect_score_tabela = texto_score.get_rect(center=score_tabela.center)
        tela.blit(texto_score, rect_score_tabela)
        
    
    elif estado_jogo == "JOGO":
        
        #esse import ta funcionando na minha maquina
        #mas pode ser q precise colocar todo o codigo do jogo aqui pra pegar
        import neu_code.py

    
    pygame.display.flip()
    relogio.tick(FPS)