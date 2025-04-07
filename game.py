import pygame
from components import button
import cv2
import random

pygame.init()

# CONFIGURAÇÕES GLOBAIS
running = True
pygame.display.set_caption("Campo minado")
clock = pygame.time.Clock()
bg_sobre = pygame.image.load("images/wallpaper.jpg")

tela = "menu"

# CONFIGURAÇÕES DA JANELA
width, height = 950, 600
screen = pygame.display.set_mode((width, height))

# CARREGAR O VÍDEO
video_de_fundo = "videos/stock_wallpaper.mp4"
captura_do_video = cv2.VideoCapture(video_de_fundo)

# ==================== BOTÕES ====================
botao_jogar = pygame.image.load("images/buttons/botao_jogar.png").convert_alpha()
botao_como_jogar = pygame.image.load("images/buttons/botao_como_jogar.png").convert_alpha()
botao_voltar = pygame.image.load("images/buttons/botao_voltar.png").convert_alpha()
botao_sair = pygame.image.load("images/buttons/botao_sair.png").convert_alpha()

scale = 0.12
start_button = button.Button(width // 2.5, height // 4, botao_jogar, scale)
about_button = button.Button(width // 2.5, height // 4 + 50, botao_como_jogar, scale)
exit_button = button.Button(width // 2.5, height // 4 + 100, botao_sair, scale)
back_button = button.Button(width // 60, height // 4 + -140, botao_voltar, scale - 0.02)

# ==================== JOGO CAMPO MINADO ====================
TAMANHO_CELULA = 40
GRID_LINHAS = 10
GRID_COLUNAS = 10
NUM_BOMBAS = 10
OFFSET_X = (width - GRID_COLUNAS * TAMANHO_CELULA) // 2
OFFSET_Y = (height - GRID_LINHAS * TAMANHO_CELULA) // 2

font = pygame.font.SysFont(None, 30)

def criar_grid():
    grid = [[0 for _ in range(GRID_COLUNAS)] for _ in range(GRID_LINHAS)]
    bombas = set()
    while len(bombas) < NUM_BOMBAS:
        linha = random.randint(0, GRID_LINHAS - 1)
        coluna = random.randint(0, GRID_COLUNAS - 1)
        if (linha, coluna) not in bombas:
            bombas.add((linha, coluna))
            grid[linha][coluna] = -1  # -1 é bomba

    for linha in range(GRID_LINHAS):
        for coluna in range(GRID_COLUNAS):
            if grid[linha][coluna] == -1:
                continue
            contador = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = linha + dx, coluna + dy
                    if 0 <= nx < GRID_LINHAS and 0 <= ny < GRID_COLUNAS and grid[nx][ny] == -1:
                        contador += 1
            grid[linha][coluna] = contador
    return grid, bombas

def revelar(grid, visivel, linha, coluna):
    if not (0 <= linha < GRID_LINHAS and 0 <= coluna < GRID_COLUNAS):
        return
    if visivel[linha][coluna]:
        return
    visivel[linha][coluna] = True
    if grid[linha][coluna] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    revelar(grid, visivel, linha + dx, coluna + dy)

grid, bombas = criar_grid()
visivel = [[False for _ in range(GRID_COLUNAS)] for _ in range(GRID_LINHAS)]

def desenhar_jogo():
    for linha in range(GRID_LINHAS):
        for coluna in range(GRID_COLUNAS):
            x = OFFSET_X + coluna * TAMANHO_CELULA
            y = OFFSET_Y + linha * TAMANHO_CELULA
            rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
            if visivel[linha][coluna]:
                pygame.draw.rect(screen, (200, 200, 200), rect)
                valor = grid[linha][coluna]
                if valor > 0:
                    texto = font.render(str(valor), True, (0, 0, 0))
                    screen.blit(texto, (x + 12, y + 10))
                elif valor == -1:
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, 10)
            else:
                pygame.draw.rect(screen, (100, 100, 100), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

def resetar_jogo():
    global grid, bombas, visivel
    grid, bombas = criar_grid()
    visivel = [[False for _ in range(GRID_COLUNAS)] for _ in range(GRID_LINHAS)]

# ==================== LOOP PRINCIPAL ====================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if tela == "jogo" and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            coluna = (x - OFFSET_X) // TAMANHO_CELULA
            linha = (y - OFFSET_Y) // TAMANHO_CELULA
            if 0 <= linha < GRID_LINHAS and 0 <= coluna < GRID_COLUNAS:
                if grid[linha][coluna] == -1:
                    resetar_jogo()
                else:
                    revelar(grid, visivel, linha, coluna)

    # TELA DE MENU
    if tela == "menu":
        if start_button.is_clicked(event):
            tela = "jogo"
            resetar_jogo()
        elif about_button.is_clicked(event):
            tela = "sobre"
        elif exit_button.is_clicked(event):
            running = False

    if back_button.is_clicked(event):
        tela = "menu"

    if tela == "menu":
        video, frame = captura_do_video.read()
        if not video:
            captura_do_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame = cv2.resize(frame, (width, height))
        frame = cv2.GaussianBlur(frame, (25, 25), 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface, -90)
        screen.blit(frame_surface, (0, 0))
        start_button.draw()
        about_button.draw()
        exit_button.draw()

    elif tela == "jogo":
        screen.fill((0, 0, 0))
        desenhar_jogo()
        back_button.draw()

    elif tela == "sobre":
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        screen.blit(bg_sobre, (-150, -150))
        back_button.draw()

        sobre = [
            ("Sobre o jogo", 200),
            ("1 - Clique em um quadrado para revelar o número de minas ao redor.", 150),
            ("2 - Evite clicar em quadrados com minas.", 100),
            ("3 - Use os números para deduzir onde estão as minas.", 50),
            ("4 - Revele todos os quadrados sem minas para vencer.", 0)
        ]
        for texto, posicao in sobre:
            texto_sobre = font.render(texto, True, (255, 255, 255))
            screen.blit(texto_sobre, (width // 2 - texto_sobre.get_width() // 2, height // 2 - texto_sobre.get_height() // 2 - posicao))

        creditos = [
            ("Feito Por: ", 60),
            ("- Angelo Miguel Requenha", 100),
            ("- Dinaê Pfiffer", 140),
            ("- Bruno de Queiróz", 180)
        ]
        for texto, posicao in creditos:
            texto_equipe = font.render(texto, True, (255, 255, 255))
            screen.blit(texto_equipe, (width // 2 - texto_equipe.get_width() // 2, height // 2 - texto_equipe.get_height() // 2 + posicao))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
