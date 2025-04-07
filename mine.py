import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
CELL_SIZE = 30
MARGIN = 50
FONT = pygame.font.SysFont('Arial', 20)
TITLE_FONT = pygame.font.SysFont('Arial', 40)
BUTTON_FONT = pygame.font.SysFont('Arial', 24)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = BUTTON_FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Minesweeper:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Minesweeper')
        
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.field_size = 10
        self.num_bombs = 10
        self.board = []
        self.revealed = []
        self.flagged = []
        
        # Menu buttons
        button_width = 200
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        
        self.new_game_button = Button(button_x, 200, button_width, button_height, "Novo jogo")
        self.how_to_play_button = Button(button_x, 280, button_width, button_height, "Como jogar")
        self.credits_button = Button(button_x, 360, button_width, button_height, "Créditos")
        self.back_button = Button(button_x, 500, button_width, button_height, "Voltar")
        
        # Game setup buttons
        self.small_field_button = Button(button_x, 200, button_width, button_height, "Pequeno (8x8)")
        self.medium_field_button = Button(button_x, 280, button_width, button_height, "Médio (12x12)")
        self.large_field_button = Button(button_x, 360, button_width, button_height, "Grande (16x16)")
        
        self.few_bombs_button = Button(button_x, 200, button_width, button_height, "Poucas (10%)")
        self.medium_bombs_button = Button(button_x, 280, button_width, button_height, "Médias (15%)")
        self.many_bombs_button = Button(button_x, 360, button_width, button_height, "Muitas (20%)")
        
        self.yes_button = Button(self.screen_width // 3 - 75, 350, 150, 50, "Sim")
        self.no_button = Button(2 * self.screen_width // 3 - 75, 350, 150, 50, "Não")
        
    def create_board(self):
        # Create empty board
        self.board = [[0 for _ in range(self.field_size)] for _ in range(self.field_size)]
        self.revealed = [[False for _ in range(self.field_size)] for _ in range(self.field_size)]
        self.flagged = [[False for _ in range(self.field_size)] for _ in range(self.field_size)]
        
        # Place bombs
        bombs_placed = 0
        while bombs_placed < self.num_bombs:
            x = random.randint(0, self.field_size - 1)
            y = random.randint(0, self.field_size - 1)
            if self.board[y][x] != -1:  # -1 represents a bomb
                self.board[y][x] = -1
                bombs_placed += 1
                
        # Calculate numbers
        for y in range(self.field_size):
            for x in range(self.field_size):
                if self.board[y][x] == -1:
                    continue
                
                # Count adjacent bombs
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.field_size and 0 <= ny < self.field_size:
                            if self.board[ny][nx] == -1:
                                count += 1
                
                self.board[y][x] = count
    
    def draw_board(self):
        board_width = self.field_size * CELL_SIZE
        board_height = self.field_size * CELL_SIZE
        
        # Center the board
        board_x = (self.screen_width - board_width) // 2
        board_y = (self.screen_height - board_height) // 2
        
        for y in range(self.field_size):
            for x in range(self.field_size):
                rect = pygame.Rect(board_x + x * CELL_SIZE, board_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if self.revealed[y][x]:
                    pygame.draw.rect(self.screen, WHITE, rect)
                    if self.board[y][x] == -1:
                        # Draw bomb
                        pygame.draw.circle(self.screen, BLACK, rect.center, CELL_SIZE // 3)
                    elif self.board[y][x] > 0:
                        # Draw number
                        text = FONT.render(str(self.board[y][x]), True, BLUE)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect)
                    if self.flagged[y][x]:
                        # Draw flag
                        pygame.draw.polygon(self.screen, RED, [
                            (rect.centerx - CELL_SIZE // 4, rect.centery - CELL_SIZE // 4),
                            (rect.centerx + CELL_SIZE // 4, rect.centery),
                            (rect.centerx - CELL_SIZE // 4, rect.centery + CELL_SIZE // 4)
                        ])
                
                pygame.draw.rect(self.screen, BLACK, rect, 1)
    
    def handle_click(self, pos, right_click=False):
        board_width = self.field_size * CELL_SIZE
        board_height = self.field_size * CELL_SIZE
        
        board_x = (self.screen_width - board_width) // 2
        board_y = (self.screen_height - board_height) // 2
        
        if (board_x <= pos[0] <= board_x + board_width and 
            board_y <= pos[1] <= board_y + board_height):
            
            cell_x = (pos[0] - board_x) // CELL_SIZE
            cell_y = (pos[1] - board_y) // CELL_SIZE
            
            if right_click:
                # Toggle flag
                if not self.revealed[cell_y][cell_x]:
                    self.flagged[cell_y][cell_x] = not self.flagged[cell_y][cell_x]
            else:
                # Reveal cell
                if not self.flagged[cell_y][cell_x] and not self.revealed[cell_y][cell_x]:
                    self.revealed[cell_y][cell_x] = True
                    
                    if self.board[cell_y][cell_x] == -1:
                        # Game over
                        self.reveal_all_bombs()
                        self.state = "game_over"
                    
                    # Check for win
                    if self.check_win():
                        self.state = "win"
    
    def reveal_all_bombs(self):
        for y in range(self.field_size):
            for x in range(self.field_size):
                if self.board[y][x] == -1:
                    self.revealed[y][x] = True
    
    def check_win(self):
        for y in range(self.field_size):
            for x in range(self.field_size):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        title = TITLE_FONT.render("Campo Minado", True, BLACK)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        self.new_game_button.draw(self.screen)
        self.how_to_play_button.draw(self.screen)
        self.credits_button.draw(self.screen)
    
    def draw_how_to_play(self):
        self.screen.fill(WHITE)
        
        title = TITLE_FONT.render("Como Jogar", True, BLACK)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        instructions = [
            "1. Clique em uma célula para revelá-la.",
            "2. Clique com o botão direito para marcar uma bomba.",
            "3. Os números indicam quantas bombas estão adjacentes.",
            "4. Evite clicar nas bombas!",
            "5. Revele todas as células sem bombas para vencer."
        ]
        
        for i, line in enumerate(instructions):
            text = FONT.render(line, True, BLACK)
            text_rect = text.get_rect(center=(self.screen_width // 2, 180 + i * 40))
            self.screen.blit(text, text_rect)
        
        self.back_button.draw(self.screen)
    
    def draw_credits(self):
        self.screen.fill(WHITE)
        
        title = TITLE_FONT.render("Créditos", True, BLACK)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        credits_text = [
            "Desenvolvido por: Seu Nome",
            "Usando Python e Pygame",
            "Versão 1.0"
        ]
        
        for i, line in enumerate(credits_text):
            text = FONT.render(line, True, BLACK)
            text_rect = text.get_rect(center=(self.screen_width // 2, 200 + i * 40))
            self.screen.blit(text, text_rect)
        
        self.back_button.draw(self.screen)
    
    def draw_field_size_selection(self):
        self.screen.fill(WHITE)
        
        title = TITLE_FONT.render("Selecione o tamanho do campo", True, BLACK)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        self.small_field_button.draw(self.screen)
        self.medium_field_button.draw(self.screen)
        self.large_field_button.draw(self.screen)
        self.back_button.draw(self.screen)
    
    def draw_bomb_selection(self):
        self.screen.fill(WHITE)
        
        title = TITLE_FONT.render("Selecione a quantidade de bombas", True, BLACK)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        self.few_bombs_button.draw(self.screen)
        self.medium_bombs_button.draw(self.screen)
        self.many_bombs_button.draw(self.screen)
        self.back_button.draw(self.screen)
    
    def draw_game_over(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        message = TITLE_FONT.render("Game Over!", True, RED)
        message_rect = message.get_rect(center=(self.screen_width // 2, 200))
        self.screen.blit(message, message_rect)
        
        question = FONT.render("Deseja jogar novamente?", True, WHITE)
        question_rect = question.get_rect(center=(self.screen_width // 2, 280))
        self.screen.blit(question, question_rect)
        
        self.yes_button.draw(self.screen)
        self.no_button.draw(self.screen)
    
    def draw_win(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        message = TITLE_FONT.render("Você Venceu!", True, GREEN)
        message_rect = message.get_rect(center=(self.screen_width // 2, 200))
        self.screen.blit(message, message_rect)
        
        question = FONT.render("Deseja jogar novamente?", True, WHITE)
        question_rect = question.get_rect(center=(self.screen_width // 2, 280))
        self.screen.blit(question, question_rect)
        
        self.yes_button.draw(self.screen)
        self.no_button.draw(self.screen)
    
    def run(self):
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                if self.state == "menu":
                    self.new_game_button.check_hover(mouse_pos)
                    self.how_to_play_button.check_hover(mouse_pos)
                    self.credits_button.check_hover(mouse_pos)
                    
                    if self.new_game_button.is_clicked(mouse_pos, event):
                        self.state = "select_field_size"
                    elif self.how_to_play_button.is_clicked(mouse_pos, event):
                        self.state = "how_to_play"
                    elif self.credits_button.is_clicked(mouse_pos, event):
                        self.state = "credits"
                
                elif self.state == "how_to_play" or self.state == "credits":
                    self.back_button.check_hover(mouse_pos)
                    
                    if self.back_button.is_clicked(mouse_pos, event):
                        self.state = "menu"
                
                elif self.state == "select_field_size":
                    self.small_field_button.check_hover(mouse_pos)
                    self.medium_field_button.check_hover(mouse_pos)
                    self.large_field_button.check_hover(mouse_pos)
                    self.back_button.check_hover(mouse_pos)
                    
                    if self.small_field_button.is_clicked(mouse_pos, event):
                        self.field_size = 8
                        self.state = "select_bombs"
                    elif self.medium_field_button.is_clicked(mouse_pos, event):
                        self.field_size = 12
                        self.state = "select_bombs"
                    elif self.large_field_button.is_clicked(mouse_pos, event):
                        self.field_size = 16
                        self.state = "select_bombs"
                    elif self.back_button.is_clicked(mouse_pos, event):
                        self.state = "menu"
                
                elif self.state == "select_bombs":
                    self.few_bombs_button.check_hover(mouse_pos)
                    self.medium_bombs_button.check_hover(mouse_pos)
                    self.many_bombs_button.check_hover(mouse_pos)
                    self.back_button.check_hover(mouse_pos)
                    
                    if self.few_bombs_button.is_clicked(mouse_pos, event):
                        self.num_bombs = int(self.field_size * self.field_size * 0.1)
                        self.create_board()
                        self.state = "game"
                    elif self.medium_bombs_button.is_clicked(mouse_pos, event):
                        self.num_bombs = int(self.field_size * self.field_size * 0.15)
                        self.create_board()
                        self.state = "game"
                    elif self.many_bombs_button.is_clicked(mouse_pos, event):
                        self.num_bombs = int(self.field_size * self.field_size * 0.2)
                        self.create_board()
                        self.state = "game"
                    elif self.back_button.is_clicked(mouse_pos, event):
                        self.state = "select_field_size"
                
                elif self.state == "game":
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            self.handle_click(mouse_pos)
                        elif event.button == 3:  # Right click
                            self.handle_click(mouse_pos, right_click=True)
                
                elif self.state == "game_over" or self.state == "win":
                    self.yes_button.check_hover(mouse_pos)
                    self.no_button.check_hover(mouse_pos)
                    
                    if self.yes_button.is_clicked(mouse_pos, event):
                        self.state = "menu"
                    elif self.no_button.is_clicked(mouse_pos, event):
                        running = False
            
            # Draw the current state
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "how_to_play":
                self.draw_how_to_play()
            elif self.state == "credits":
                self.draw_credits()
            elif self.state == "select_field_size":
                self.draw_field_size_selection()
            elif self.state == "select_bombs":
                self.draw_bomb_selection()
            elif self.state == "game":
                self.screen.fill(WHITE)
                self.draw_board()
            
            if self.state == "game_over":
                self.draw_board()
                self.draw_game_over()
            elif self.state == "win":
                self.draw_board()
                self.draw_win()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Minesweeper()
    game.run()