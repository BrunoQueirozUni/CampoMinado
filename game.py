# Importa as bibliotecas
import pygame
import cv2
import random
from components import button  # Arquivo separado que define os botões

# Inicializa o Pygame
pygame.init()

# ========== CONFIGURAÇÕES GERAIS ==========
executando = True
pygame.display.set_caption("Campo Minado")
relogio = pygame.time.Clock()

# Título e fundo
imagem_sobre = pygame.image.load("images/wallpaper.jpg")

# Variáveis de controle
tela_atual = "menu"      # Pode ser "menu", "jogo" ou "sobre"
tela_final = None        # Será "vitoria" ou "derrota"
pontuacao = 0            # Começa com 0 pontos

# Tamanho da janela
largura, altura = 950, 600
tela = pygame.display.set_mode((largura, altura))

# ========== VÍDEO DE FUNDO ==========
video_de_fundo = "videos/stock_wallpaper.mp4"
captura_video = cv2.VideoCapture(video_de_fundo)

# ========== BOTÕES ==========
# Carrega as imagens dos botões
imagem_jogar = pygame.image.load("images/buttons/botao_jogar.png").convert_alpha()
imagem_como_jogar = pygame.image.load("images/buttons/botao_como_jogar.png").convert_alpha()
imagem_sair = pygame.image.load("images/buttons/botao_sair.png").convert_alpha()
imagem_voltar = pygame.image.load("images/buttons/botao_voltar.png").convert_alpha()

