from xmlrpc.client import Boolean
import pygame
import sys

B_R, B_C = 10, 10
SQUARE_LEN = 60

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
DARKSEAGREEN = (143, 188, 143)
MEDIUMSEAGREEN = (0, 250, 154)

RADIUS = 0.45*SQUARE_LEN

IMAGES = {}
def load_image():
    pics = ["agent_down1", "agent_left1", "agent_right1", "agent_up1", "breeze", "gold", "bg", "bg1", "pit", "stench", "wumpus" , "dead_wumpus", "arrow_overlay"]
    for pic in pics:
        IMAGES[pic] = pygame.transform.scale(pygame.image.load(f"./icons/{pic}.png"), (SQUARE_LEN-1, SQUARE_LEN-1))
        
def board_graphics_init():
    pygame.init()
    board_width = B_R * SQUARE_LEN
    board_height = (B_C+2) * SQUARE_LEN
    screen = pygame.display.set_mode((board_width, board_height))
    load_image()
    return screen

def show_msg_up(txt, screen, color=WHITE):
    pygame.draw.rect(screen, BLACK, (0, 0, B_C*SQUARE_LEN, 2*SQUARE_LEN))
    font = pygame.font.SysFont('Verdana', 50)
    text = font.render(txt, True, (color))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, SQUARE_LEN//2))
    screen.blit(text, text_rect)
    pygame.display.update()

def show_msg_down(txt, screen, color=WHITE):
    # pygame.draw.rect(screen, BLACK, (0, 0, B_C*SQUARE_LEN, 2*SQUARE_LEN))
    font = pygame.font.SysFont('Verdana', 40)
    text = font.render(txt, True, (color))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, SQUARE_LEN//2+SQUARE_LEN))
    screen.blit(text, text_rect)
    pygame.display.update()

def show_percept(tile, scream, screen):
    # print('percept', scream)
    pos = 0

    icon_size = (SQUARE_LEN-30, SQUARE_LEN-30)

    dead_wump_img = IMAGES['dead_wumpus']
    gold_img = IMAGES['gold']
    breeze_img = IMAGES['breeze']
    stench_img = IMAGES['stench']

    per = 0
    if tile.stench: per+=1
    if tile.breeze: per+=1
    if tile.gold:   per+=1
    # if scream: per+=1

    pos = -1*per//2
    if tile.stench: 
        pygame.draw.rect(screen, WHITE, (B_C*SQUARE_LEN//2+(35*pos), SQUARE_LEN//2+40, 30, 30))
        screen.blit(stench_img, (B_C*SQUARE_LEN//2+(35*pos), SQUARE_LEN//2+40))
        pos+=1
    if tile.breeze: 
        screen.blit(breeze_img, (B_C*SQUARE_LEN//2+(35*pos), SQUARE_LEN//2+40))
        pos+=1
    if tile.gold:   
        screen.blit(gold_img, (B_C*SQUARE_LEN//2+(35*pos), SQUARE_LEN//2+40))
        pos+=1
    if scream:
        screen.blit(dead_wump_img, (B_C*SQUARE_LEN//2+(35*pos), SQUARE_LEN//2+40))
        pos+=1

    pygame.display.update()



def refresh_graphics(board, dir, show_board, screen):
    # screen.fill((0, 0, 0))
    for c in range(B_C):
        board[c], board[B_C-c-1] = board[B_C-c-1], board[c]
    ''' Icons '''

    bg_img = IMAGES['bg']
    wump_img = IMAGES['wumpus']
    player_right = IMAGES['agent_right1']
    player_left = IMAGES['agent_left1']
    player_up = IMAGES['agent_up1']
    player_down = IMAGES['agent_down1']
    pit_img = IMAGES['pit']
    gold_img = IMAGES['gold']
    breeze_img = IMAGES['breeze']
    stench_img = IMAGES['stench']
    alt_bg_img = IMAGES['bg1']
    
    for col in range(B_C):
        for row in range(B_R):
            pos = (col*SQUARE_LEN, B_R*SQUARE_LEN - row*SQUARE_LEN+SQUARE_LEN)
            screen.blit(bg_img, pos)
            
            if board[col][row].agent:
                player_img = player_right
                if dir == 0:
                    player_img = player_right
                elif dir == 1:
                    player_img = player_down
                elif dir == 2:
                    player_img = player_left
                elif dir == 3:
                    player_img = player_up
                screen.blit(player_img, pos)
            if board[col][row].wumpus:
                screen.blit(wump_img, pos)
            if board[col][row].pit:
                screen.blit(pit_img, pos)
            if board[col][row].gold:
                screen.blit(gold_img, pos)
            if board[col][row].breeze:
                screen.blit(breeze_img, pos)
            if board[col][row].stench:
                screen.blit(stench_img, pos)
            
            if not board[col][row].visited and not show_board:
                screen.blit(alt_bg_img, pos)

                
    pygame.display.update()
    pass

def menu_gui(screen):
    # screen = board_graphics_init()
    font = pygame.font.Font(None, 80)
    text = font.render('New Game', True, (WHITE))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, B_R*SQUARE_LEN//3))
    screen.blit(text, text_rect)
    
    text = font.render('Custom Game', True, (WHITE))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, B_R*SQUARE_LEN//3+80))
    screen.blit(text, text_rect)

    text = font.render('Exit', True, (WHITE))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, B_R*SQUARE_LEN//3+160))
    screen.blit(text, text_rect)

    pygame.display.update()

def main_menu(screen):
    menu_gui(screen)
    # mouse = pygame.mouse.get_pos()
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # For events that occur upon clicking the mouse (left click) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                print(B_C*SQUARE_LEN, B_R*SQUARE_LEN)
                w_pad, h_pad = 100, 50
                if (B_C*SQUARE_LEN//2)-w_pad <= event.pos[0] <= (B_C*SQUARE_LEN//2)+w_pad and (B_R*SQUARE_LEN//3)-h_pad <= event.pos[1] <= (B_R*SQUARE_LEN//3)+h_pad:
                    return 1
                elif (B_C*SQUARE_LEN//2)-w_pad <= event.pos[0] <= (B_C*SQUARE_LEN//2)+w_pad and (B_R*SQUARE_LEN//3+80)-h_pad <= event.pos[1] <= (B_R*SQUARE_LEN//3+80)+h_pad:
                    return 2
                elif (B_C*SQUARE_LEN//2)-w_pad <= event.pos[0] <= (B_C*SQUARE_LEN//2)+w_pad and (B_R*SQUARE_LEN//3+160)-h_pad <= event.pos[1] <= (B_R*SQUARE_LEN//3+160)+h_pad:
                    return 3
