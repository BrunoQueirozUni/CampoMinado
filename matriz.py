import pygame
import sys
import random
from collections import deque

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Campo Minado")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (0, 0, 200)

font = pygame.font.Font(None, 36)

input_active = True
user_text = ''
tam = 0
cell_size = 40
bombs = []
reveal = []
bomb_count = []

def gerar_bombas(tam, qtd_bombas):
    posicoes = [(i, j) for i in range(tam) for j in range(tam)]
    return random.sample(posicoes, qtd_bombas)

def contar_bombas_ao_redor(i, j, bombas, tam):
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            ni, nj = i + di, j + dj
            if 0 <= ni < tam and 0 <= nj < tam and (ni, nj) in bombs:
                count += 1
    return count

def revelar_area_vazia(i, j):
    fila = deque()
    fila.append((i, j))

    while fila:
        x, y = fila.popleft()
        if not reveal[x][y]:
            reveal[x][y] = True
            if bomb_count[x][y] == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < tam and 0 <= ny < tam and not reveal[nx][ny]:
                            fila.append((nx, ny))

def iniciar_jogo():
    global reveal, bombs, bomb_count, input_active, user_text

    reveal = [[False for _ in range(tam)] for _ in range(tam)]
    bombs = gerar_bombas(tam, tam * tam // 6)
    bomb_count = [[0 for _ in range(tam)] for _ in range(tam)]

    for i in range(tam):
        for j in range(tam):
            bomb_count[i][j] = contar_bombas_ao_redor(i, j, bombs, tam)

    input_active = False
    user_text = ''

def desenhar_input():
    screen.fill(WHITE)

    label = font.render("Digite o tamanho da matriz:", True, BLACK)
    label_rect = label.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    screen.blit(label, label_rect)

    input_surface = font.render(user_text, True, BLACK)
    input_box = pygame.Rect(0, 0, 200, 50)
    input_box.center = (screen_width // 2, screen_height // 2)
    pygame.draw.rect(screen, GRAY, input_box, 2)
    screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

    pygame.display.flip()

# Loop principal
running = True
while running:
    if input_active:
        desenhar_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_text.isdigit():
                    tam = int(user_text)
                    iniciar_jogo()
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if event.unicode.isdigit():
                        user_text += event.unicode

    else:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                matriz_width = tam * cell_size
                matriz_height = tam * cell_size
                offset_x = (screen_width - matriz_width) // 2
                offset_y = (screen_height - matriz_height) // 2

                if offset_x <= mx < offset_x + matriz_width and offset_y <= my < offset_y + matriz_height:
                    col = (mx - offset_x) // cell_size
                    row = (my - offset_y) // cell_size
                    if 0 <= row < tam and 0 <= col < tam:
                        if (row, col) in bombs:
                            # Reiniciar jogo se clicou em bomba
                            iniciar_jogo()
                        else:
                            if bomb_count[row][col] == 0:
                                revelar_area_vazia(row, col)
                            else:
                                reveal[row][col] = True

        matriz_width = tam * cell_size
        matriz_height = tam * cell_size
        offset_x = (screen_width - matriz_width) // 2
        offset_y = (screen_height - matriz_height) // 2

        for i in range(tam):
            for j in range(tam):
                rect = pygame.Rect(offset_x + j * cell_size, offset_y + i * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 2)

                if reveal[i][j]:
                    if (i, j) in bombs:
                        pygame.draw.rect(screen, RED, rect)
                        bomb_text = font.render("💣", True, BLACK)
                        screen.blit(bomb_text, (rect.x + 5, rect.y + 5))
                    else:
                        pygame.draw.rect(screen, WHITE, rect)
                        count = bomb_count[i][j]
                        if count > 0:
                            count_text = font.render(str(count), True, BLUE)
                            screen.blit(count_text, (rect.x + 10, rect.y + 5))
                else:
                    pygame.draw.rect(screen, GRAY, rect)

        pygame.display.flip()
        clock.tick(30)

pygame.quit()
sys.exit()