# Cria os botões com posição e tamanho
escala = 0.12
botao_jogar = button.Button(largura // 2.5, altura // 4, imagem_jogar, escala)
botao_como_jogar = button.Button(largura // 2.5, altura // 4 + 50, imagem_como_jogar, escala)
botao_sair = button.Button(largura // 2.5, altura // 4 + 100, imagem_sair, escala)
botao_voltar = button.Button(largura // 60, altura // 4 - 140, imagem_voltar, escala - 0.02)

# ========== CONFIGURAÇÃO DO CAMPO MINADO ==========
tamanho_celula = 40
linhas_grade = 10
colunas_grade = 10
quantidade_bombas = 10

# Centraliza a grade no meio da tela
deslocamento_x = (largura - colunas_grade * tamanho_celula) // 2
deslocamento_y = (altura - linhas_grade * tamanho_celula) // 2

# Fonte para os textos
fonte = pygame.font.SysFont(None, 30)

# Cria uma grade com bombas e números ao redor
def criar_grade():
    grade = [[0 for _ in range(colunas_grade)] for _ in range(linhas_grade)]
    bombas = set()

    while len(bombas) < quantidade_bombas:
        linha = random.randint(0, linhas_grade - 1)
        coluna = random.randint(0, colunas_grade - 1)
        if (linha, coluna) not in bombas:
            bombas.add((linha, coluna))
            grade[linha][coluna] = -1  # -1 representa bomba

    # Preenche os números ao redor das bombas
    for linha in range(linhas_grade):
        for coluna in range(colunas_grade):
            if grade[linha][coluna] == -1:
                continue
            contador = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = linha + dx, coluna + dy
                    if 0 <= nx < linhas_grade and 0 <= ny < colunas_grade and grade[nx][ny] == -1:
                        contador += 1
            grade[linha][coluna] = contador

    return grade, bombas

# Função para revelar uma célula e as vizinhas se não tiver bomba
def revelar(grade, visivel, linha, coluna):
    global pontuacao
    if not (0 <= linha < linhas_grade and 0 <= coluna < colunas_grade):
        return
    if visivel[linha][coluna]:
        return

    visivel[linha][coluna] = True
    if grade[linha][coluna] == 0:
        pontuacao += 10
        # Revela vizinhos automaticamente
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    revelar(grade, visivel, linha + dx, coluna + dy)
    elif grade[linha][coluna] > 0:
        pontuacao += 10

# Criação inicial do campo
grade, bombas = criar_grade()
visivel = [[False for _ in range(colunas_grade)] for _ in range(linhas_grade)]

# Desenha o campo minado
def desenhar_jogo():
    for linha in range(linhas_grade):
        for coluna in range(colunas_grade):
            x = deslocamento_x + coluna * tamanho_celula
            y = deslocamento_y + linha * tamanho_celula
            retangulo = pygame.Rect(x, y, tamanho_celula, tamanho_celula)

            if visivel[linha][coluna]:
                pygame.draw.rect(tela, (200, 200, 200), retangulo)
                valor = grade[linha][coluna]
                if valor > 0:
                    texto = fonte.render(str(valor), True, (0, 0, 0))
                    tela.blit(texto, (x + 12, y + 10))
                elif valor == -1:
                    pygame.draw.circle(tela, (255, 0, 0), retangulo.center, 10)
            else:
                pygame.draw.rect(tela, (100, 100, 100), retangulo)

            pygame.draw.rect(tela, (0, 0, 0), retangulo, 1)

    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
    tela.blit(texto_pontos, (10, 10))

# Reinicia o jogo
def resetar_jogo():
    global grade, bombas, visivel, pontuacao, tela_final
    grade, bombas = criar_grade()
    visivel = [[False for _ in range(colunas_grade)] for _ in range(linhas_grade)]
    pontuacao = 0
    tela_final = None

# Verifica se o jogador venceu
def checar_vitoria():
    for linha in range(linhas_grade):
        for coluna in range(colunas_grade):
            if grade[linha][coluna] != -1 and not visivel[linha][coluna]:
                return False
    return True

# Tela de vitória ou derrota
def desenhar_tela_final():
    tela.fill((0, 0, 0))
    mensagem = "Você Venceu!" if tela_final == "vitoria" else "Você Perdeu!"
    cor = (0, 255, 0) if tela_final == "vitoria" else (255, 0, 0)

    texto_mensagem = fonte.render(mensagem, True, cor)
    texto_pontos = fonte.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))

    tela.blit(texto_mensagem, (largura // 2 - texto_mensagem.get_width() // 2, altura // 2 - 60))
    tela.blit(texto_pontos, (largura // 2 - texto_pontos.get_width() // 2, altura // 2))
    botao_voltar.draw()

# ========== LOOP PRINCIPAL ==========
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        # Clicar no campo do jogo
        if tela_atual == "jogo" and tela_final is None and evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            coluna = (x - deslocamento_x) // tamanho_celula
            linha = (y - deslocamento_y) // tamanho_celula
            if 0 <= linha < linhas_grade and 0 <= coluna < colunas_grade:
                if grade[linha][coluna] == -1:
                    tela_final = "derrota"
                    pontuacao = 0
                else:
                    revelar(grade, visivel, linha, coluna)
                    if checar_vitoria():
                        tela_final = "vitoria"

    # === MENU PRINCIPAL ===
    if tela_atual == "menu":
        if botao_jogar.is_clicked(evento):
            tela_atual = "jogo"
            resetar_jogo()
        elif botao_como_jogar.is_clicked(evento):
            tela_atual = "sobre"
        elif botao_sair.is_clicked(evento):
            executando = False

    if botao_voltar.is_clicked(evento):
        tela_atual = "menu"

    # === TELAS ===
    if tela_atual == "menu":
        sucesso, quadro = captura_video.read()
        if not sucesso:
            captura_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        quadro = cv2.resize(quadro, (largura, altura))
        quadro = cv2.GaussianBlur(quadro, (25, 25), 0)
        quadro = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
        superficie_quadro = pygame.surfarray.make_surface(quadro)
        superficie_quadro = pygame.transform.rotate(superficie_quadro, -90)
        tela.blit(superficie_quadro, (0, 0))

        botao_jogar.draw()
        botao_como_jogar.draw()
        botao_sair.draw()

    elif tela_atual == "jogo":
        if tela_final:
            desenhar_tela_final()
        else:
            tela.fill((0, 0, 0))
            desenhar_jogo()
            botao_voltar.draw()

    elif tela_atual == "sobre":
        tela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 36)
        tela.blit(imagem_sobre, (-150, -150))
        botao_voltar.draw()

        explicacao = [
            ("Sobre o jogo", 200),
            ("1 - Clique em um quadrado para revelar o número de minas ao redor.", 150),
            ("2 - Evite clicar em quadrados com minas.", 100),
            ("3 - Use os números para deduzir onde estão as minas.", 50),
            ("4 - Revele todos os quadrados sem minas para vencer.", 0)
        ]
        for texto, posicao in explicacao:
            linha_texto = fonte.render(texto, True, (255, 255, 255))
            tela.blit(linha_texto, (largura // 2 - linha_texto.get_width() // 2, altura // 2 - linha_texto.get_height() // 2 - posicao))

        creditos = [
            ("Feito Por: ", 60),
            ("- Angelo Miguel Requenha", 100),
            ("- Dinaê Pfiffer", 140),
            ("- Bruno de Queiróz", 180)
        ]
        for texto, posicao in creditos:
            linha_credito = fonte.render(texto, True, (255, 255, 255))
            tela.blit(linha_credito, (largura // 2 - linha_credito.get_width() // 2, altura // 2 - linha_credito.get_height() // 2 + posicao))

    pygame.display.update()
    relogio.tick(30)

# Finaliza o Pygame
pygame.quit()
