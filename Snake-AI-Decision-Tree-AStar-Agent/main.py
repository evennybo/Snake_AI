import pygame
from GameState import GameState
from Renderer import Renderer
import sys
sys.setrecursionlimit(10000)



def main():
    
    BOARD_WIDTH = 60
    BOARD_HEIGHT = 50
    BLOCK_SIZE = 10
    SPEED = 5000000

    gamestate = GameState((BOARD_WIDTH, BOARD_HEIGHT))
    renderer = Renderer(gamestate, BLOCK_SIZE, SPEED)

    game_over = False

    renderer.render()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    gamestate.grow()
        
        gamestate.play()
        renderer.render()


                

if __name__ == "__main__":
    main()
