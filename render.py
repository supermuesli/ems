from grid import Grid
from pygame.math import Vector2
from copy import copy
import sys, pygame, time, datetime


# misc
epsilon = 1**(-8)

# window context
windowSize = windowWidth, windowHeight = 2100, 1300
borderWidth = 10
screen = pygame.display.set_mode(windowSize)

# colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (100, 100, 100)
red = (255, 0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# sprites
providerSprite = pygame.image.load("assets/images/provider.png")
userSprite = pygame.image.load("assets/images/user.png")
storageSprite = pygame.image.load("assets/images/storage.png")
p2xSprite = pygame.image.load("assets/images/p2x.png")


def getRenderRects(grid: Grid):
    providerRects = []
    for p in grid.providers:
        providerRects.append(
            (
                providerSprite.get_rect().move(
                    getRenderPosition(grid.cellSize, p.coordX, p.coordY)
                )
            )
        )

    userRects = []
    for u in grid.users:
        userRects.append(
            (
                userSprite.get_rect().move(
                    getRenderPosition(grid.cellSize, u.coordX, u.coordY)
                )
            )
        )

    storageRects = []
    for s in grid.storages:
        storageRects.append(
            (
                storageSprite.get_rect().move(
                    getRenderPosition(grid.cellSize, s.coordX, s.coordY)
                )
            )
        )

    p2xRects = []
    for p in grid.p2xs:
        p2xRects.append(
            (
                p2xSprite.get_rect().move(
                    getRenderPosition(grid.cellSize, p.coordX, p.coordY)
                )
            )
        )
    
    return providerRects, userRects, storageRects, p2xRects


def handleWindowClose(event):
    if event.type == pygame.QUIT: 
        sys.exit()


def handleMouseClick(grid: Grid, event):
    # mouse click -> add or remove grid cell (not persistent)
    if event.type == pygame.MOUSEBUTTONDOWN:
        # left click -> add cell
        if event.button == 1:
            pos = pygame.mouse.get_pos()
            x, y = getGridPosition(grid.cellSize, pos[0], pos[1])
            grid.cells[x][y] = True

        # right click -> remove cell
        if event.button == 3:
            pos = pygame.mouse.get_pos()
            x, y = getGridPosition(grid.cellSize, pos[0], pos[1])
            grid.cells[x][y] = False


def handleKeyPress(font, grid: Grid, event):
    if event.type == pygame.KEYDOWN: 
        # key press esc -> quit
        if event.key == pygame.K_ESCAPE:
            sys.exit()

        # key press up -> increase tickrate
        if event.key == pygame.K_UP:
            if grid.timestepSize * 0.9 >= 1**(-8):
                grid.timestepSize = 1**(-8)
            else:
                grid.timestepSize *= 0.9

        # key press down -> decrease tickrate
        if event.key == pygame.K_DOWN:
            if grid.timestepSize * 1.1 <= 2:
                grid.timestepSize *= 1.1
            else:
                grid.timestepSize = 2

        # key press space -> pause
        if event.key == pygame.K_SPACE:
            # render pause text                
            pauseText = font.render('Paused', True, white)
            screen.blit(pauseText, (windowWidth-200, 150))
            pygame.display.flip()
            
            paused = True
            while paused:
                for event in pygame.event.get():
                    handleWindowClose(event)
    
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_SPACE:
                            paused = False


def handleEvents(font, grid: Grid):
    for event in pygame.event.get():
        handleWindowClose(event)
        handleMouseClick(grid, event)
        handleKeyPress(font, grid, event)


# converts a cell position on the grid to a position on the canvas
def getRenderPosition(cellSize: int, x: int, y: int) -> (int, int):
    return x*cellSize, y*cellSize


# converts a position on the canvas to cell position on the grid
def getGridPosition(cellSize: int, x: float, y: float) -> (int, int):
    return round(x/cellSize - 0.5), round(y/cellSize - 0.5)


# get grid color based on satisfaction of component that resides on the given coordiantes
def getGridColor(grid: Grid, x: int, y: int) -> tuple:
    for p in grid.providers:
        if p.coordX == x and p.coordY == y:
            if p.getSatisfaction()/100 > 2/3:    
                return green
            if 2/3 > p.getSatisfaction()/100 > 1/3:    
                return yellow
            if 1/3 > p.getSatisfaction()/100:    
                return red

    for u in grid.users:
        if u.coordX == x and u.coordY == y:
            if u.getSatisfaction()/100 > 2/3:    
                return green
            if 2/3 > u.getSatisfaction()/100 > 1/3:    
                return yellow
            if 1/3 > u.getSatisfaction()/100:    
                return red

    for s in grid.storages:
        if s.coordX == x and s.coordY == y:
            if s.getSatisfaction()/100 > 2/3:    
                return green
            if 2/3 > s.getSatisfaction()/100 > 1/3:    
                return yellow
            if 1/3 > s.getSatisfaction()/100:    
                return red

    for p in grid.p2xs:
        if p.coordX == x and p.coordY == y:
            if p.getSatisfaction()/100 > 2/3:    
                return green
            if 2/3 > p.getSatisfaction()/100 > 1/3:    
                return yellow
            if 1/3 > p.getSatisfaction()/100:    
                return red

    return gray


def renderGridCells(grid: Grid):
    for x in range(len(grid.cells)):
        for y in range(len(grid.cells[x])):
            if grid.cells[x][y]:
                renderX, renderY = getRenderPosition(grid.cellSize, x, y)
                pygame.draw.rect(
                    screen, 
                    getGridColor(grid, x, y), 
                    pygame.Rect(
                        renderX, 
                        renderY,
                        grid.cellSize, 
                        grid.cellSize
                    ),
                    borderWidth
                )


def renderGridComponents(grid: Grid, providerRects, userRects, storageRects, p2xRects, font):
    # render icons
    for rect in providerRects:
        screen.blit(providerSprite, rect)
    
    for rect in userRects:
        screen.blit(userSprite, rect)
    
    for rect in storageRects:
        screen.blit(storageSprite, rect)
    
    for rect in p2xRects:
        screen.blit(p2xSprite, rect)

    # render satisfaction percent text
    for p in grid.providers:
        if grid.cells[p.coordX][p.coordY]:
            percentText = font.render('%d%%' % p.getSatisfaction(), True, getGridColor(grid, p.coordX, p.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/4, renderY + grid.cellSize/1.45))

    for u in grid.users:
        if grid.cells[u.coordX][u.coordY]:
            percentText = font.render('%d%%' % u.getSatisfaction(), True, getGridColor(grid, u.coordX, u.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, u.coordX, u.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/4, renderY + grid.cellSize/1.45))

    for s in grid.storages:
        if grid.cells[s.coordX][s.coordY]:
            percentText = font.render('%d%%' % s.getSatisfaction(), True, getGridColor(grid, s.coordX, s.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, s.coordX, s.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/4, renderY + grid.cellSize/1.45))

    for p in grid.p2xs:
        if grid.cells[p.coordX][p.coordY]:
            percentText = font.render('%d%%' % p.getSatisfaction(), True, getGridColor(grid, p.coordX, p.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/4, renderY + grid.cellSize/1.45))


def renderDisplayTime(font, displayTime):
    timeText = font.render(displayTime.strftime("%H:%M"), True, white)
    screen.blit(timeText, (windowWidth-200, 70))


def renderMousePosition(font, cellSize: int):
    pos = pygame.mouse.get_pos()
    x, y = getGridPosition(cellSize, pos[0], pos[1])

    timeText = font.render('x:%d | y:%d' % (x, y), True, white)
    screen.blit(timeText, (windowWidth-200, 230))


def renderEquilibrium(font, equilibrium: int):
    if 2/3 < equilibrium/100:
        color = green
    elif 1/3 < equilibrium/100 < 2/3:
        color = yellow
    else:
        color = red

    timeText = font.render('%d%%' % equilibrium, True, color)
    screen.blit(timeText, (windowWidth-200, 360))


def renderComponentDependencies(grid):
    for componentID in grid.dependencyMap:
        for adjacentComponentID in grid.dependencyMap[componentID]:
            srcX, srcY = grid.getPosition(componentID)
            trgX, trgY = grid.getPosition(adjacentComponentID)
            pygame.draw.line(
                screen, 
                blue, 
                getRenderPosition(grid.cellSize, srcX+0.5, srcY+0.5), 
                getRenderPosition(grid.cellSize, trgX+0.5, trgY+0.5), 
                borderWidth
            )


def render(grid: Grid):
    pygame.init()
    font = pygame.font.SysFont(None, 64)
    
    # get grid component rectangles
    providerRects, userRects, storageRects, p2xRects = getRenderRects(grid)

    startTime = time.time()
    
    # render loop
    while True:
        # handle window events
        handleEvents(font, grid=grid)

        # clear canvas with black
        screen.fill(black)

        # buffer grid
        renderGridCells(grid)

        # buffer component dependencies
        renderComponentDependencies(grid)

        # buffer grid components
        renderGridComponents(grid, providerRects, userRects, storageRects, p2xRects, font)

        # buffer display time
        renderDisplayTime(font, grid.simulationDayTime)

        # buffer mouse grid position
        renderMousePosition(font, cellSize=grid.cellSize)

        # buffer equilibrium text
        renderEquilibrium(font, grid.getRunningEquilibrium())

        # dump buffer (render)
        pygame.display.flip()

        # execute next grid decision if timestep is over
        endTime = time.time()
        if endTime - startTime > grid.timestepSize:
            grid.step()
            startTime = time.time()

        # TODO cap render to 30 or 60 fps

