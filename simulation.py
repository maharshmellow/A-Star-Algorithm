from graphics import *



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

        self.start = (1, 1)
        self.goal = (5, 5)

    def draw(self):
        for i in range(self.width):
            row = []
            for j in range(self.height):
                x = (i*self.nodeSize)+((i+1)*self.nodeGap)
                y = (j*self.nodeSize)+((j+1)*self.nodeGap)
                color = "white"
                node = Node(x, y,self.nodeSize, self.window, color)
                row.append(node)
                node.draw()

            self.nodes.append(row)

class Node:
    def __init__(self, x, y, size, window, color):
        self.x = x
        self.y = y
        self.size = size
        self.window = window
        self.color = color
        self.parent = None

    def draw(self):
        node = Rectangle(Point(self.x, self.y), Point(self.x + self.size, self.y + self.size))
        node.setFill(self.color)
        node.setOutline(self.color)
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

    screenWidth = (gridWidth * nodeSize) + ((gridWidth + 1) * gap) - 5
    screenHeight = (gridHeight * nodeSize) + ((gridHeight + 1) * gap) - 5

    # create window
    window = GraphWin("A* Simulation", screenWidth, screenHeight, autoflush=False)
    window.setBackground("#D3D3D3")
    window.flush()

    grid = Grid(gridWidth, gridHeight, nodeSize, gap, window)
    grid.draw()

    # prevents the program from exiting
    while True:
        mousePoint = window.checkMouse()
main()
