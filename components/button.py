import pygame

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

class Button():
   def __init__(self, x, y, image, scale):
      width = int(image.get_width() * scale)
      height = int(image.get_height() * scale)

      self.image = pygame.transform.scale(image, (width, height))
      self.rect = self.image.get_rect(midtop=(WIDTH // 2, HEIGHT))
      self.rect.topleft = (x, y)
   
   def draw(self):
      # Desenha o botão na tela
      SCREEN.blit(self.image, self.rect.topleft)