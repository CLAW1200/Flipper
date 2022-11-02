"""
FLIPPER
aka chasing the light
"""
import pygame
import random

class Game:
    def __init__(self, windowX, windowY):
        pygame.init() 
        pygame.display.set_caption("Flipper") 
        self.gridX = 1
        self.gridY = 1
        self.windowX = windowX
        self.windowY = windowY
        self.screen = pygame.display.set_mode((windowX, windowY))
        self.clock = pygame.time.Clock()
        self.running = True
        self.startingCellColor = (255,255,70)
        self.cellWinColor = (70,255,70)
        self.background = (25,25,25)
        self.cellColor = self.startingCellColor
        self.lineColor = (70,70,200)
        self.moveCount = 0
        self.run()

    def recordBestMoveCount(self):
        with open("bestMoves.txt", "a") as f:
            f.write(f"Record for level {self.gridX}: {self.moveCount} moves\n")


    def justWin(self):
        for x in range(self.gridX):
            for y in range(self.gridY):
                self.grid[x][y] = 1
        self.updateGrid()
        if self.checkWin():
            self.userWon()

    def checkWin(self):
        for x in range(self.gridX):
            for y in range(self.gridY):
                if self.grid[x][y] == 0:
                    return False
        return True

    def userWon(self):
        self.soundPlayer(f"Assets\\Audio\\win_level4.wav")
        #keep drawing grid until user presses a key
        self.cellColor = self.cellWinColor
        self.updateGrid()
        pygame.display.flip()
        #wait for user to press a key
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.recordBestMoveCount()
                    self.moveCount = 0
                    self.increaseGrid()
                    self.start()
                    return
                if event.type == pygame.QUIT:
                    self.running = False
                    return

    def soundPlayer(self, sound):
        try:
            pygame.mixer.Sound.play(pygame.mixer.Sound(sound))
        except:
            pass

    def increaseGrid(self):
        self.gridX += 1
        self.gridY += 1
        self.soundPlayer("Assets\\Audio\\click_up.wav")
        self.start()
    
    def decreaseGrid(self):
        if self.gridX < 2:
            pass
        else:
            self.gridX -= 1
            self.gridY -= 1
            self.soundPlayer("Assets\\Audio\\click_down.wav")
            self.start()


    def run(self):
        self.start()
        pygame.display.flip()
        while self.running:
            self.clock.tick(165)
            self.update()
            pygame.display.flip()

    def flip(self, x, y):
        #invert cells
        self.flipCellState(x, y)
        self.flipCellState(x+1, y)
        self.flipCellState(x-1, y)
        self.flipCellState(x, y+1)
        self.flipCellState(x, y-1)
        self.moveCount += 1
        
        if self.checkWin():
            self.userWon()
        else:
            self.soundPlayer("Assets\\Audio\\click.wav")
        

    def update(self):
        self.updateGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    x = int(mousePos[0]//(self.windowX/self.gridX))
                    y = int(mousePos[1]//(self.windowY/self.gridY))
                    self.flip(x, y)
                if event.button == 3:
                    self.invertGrid()
                if event.button == 4:
                    self.increaseGrid()
                if event.button == 5:
                    self.decreaseGrid()

    def invertGrid(self):
        for x in range(self.gridX):
            for y in range(self.gridY):
                self.flipCellState(x, y)
        self.moveCount += 1
        self.updateGrid()
        
        if self.checkWin():
            self.userWon()
        else:
            self.soundPlayer("Assets\\Audio\\flip.wav")
          
    def start(self):
        self.cellColor = self.startingCellColor
        self.createGrid(self.gridX, self.gridY)
        self.randomizeGrid()
        self.updateGrid()

    def createGrid(self, gridX, gridY):
        self.grid = []
        for x in range(gridX):
            self.grid.append([])
            for y in range(gridY):
                self.grid[x].append(0)

    def randomizeGrid(self):
        if self.gridX == 1:
            self.grid[0][0] = 0
        else:
            for x in range(self.gridX):
                for y in range(self.gridY):
                    self.grid[x][y] = random.randint(0,1)

    def updateGrid(self):
        self.screen.fill(self.background)
        for x in range(self.gridX):
            for y in range(self.gridY):
                if self.grid[x][y] == 1:
                    pygame.draw.rect(self.screen, self.cellColor, (x*self.windowX/self.gridX, y*self.windowY/self.gridY, self.windowX/self.gridX, self.windowY/self.gridY))

        self.lineThickness = (self.windowX)/100
        for x in range(self.gridX+1): #vertical lines 6px wide with offset
            pygame.draw.rect(self.screen, self.lineColor, ((x*self.windowX/self.gridX)-(self.lineThickness/2), 0, self.lineThickness, self.windowY))

        for y in range(self.gridY+1): #horizontal lines 6px wide with offset
            pygame.draw.rect(self.screen, self.lineColor, (0, (y*self.windowY/self.gridY)-(self.lineThickness/2), self.windowX, self.lineThickness))

    def getCellState(self, x, y):
        return self.grid[x][y]

    def flipCellState(self, x, y):
        if x >= 0 and x < self.gridX and y >= 0 and y < self.gridY:
            self.grid[x][y] = ((self.grid[x][y])+1) % 2

if __name__ == "__main__":
    game = Game(500, 500)



