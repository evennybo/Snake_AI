from typing import List, Tuple
import pygame
from GameState import GameState

class Renderer:
    def __init__(self, game: GameState, block_size: int = 10, speed: int = 15):
        self.block_size = block_size
        self.game = game
        self.clock = pygame.time.Clock()
        self.speed = speed

        # initialize colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (128, 128, 128)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)

        pygame.init()
        self.score_font = pygame.font.SysFont("arial", self.block_size)
        self.screen = pygame.display.set_mode((game.getBoard()[0]*block_size, game.getBoard()[1]*block_size))
        pygame.display.set_caption("Snaeke")

    def renderSnakes(self, snakebody: List[Tuple[int, int]]):
       for pair in snakebody:
            pygame.draw.rect(self.screen, self.red, [pair[0]*self.block_size, pair[1]*self.block_size, self.block_size, self.block_size])

    def renderFruit(self, coordinates: Tuple[int, int]):
        pygame.draw.rect(self.screen, self.green, [coordinates[0]*self.block_size, coordinates[1]*self.block_size, self.block_size, self.block_size])

    def renderAgentStats(self, stats):
        score = self.score_font.render("Score - " + str(stats[0]), True, self.white)
        best_score = self.score_font.render("Best Score - " + str(stats[1]), True, self.white)
        avg_steps = self.score_font.render("Avg Steps: - " + str(stats[2].__format__('.3f')), True, self.white)
        deaths = self.score_font.render("Deaths: - " + str(stats[3]), True, self.white)
        expirys = self.score_font.render("Expirys: - " + str(stats[4]), True, self.white)
        
        
        self.screen.blit(score, [0,0])
        self.screen.blit(best_score, [0,self.block_size])
        self.screen.blit(deaths, [0,self.block_size*2])
        self.screen.blit(avg_steps, [0,self.block_size*3])
        self.screen.blit(expirys, [0,self.block_size*4])
        
        pygame.display.update()

    def render(self):
        self.screen.fill(self.black)
        self.renderSnakes(self.game.getSnake()["body"])
        self.renderFruit(self.game.getFruit())
        self.renderAgentStats(self.game.getAgentStats())
        pygame.display.update()
        self.clock.tick(self.speed)

    def renderGameOver(self):
        scoreval = self.game.getScore()
        self.screen.fill(self.black)
        score = self.score_font.render("Game Over", True, self.white)
        self.screen.blit(score, [0,0])
        score = self.score_font.render("Score - " + str(scoreval), True, self.white)
        self.screen.blit(score, [0,30])
        pygame.display.update()

        # wait for 5 seconds
        pygame.time.wait(5000)