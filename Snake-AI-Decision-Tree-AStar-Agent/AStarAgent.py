class AStarAgent:
    def __init__(self, gamestate):
        self.path = []
        self.gamestate = gamestate
        self.board = gamestate.getBoard()
        self.snake_body = None
        self.fruit = None


    def reconstructPath(self, cameFrom, current):
        totalPath = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            totalPath.append(current)
        return totalPath

    def getNeighbors(self, node):
        neighbors = []
        if node[0] > 0:
            neighbor = (node[0] - 1, node[1])
            if neighbor not in self.snake_body:
                neighbors.append(neighbor)
        if node[0] < self.board[0] - 1:
            neighbor = (node[0] + 1, node[1])
            if neighbor not in self.snake_body:
                neighbors.append(neighbor)
        if node[1] > 0:
            neighbor = (node[0], node[1] - 1)
            if neighbor not in self.snake_body:
                neighbors.append(neighbor)
        if node[1] < self.board[1] - 1:
            neighbor = (node[0], node[1] + 1)
            if neighbor not in self.snake_body:
                neighbors.append(neighbor)

        return neighbors

    def heuristic(self, start, end):
        # Manhattan distance
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def dfs(self, start, end):
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node == end:
                return True
            if node not in visited:
                visited.add(node)
                stack.extend(self.getNeighbors(node))
        return False

    def path_exists(self, start, end):
        return self.dfs(start, end)

    def aStar(self, start, end):
        openSet = []
        closedSet = []
        cameFrom = {}

        gScore = {}
        gScore[start] = 0

        fScore = {}
        fScore[start] = self.heuristic(start, end)

        openSet.append(start)

        while len(openSet) > 0:
            current = openSet[0]
            for i in range(1, len(openSet)):
                if fScore[openSet[i]] < fScore[current]:
                    current = openSet[i]

            if current == end:
                return self.reconstructPath(cameFrom, current)

            openSet.remove(current)
            closedSet.append(current)

            for neighbor in self.getNeighbors(current):
                if neighbor in closedSet:
                    continue

                gScore_temp = gScore[current] + 1

                if neighbor not in openSet:
                    openSet.append(neighbor)
                elif gScore_temp >= gScore[neighbor]:
                    continue

                cameFrom[neighbor] = current
                gScore[neighbor] = gScore_temp
                fScore[neighbor] = gScore[neighbor] + self.heuristic(neighbor, end)

        return []

    def findPath(self):
        self.snake_body = self.gamestate.getSnake()["body"]
        self.fruit = self.gamestate.getFruit()
        start = self.snake_body[0]

        if self.path_exists(start, self.fruit):
            self.path = self.aStar(start, self.fruit)
            self.path.pop()
        else:
            self.path = [None]
            

    def getNextLocation(self):
        if len(self.path) == 0:
            self.findPath()
        
        return self.path.pop()
        