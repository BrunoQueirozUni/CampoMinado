import pygame

pygame.init()

# Constants
running = True
pygame.display.set_caption("Campo minado") # Titulo da janela
clock = pygame.time.Clock() # FPS 
delta_time = 0.1 # Tempo entre os frames

# Janela Config
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Imagens              | importando de uma pasta |
roblox = pygame.image.load("images/image0.png").convert_alpha() #Converte a imagem para "png"

# Posição das Imagens
robloxImageX = 0;

while running:
   
   # Janela
   screen.fill((255, 255, 255)) # Limpa a tela
   
   robloxImageX += 50 * delta_time
   
   # Evento para sair do jogo sem crashar
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
   
   pygame.display.flip()
   
   delta_time = clock.tick(60) / 1000 # Atualiza o tempo entre os frames
   delta_time = max(0.001, min(0.1, delta_time)) # Limita o delta_time entre 0.001 e 0.1

pygame.quit()
