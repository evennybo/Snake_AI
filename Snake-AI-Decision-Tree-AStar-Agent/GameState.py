import random
from DecisionTreeAgent import DecisionTreeAgent
from AStarAgent import AStarAgent
from copy import deepcopy

class GameState:
    def __init__(self, board):
        self.snake = {"body" : [(board[0] // 2, board[1] // 2)], "direction" : random.choice([0, 1, 2, 3])}
        self.fruit = (random.randrange(1, board[0]-1, 1), random.randrange(1, board[1]-1, 1))
        self.board = board
        self.score = 0

        # agent stats
        self.agent = AStarAgent(self)
        self.back_up_agent = DecisionTreeAgent(self)

        # score stats
        self.total_score = 0
        self.best_score = 0
        
        # death stats
        self.deaths = 0
        
        # average steps to fruit
        self.total_steps = 0
        
        # expiry stats
        self.expires = 0
        self.time_since_last_fruit = 0

# ====================================Setters and Getters====================================
    def getBoard(self):
        return self.board

    def getSnake(self):
        return self.snake

    def getSnakeData(self):
        return str(self.snake)

    def getFruit(self):
        return self.fruit
        
    def getScore(self):
        return self.score

    def getDistanceToFruit(self):
        # Manhattan Distance
        return abs(self.fruit[0] - self.snake["body"][0][0]) + abs(self.fruit[1] - self.snake["body"][0][1])

    def getAgentStats(self):
        score = self.score
        best_score = self.best_score
        deaths = self.deaths
        average_steps = self.total_steps / self.total_score if self.total_score != 0 else self.total_steps
        expires = self.expires

        return score, best_score, average_steps, deaths, expires

# ==========================================Checkers==========================================
    def checkIfFruitEaten(self):
        if self.snake["body"][0] == self.fruit:
            return True
        return False

    def checkIfSnakeHitItself(self):
        if self.snake["body"][0] in self.snake["body"][1:]:
            return True
        return False

    def checkIfSnakeHitBorder(self):
        if self.snake["body"][0][0] < 0 or self.snake["body"][0][0] >= self.board[0] or self.snake["body"][0][1] < 0 or self.snake["body"][0][1] >= self.board[1]:
            return True
        return False
        
    def checkIfGameEnded(self):
        if self.checkIfSnakeHitBorder() or self.checkIfSnakeHitItself():
            print("Game ended")
            return True
        return False

# =========================================SNAKE Movement Functions========================================     
        
    def move(self, input):
        # Moving the snake based on the input
        # [0, 0, 1] -> move right for 1 block
        # [0, 1, 0] -> go straight for 1 block
        # [1, 0, 0] -> move left for 1 block

        if input[0]:
            self.snake["direction"] = (self.snake["direction"] - 1) % 4
        elif input[2]:
            self.snake["direction"] = (self.snake["direction"] + 1) % 4
        
        head = self.snake["body"][0]
        if self.snake["direction"] == 0:
            self.snake["body"].insert(0, (head[0] + 1, head[1]))
        elif self.snake["direction"] == 1:
            self.snake["body"].insert(0, (head[0], head[1] + 1))
        elif self.snake["direction"] == 2:
            self.snake["body"].insert(0, (head[0] - 1, head[1]))
        elif self.snake["direction"] == 3:
            self.snake["body"].insert(0, (head[0], head[1] - 1))
            
        self.snake["body"].pop()

    def moveTo(self, coordinates):
        self.snake["body"].insert(0, coordinates)
        self.snake["body"].pop()

    def grow(self):
        tail = self.snake["body"][-1]
        if len(self.snake["body"]) > 1:
            second_last = self.snake["body"][-2]
            if tail[0] == second_last[0]:
                if tail[1] > second_last[1]:
                    self.snake["body"].append((tail[0], tail[1] + 1))
                else:
                    self.snake["body"].append((tail[0], tail[1] - 1))
            else:
                if tail[0] > second_last[0]:
                    self.snake["body"].append((tail[0] + 1, tail[1]))
                else:
                    self.snake["body"].append((tail[0] - 1, tail[1]))
        else:
            if self.snake["direction"] == 0:
                self.snake["body"].append((tail[0] + 1, tail[1]))
            elif self.snake["direction"] == 1:
                self.snake["body"].append((tail[0], tail[1] + 1))
            elif self.snake["direction"] == 2:
                self.snake["body"].append((tail[0] - 1, tail[1]))
            elif self.snake["direction"] == 3:
                self.snake["body"].append((tail[0], tail[1] - 1))  

# ====================================Playing Game====================================
    def respawnFruit(self):
        self.fruit = (random.randrange(1, self.board[0]-1, 1), random.randrange(1, self.board[1]-1, 1))
        if self.fruit in self.snake["body"]:
            self.respawnFruit()

    def reset(self):
        self.snake = {"body" : [(self.board[0] // 2, self.board[1] // 2)], "direction" : random.choice([0, 1, 2, 3])}
        self.fruit = (random.randrange(1, self.board[0]-1, 1), random.randrange(1, self.board[1]-1, 1))
        self.score = 0
        self.time_since_last_fruit = 0

    def play(self):
            move = self.agent.getNextLocation()
            if move == None:
                move = self.back_up_agent.getMove()
                self.move(move)
            else:
                self.moveTo(move)

            self.time_since_last_fruit += 1
            self.total_steps += 1

            if self.checkIfFruitEaten():
                self.score += 1
                self.total_score += 1
                self.time_since_last_fruit = 0
                if self.score > self.best_score:
                    self.best_score = self.score

                self.grow()
                self.respawnFruit()
            
            if self.checkIfGameEnded():
                self.deaths += 1
                self.reset()
                return
            
            if self.time_since_last_fruit > self.board[0] * self.board[1]:
                self.expires += 1
                self.reset()
                return


    # Used to get potential states of the game for recursive operations by the agent
    def gamestateAfterMove(self, move):
        resultant_gamestate = deepcopy(self)
        resultant_gamestate.move(move)
        return resultant_gamestate

    def getOccupiedSpace(self):
        head = self.snake["body"][0]
        tail = self.snake["body"][-1]
        occupied_space = abs(head[0] - tail[0]) * abs(head[1] - tail[1])

        return occupied_space

        