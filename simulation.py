from graphics import *
import math


class Grid:
    def __init__(self, width, height, nodeSize, nodeGap, window):
        self.opened = []
        self.closed = []
        self.width = width
        self.height = height
        self.nodeSize = nodeSize
        self.nodeGap = nodeGap
        self.window = window
        self.nodes = []

        self.start = (14, 8)
        self.end = (17, 8)
        self.blocks = [(15, 6), (15, 7), (15, 8), (15, 9), (15, 10)]

    def draw(self):
        for i in range(self.width):
            row = []
            for j in range(self.height):
                x = (i*self.nodeSize)+((i+1)*self.nodeGap)
                y = (j*self.nodeSize)+((j+1)*self.nodeGap)

                # color start/end/obstacle blocks differently
                if (i+1, j+1) == self.start:
                    color = "red"
                elif (i+1, j+1) == self.end:
                    color = "green"
                elif (i+1, j+1) in self.blocks:
                    color = "black"
                else:
                    color = "white"

                node = Node(x, y, self.nodeSize, self.window, color, i, j)
                row.append(node)
                node.draw()

            self.nodes.append(row)

    def findPath(self):
        startNode = self.nodes[self.start[0]-1][self.start[1]-1]
        endNode = self.nodes[self.end[0]-1][self.end[1]-1]

        # add the start node to the opened list so the loop can start
        self.opened.append(startNode)

        # set the gScore of the start node to 0 because it is 0 units away from start
        startNode.setGScore(0)

        # fScore = gScore + hCost but gScore = 0 for first node therefore fScore = hCost = distance from start to end
        startNode.setFScore(self.getDistance(startNode, endNode))

        while self.opened:
            # current is an opened node with the lowest fScore
            current = self.opened[0]
            for node in self.opened:
                if node.fScore < current.fScore:
                    current = node

            if current == endNode:
                # found the path - display the path
                self.reconstructPath(endNode)

            self.opened.remove(current)
            self.closed.append(current)

            self.getNeighbours(current)


    def getDistance(self, node, endNode):
        """Gets the distance from the node to the end node - hCost in this case"""
        xDistance = node.row - endNode.row
        yDistance = node.column = endNode.column
        hCost = math.sqrt((xDistance**2) + (yDistance**2))

        return(hCost)


    def getNeighbours(self, node):
        
        neighbours = []
        row = node.row
        column = node.column
        adjacentCoordinates = [(row-1, column-1), (row-1, column), (row-1, column+1), (row, column-1), (row, column+1), (row+1, column - 1), (row+1, column), (row+1, column+1)]

        for coord in adjacentCoordinates:
            if (coord[0]+1, coord[1]+1) not in self.blocks and coord[0] >= 0 and coord[0] <= self.height-1 and coord[1] >= 0 and coord[1] <= self.width-1:
                # valid node
                print(coord)
                neighbours.append(self.nodes[coord[0]][coord[1]])

        print(neighbours)
        return(neighbours)


    def reconstructPath(self, endNode):
        pass

class Node:
    def __init__(self, x, y, size, window, color, row, column):
        self.x = x
        self.y = y
        self.size = size
        self.window = window
        self.color = color
        self.row = row
        self.column = column

        self.parent = None
        self.fScore = None
        self.gScore = None

    def draw(self):
        node = Rectangle(Point(self.x, self.y), Point(self.x + self.size, self.y + self.size))
        node.setFill(self.color)
        node.setOutline(self.color)
        node.draw(self.window)
        self.window.flush()

    def setFScore(self, fScore):
        self.fScore = fScore

    def setGScore(self, gScore):
        self.gScore = gScore


def main():
    # size in terms of # of nodes
    gridWidth = 30
    gridHeight = 15
    # size of each node in pixels
    nodeSize = 30
    # gap between each node in pixels
    gap = 2

    # subtracting 5px just makes it look nicer
    screenWidth = (gridWidth * nodeSize) + ((gridWidth + 1) * gap) - 5
    screenHeight = (gridHeight * nodeSize) + ((gridHeight + 1) * gap) - 5

    # create window
    window = GraphWin("A* Simulation", screenWidth, screenHeight, autoflush=False)
    window.setBackground("#D3D3D3")
    window.flush()

    grid = Grid(gridWidth, gridHeight, nodeSize, gap, window)
    grid.draw()
    grid.findPath()

    # prevents the program from exiting
    while True:
        mousePoint = window.checkMouse()
main()
