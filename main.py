from World import World
import time
from wumpus_gui import *

def main (wrld_file = None ):
    
    world = World(True, file= wrld_file)
    score = world.run(screen)
    print ("Your agent scored: " + str(score))
    show_msg_up('Game Over', screen)
    show_msg_down('score: '+str(score), screen)
    time.sleep(5)
    game()

screen = board_graphics_init()
pygame.display.set_caption('wumpus world')

def game():
    screen.fill((0, 0, 0))
    choice = main_menu(screen)
    if choice == 1:
        screen.fill((0, 0, 0))
        main()

    elif choice == 2:
        file = open('world/custom_world.txt', 'r')
        screen.fill((0, 0, 0))
        main(file)
    elif choice == 3:
        pygame.quit()

game()
