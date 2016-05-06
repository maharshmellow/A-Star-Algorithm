from graphics import *
import math
import time

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

        self.start = (7, 8)
        self.end = (17, 8)
        self.blocks = [(7, 7), (8, 7), (8, 9), (9, 7), (9, 9), (10, 7), (10, 9), (11, 7), (11, 9), (12, 7), (12, 9), (13, 7), (13, 9), (13, 8)]

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
        startTime = time.time()
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
                return(True)

            self.opened.remove(current)
            self.closed.append(current)

            for neighbour in self.getNeighbours(current):
                if neighbour in self.closed:
                    continue    # ignore it because it has already been evaluated

                # the distance from start to a neighbour
                tempGScore = current.gScore + self.getDistance(current, neighbour)
                if neighbour not in self.opened:    # discover a new node
                    self.opened.append(neighbour)
                elif tempGScore >= neighbour.gScore:
                    continue    # this is not a better path

                # this path is the best path until now
                neighbour.setParent(current)
                neighbour.setGScore(tempGScore)
                neighbour.setFScore(tempGScore + self.getDistance(neighbour, endNode)) # fScore = gScore + hCost


        return False    # failure to find a path


    def getDistance(self, node, endNode):
        """Gets the distance from the node to the end node - hCost in this case"""
        xDistance = node.column - endNode.column
        yDistance = node.row - endNode.row

        hCost = math.sqrt((xDistance**2) + (yDistance**2))

        return(hCost)


    def getNeighbours(self, node):

        neighbours = []
        row = node.row
        column = node.column
        adjacentCoordinates = [(row-1, column-1), (row-1, column), (row-1, column+1), (row, column-1), (row, column+1), (row+1, column - 1), (row+1, column), (row+1, column+1)]

        for coord in adjacentCoordinates:
            if (coord[0]+1, coord[1]+1) not in self.blocks and coord[0] >= 0 and coord[0] <= self.width-1 and coord[1] >= 0 and coord[1] <= self.height-1:
                # valid node
                neighbours.append(self.nodes[coord[0]][coord[1]])

        return(neighbours)


    def reconstructPath(self, endNode):
        current = endNode

        while current.getParent():
            current.changeColor("yellow")
            current = current.getParent()
        endNode.changeColor("green")




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
        self.fScore = math.inf
        self.gScore = math.inf

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

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return(self.parent)

    def changeColor(self, newColor):
        node = Rectangle(Point(self.x, self.y), Point(self.x + self.size, self.y + self.size))
        node.setFill(newColor)
        node.setOutline(newColor)
        node.draw(self.window)
        self.window.flush()


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
    if grid.findPath():
        print("Path Successful")

    # prevents the program from exiting
    while True:
        mousePoint = window.checkMouse()
main()
