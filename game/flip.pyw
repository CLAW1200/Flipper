"""
FLIPPER
"""
import pygame
import random

class Game:
    def __init__(self, windowX, windowY):
        pygame.init() 
        pygame.display.set_caption("Flipper") 
        self.gridX = 2
        self.gridY = 2
        self.windowX = windowX
        self.windowY = windowY
        self.screen = pygame.display.set_mode((windowX, windowY))
        self.clock = pygame.time.Clock()
        self.running = True
        self.startingCellColor = (40,40,150)
        self.cellWinColor = (40,150,40)
        self.background = (25,25,25)
        self.cellColor = self.startingCellColor
        self.lineColor = (255,255,255)
        self.run()

    def checkWin(self):
        for x in range(self.gridX):
            for y in range(self.gridY):
                if self.grid[x][y] == 0:
                    return False
        return True

    def userWon(self):
        self.soundPlayer("click_high.wav")
        #keep drawing grid until user presses a key
        self.cellColor = self.cellWinColor
        self.updateGrid()
        pygame.display.flip()
        #wait for user to press a key
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.increaseGrid()
                    self.start()
                    return

    def soundPlayer(self, sound):
        pygame.mixer.Sound.play(pygame.mixer.Sound(sound))

    def increaseGrid(self):
        self.gridX += 1
        self.gridY += 1
        self.soundPlayer("click_up.wav")
        self.start()
    
    def decreaseGrid(self):
        if self.gridX < 2:
            pass
        else:
            self.gridX -= 1
            self.gridY -= 1
            self.soundPlayer("click_down.wav")
            self.start()


    def run(self):
        self.start()
        pygame.display.flip()
        while self.running:
            self.clock.tick(165)
            self.update()
            pygame.display.flip()
        self.soundPlayer("click_loose.wav")

    def flip(self, x, y):
        #invert cells
        self.flipCellState(x, y)
        self.flipCellState(x+1, y)
        self.flipCellState(x-1, y)
        self.flipCellState(x, y+1)
        self.flipCellState(x, y-1)
        if self.checkWin():
            self.userWon()
        else:
            self.soundPlayer("click_low.wav")
        

    def update(self):
        self.updateGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    self.increaseGrid()
                if event.key == pygame.K_DOWN:
                    self.decreaseGrid()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    x = int(mousePos[0]//(self.windowX/self.gridX))
                    y = int(mousePos[1]//(self.windowY/self.gridY))
                    self.flip(x, y)
          
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
            if self.grid[x][y] == 1:
                self.grid[x][y] = 0
            else:
                self.grid[x][y] = 1


if __name__ == "__main__":
    game = Game(300, 300)



