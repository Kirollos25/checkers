import pygame
import sys
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED, BLACK, GREY, PLAYER1_COLOR, PLAYER2_COLOR
from checkers.game import Game

pygame.init()
pygame.font.init()

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def draw_menu():
    background = pygame.image.load('checkers/assets/background.png').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    transparency = 128 
    
    WIN.blit(background, (0, 0))
    
    try:
        font = pygame.font.SysFont('arial', 50)
        small_font = pygame.font.SysFont('arial', 35)  
    except:
        font = pygame.font.Font(None, 50)
        small_font = pygame.font.Font(None, 35) 
        
    title = font.render('Welcome to Checkers! ', True, WHITE)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    developed_by = small_font.render('Developed by BFCAI team', True, WHITE)
    WIN.blit(developed_by, (WIDTH//2 - developed_by.get_width()//2, 160))
    
    button_color = (70, 70, 200) 
    pygame.draw.rect(WIN, button_color, (WIDTH//4, 300, WIDTH//2, 50), border_radius=10)
    pygame.draw.rect(WIN, WHITE, (WIDTH//4, 400, WIDTH//2, 50), border_radius=10)
    pygame.draw.rect(WIN, (200, 70, 70), (WIDTH//4, 500, WIDTH//2, 50), border_radius=10)
    
    btn_font = pygame.font.SysFont('arial', 30)
    player_vs_ai = btn_font.render('Play vs AI', True, WHITE)
    player_vs_player = btn_font.render('2 Players', True, BLACK)
    quit_text = btn_font.render('Quit', True, WHITE)
    
    WIN.blit(player_vs_ai, (WIDTH//2 - player_vs_ai.get_width()//2, 310))
    WIN.blit(player_vs_player, (WIDTH//2 - player_vs_player.get_width()//2, 410))
    WIN.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 510))
    
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    game = None
    menu = True
    
    while run:
        clock.tick(FPS)
        
        if menu:
            draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if WIDTH//4 <= pos[0] <= WIDTH//4 + WIDTH//2:
                        if 300 <= pos[1] <= 350: 
                            game = Game(WIN, ai_game=True)
                            menu = False
                        elif 400 <= pos[1] <= 450:  
                            game = Game(WIN, ai_game=False)
                            menu = False
                        elif 500 <= pos[1] <= 550: 
                            run = False
        else:
            if not game.update(): 
                menu = True
                game = None
                continue

            if game.ai_game and game.turn == PLAYER2_COLOR:
                game.ai_move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)
    
    pygame.quit()

if __name__ == "__main__":
    main()