import pygame
from components import button

import cv2

pygame.init()

# CARREGAR O VÍDEO
video_de_fundo = "videos/stock_wallpaper.mp4"  # Substitua pelo caminho do seu vídeo
captura_do_video = cv2.VideoCapture(video_de_fundo)

# CONFIGURAÇÕES GLOBAIS
running = True
pygame.display.set_caption("Campo minado")  # Título da janela
clock = pygame.time.Clock()  # FPS

# CONFIGURAÇÕES DA JANELA
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# BOTÕES
start_button = pygame.image.load("images/buttons/start_button_01.png").convert_alpha()
options_button = pygame.image.load("images/buttons/options_button_02.png").convert_alpha()
about_button = pygame.image.load("images/buttons/about_button_03.png").convert_alpha()
exit_button = pygame.image.load("images/buttons/exit_button_04.png").convert_alpha()

# => config dos botões
scale = 0.1
exit_scale = 0.08 # Diferentão

start_button = button.Button(WIDTH // 2.5, HEIGHT // 4, start_button, scale)
options_button = button.Button(WIDTH // 2.5, HEIGHT // 4 + 50, options_button, scale)
about_button = button.Button(WIDTH // 2.5, HEIGHT // 4 + 100, about_button, scale)
exit_button = button.Button(WIDTH // 2.37, HEIGHT // 4 + 150, exit_button, exit_scale)

# FUNÇÕES DO JOGO

while running:

   # ==================== MENU ====================
   
   # Inicia o vídeo
   video, frame = captura_do_video.read()
    
   if not video:
      captura_do_video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia o vídeo se acabar
      continue

   # Faz o vídeo ocupar toda a tela
   frame = cv2.resize(frame, (WIDTH, HEIGHT))

   # Aplica o blur no vídeo                # ↓ Quantidade de desfoque
   frame = cv2.GaussianBlur(frame, (25, 25), 0)
   
   # Coloca o vídeo com as cores padrões? não sei porque ele muda
   frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

   # Converte o vídeo de cv2 para o pygame
   frame_surface = pygame.surfarray.make_surface(frame) # Joga o vídeo para o fundo
   frame_surface = pygame.transform.rotate(frame_surface, -90) # Deixa o vídeo reto

   # Desenha o vídeo na tela
   SCREEN.blit(frame_surface, (0, 0))

   # Desenha os botões na tela
   start_button.draw()
   options_button.draw()
   about_button.draw()
   exit_button.draw()
   
   # ==================== FIM MENU ====================

   # Eventos
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
         
   pygame.display.update() # Atualiza o jogo, sem isso, o jogo não roda...
   
   clock.tick(30) # FPS do jogo

captura_do_video.release()
pygame.quit()
