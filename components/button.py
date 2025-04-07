import pygame

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

class Button():
   def __init__(self, x, y, image, scale):
      width = int(image.get_width() * scale)
      height = int(image.get_height() * scale)

      self.image = pygame.transform.scale(image, (width, height))
      self.rect = self.image.get_rect(midtop=(width // 2, height))
      self.rect.topleft = (x, y)
   
   def draw(self):
      screen.blit(self.image, self.rect.topleft) # Desenha o botão na tela
      
   def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # botão esquerdo
            if self.rect.collidepoint(event.pos):
                return True
        return False