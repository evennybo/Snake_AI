import numpy as np

class DecisionTreeAgent:
    def __init__(self, gamestate, discount_factor: float = 0.99):
        self.discount_factor = discount_factor
        self.gamestate = gamestate
        self.possible_moves = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.previous_snake_states = set()

    def calculateMaxStateValue(self, gamestate) -> float:
        # Using the Bellman equation to calculate the value of a state
        # print(self.previous_snake_states)
        # If we have already calculated the value of this state, return nothing
        if self.previous_snake_states.__contains__(gamestate.getSnakeData()):
            del gamestate
            return 0
        else:
            # First 3 if statements are to check if the state is terminal
            if gamestate.checkIfSnakeHitItself():
                self.previous_snake_states.add(gamestate.getSnakeData())
                v = -10
                del gamestate
                return v
            elif gamestate.checkIfSnakeHitBorder():
                self.previous_snake_states.add(gamestate.getSnakeData())
                v = -10
                del gamestate
                return v
            else:
                # If the state is not terminal, calculate the value of the state recursively using the Bellman equation      
                self.previous_snake_states.add(gamestate.getSnakeData())
                current_value = 0
                potential_value = 0
                for move in self.possible_moves:
                    potential_value = max(potential_value, self.calculateMaxStateValue(self.gamestate.gamestateAfterMove(move)))
                v = current_value + self.discount_factor * potential_value
                del gamestate
                return v

    def getMove(self) -> int:
        # Get the move that will result in the highest value state
        move_values = []
        # print("\nHead: {}\t Fruit: {}".format(self.gamestate.getSnake().getHead(), self.gamestate.getFruit().getPos()))
        for move in self.possible_moves:
            # print("Calculating move value for move: {}".format(move))
            move_value = self.calculateMaxStateValue(self.gamestate.gamestateAfterMove(move))
            # print("Move value: {}".format(move_value))
            move_values.append(move_value)
            self.previous_snake_states.clear()
        best_move = [0, 0, 0]
        best_move[np.argmax(move_values)] = 1
        # print("Move values: {}\t Best move: {}".format(move_values, best_move))
        return best_move
            