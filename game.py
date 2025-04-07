import pygame
from components import button

import cv2

pygame.init()

# CONFIGURAÇÕES GLOBAIS
running = True
pygame.display.set_caption("Campo minado")  # Título da janela
clock = pygame.time.Clock() # FPS
bg_sobre = pygame.image.load("images/wallpaper.jpg")

tela = "menu"

# CONFIGURAÇÕES DA JANELA
width, height = 950, 600
screen = pygame.display.set_mode((width, height))

# CARREGAR O VÍDEO
video_de_fundo = "videos/stock_wallpaper.mp4"  # Substitua pelo caminho do seu vídeo
captura_do_video = cv2.VideoCapture(video_de_fundo)

# ==================== BOTÕES ====================
botao_jogar = pygame.image.load("images/buttons/botao_jogar.png").convert_alpha()
botao_como_jogar = pygame.image.load("images/buttons/botao_como_jogar.png").convert_alpha()
botao_voltar = pygame.image.load("images/buttons/botao_voltar.png").convert_alpha()
botao_sair = pygame.image.load("images/buttons/botao_sair.png").convert_alpha()

# => config dos botões
scale = 0.12

start_button = button.Button(width // 2.5, height // 4, botao_jogar, scale)
about_button = button.Button(width // 2.5, height // 4 + 50, botao_como_jogar, scale)
exit_button = button.Button(width // 2.5, height // 4 + 100, botao_sair, scale)
back_button = button.Button(width // 60, height // 4 + -140, botao_voltar, scale - 0.02)

# FUNÇÕES DO JOGO
# def play():
#    while True:

while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
   
   # Menu de Opcões
   if tela == "menu":
      if start_button.is_clicked(event):
         tela = "jogo"
      elif about_button.is_clicked(event):
         tela = "sobre"
      elif exit_button.is_clicked(event):
         running = False
   if back_button.is_clicked(event):
         tela = "menu"
   
   if tela == "menu":
      # ==================== MENU ====================
      video, frame = captura_do_video.read()
      
      if not video:
         captura_do_video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia o vídeo se acabar
         continue

      frame = cv2.resize(frame, (width, height)) # Faz o vídeo ocupar toda a tela
      frame = cv2.GaussianBlur(frame, (25, 25), 0) # Aplica o blur no vídeo 
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Coloca o vídeo com as cores padrões? não sei porque ele muda

      # Converte o vídeo de cv2 para o pygame
      frame_surface = pygame.surfarray.make_surface(frame) # Joga o vídeo para o fundo
      frame_surface = pygame.transform.rotate(frame_surface, -90) # Deixa o vídeo reto

      # Desenha o vídeo na tela
      screen.blit(frame_surface, (0, 0))

      # Desenha os botões na tela
      start_button.draw()
      about_button.draw()
      exit_button.draw()
      # ==================== FIM MENU ====================
         
   elif tela == "jogo":
      screen.fill((0, 0, 0))
      back_button.draw()
   
   elif tela == "sobre":
      screen.fill((0, 0, 0))
      font = pygame.font.Font(None, 36)
      
      screen.blit(bg_sobre, (-150, -150))
      back_button.draw()
      
      # ===================== SOBRE ====================
      text = font.render("Sobre o jogo", True, (255, 255, 255))
      text_1 = font.render("1 - Clique em um quadrado para revelar o número de minas ao redor.", True, (255, 255, 255))
      text_2 = font.render("2 - Evite clicar em quadrados com minas.", True, (255, 255, 255))
      text_3 = font.render("3 - Use os números para deduzir onde estão as minas.", True, (255, 255, 255))
      text_4 = font.render("4 - Revele todos os quadrados sem minas para vencer.", True, (255, 255, 255))
      screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2 - 200))
      screen.blit(text_1, (width // 2 - text_1.get_width() // 2, height // 2 - text_1.get_height() // 2 - 150))
      screen.blit(text_2, (width // 2 - text_2.get_width() // 2, height // 2 - text_2.get_height() // 2 - 100))
      screen.blit(text_3, (width // 2 - text_3.get_width() // 2, height // 2 - text_3.get_height() // 2 - 50))
      screen.blit(text_4, (width // 2 - text_4.get_width() // 2, height // 2 - text_4.get_height() // 2))
      
      # ===================== CRÉDITOS ====================
      text_creditos = font.render("Feito Por: ", True, (255, 255, 255))
      text_Angelo = font.render("- Angelo Miguel Requenha", True, (255, 255, 255))
      text_Dinae = font.render("- Dinaê Pfiffer", True, (255, 255, 255))
      text_Bruno = font.render("- Bruno de Queiróz", True, (255, 255, 255))
      screen.blit(text_creditos, (width // 2 - text_creditos.get_width() // 2, height // 2 - text_creditos.get_height() // 2 + 60))
      screen.blit(text_Angelo, (width // 2 - text_Angelo.get_width() // 2, height // 2 - text_Angelo.get_height() // 2 + 100))
      screen.blit(text_Dinae, (width // 2 - text_Dinae.get_width() // 2, height // 2 - text_Dinae.get_height() // 2 + 140))
      screen.blit(text_Bruno, (width // 2 - text_Bruno.get_width() // 2, height // 2 - text_Bruno.get_height() // 2 + 180))
      
   pygame.display.update() # Atualiza o jogo, sem isso, o jogo não roda...
   clock.tick(30) # FPS do jogo

pygame.quit()
