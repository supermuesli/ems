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

# sprites
providerSprite = pygame.image.load("assets/images/provider.png")
userSprite = pygame.image.load("assets/images/user.png")
storeSprite = pygame.image.load("assets/images/store.png")
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

    storeRects = []
    for s in grid.stores:
        storeRects.append(
            (
                storeSprite.get_rect().move(
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
    
    return providerRects, userRects, storeRects, p2xRects


def handleEscape(event):
    if event.type == pygame.QUIT: 
        sys.exit()

    # key press esc -> quit
    if event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_ESCAPE:
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


def handleEvents(font, grid: Grid):
    for event in pygame.event.get():
            handleEscape(event)
            handleMouseClick(grid, event)

            # key press space -> pause
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    print('Pause')
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            renderMousePosition(font, grid.cellSize)
                            handleEscape(event)
            
                            if event.type == pygame.KEYDOWN: 
                                if event.key == pygame.K_SPACE:
                                    print('Resume')
                                    paused = False


def getRenderPosition(cellSize: int, x: int, y: int) -> (int, int):
    return x*cellSize, y*cellSize


def getGridPosition(cellSize: int, x: float, y: float) -> (int, int):
    return round(x/cellSize - 0.5), round(y/cellSize - 0.5)


def getGridColor(grid: Grid, x: int, y: int) -> tuple:
    for p in grid.providers:
        if p.coordX == x and p.coordY == y:
            # get grid color based on satisfiedness of component that resides on the given coordiantes
            if True:    
                return green

    for u in grid.users:
        if u.coordX == x and u.coordY == y:
            # get grid color based on satisfiedness of component that resides on the given coordiantes
            if True:    
                return green

    for s in grid.stores:
        if s.coordX == x and s.coordY == y:
            # get grid color based on satisfiedness of component that resides on the given coordiantes
            if True:    
                return yellow

    for p in grid.p2xs:
        if p.coordX == x and p.coordY == y:
            # get grid color based on satisfiedness of component that resides on the given coordiantes
            if True:    
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


def renderGridComponents(grid: Grid, providerRects, userRects, storeRects, p2xRects, font):
    # render icons
    for rect in providerRects:
        screen.blit(providerSprite, rect)
    
    for rect in userRects:
        screen.blit(userSprite, rect)
    
    for rect in storeRects:
        screen.blit(storeSprite, rect)
    
    for rect in p2xRects:
        screen.blit(p2xSprite, rect)

    # render satisfiedness percent text
    for p in grid.providers:
        if grid.cells[p.coordX][p.coordY]:
            percentText = font.render('%.1f' % (p.currentKWH/p.desiredKWH), True, getGridColor(grid, p.coordX, p.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/3, renderY + grid.cellSize/1.45))

    for u in grid.users:
        if grid.cells[u.coordX][u.coordY]:
            percentText = font.render('%.1f' % (u.currentKWH/u.desiredKWH), True, getGridColor(grid, u.coordX, u.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, u.coordX, u.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/3, renderY + grid.cellSize/1.45))

    for s in grid.stores:
        if grid.cells[s.coordX][s.coordY]:
            percentText = font.render('%.1f' % (s.currentKWH/s.desiredKWH), True, getGridColor(grid, s.coordX, s.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, s.coordX, s.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/3, renderY + grid.cellSize/1.45))

    for p in grid.p2xs:
        if grid.cells[p.coordX][p.coordY]:
            percentText = font.render('%.1f' % (p.currentKWH/p.desiredKWH), True, getGridColor(grid, p.coordX, p.coordY))
            renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
            screen.blit(percentText, (renderX + grid.cellSize/3, renderY + grid.cellSize/1.45))


def renderDisplayTime(font, displayTime):
    timeText = font.render(displayTime.strftime("%H:%M"), True, white)
    screen.blit(timeText, (windowWidth-200, 70))


def renderMousePosition(font, cellSize: int):
    pos = pygame.mouse.get_pos()
    x, y = getGridPosition(cellSize, pos[0], pos[1])

    timeText = font.render("x:%d | y:%d" % (x, y), True, white)
    screen.blit(timeText, (windowWidth-280, windowHeight-120))


def renderEnergyManagement(grid):
    # TODO
    pass


def render(grid: Grid):
    pygame.init()
    font = pygame.font.SysFont(None, 64)
    
    # get grid component rectangles
    providerRects, userRects, storeRects, p2xRects = getRenderRects(grid)

    startTime = time.time()
    displayTime = datetime.datetime(year=1, month=1, day=1, hour=0)

    # render loop
    while True:
        # handle window events
        handleEvents(font, grid=grid)

        # clear canvas with black
        screen.fill(black)

        # buffer grid components
        renderGridComponents(grid, providerRects, userRects, storeRects, p2xRects, font)

        # buffer energy management decisions
        renderEnergyManagement(grid)

        # buffer grid
        renderGridCells(grid)

        # buffer display time
        renderDisplayTime(font, displayTime)

        # buffer mouse grid position
        renderMousePosition(font, cellSize=grid.cellSize)

        # dump buffer (render)
        pygame.display.flip()

        # execute next grid decision if timestep is over
        endTime = time.time()
        if endTime - startTime > grid.timestepSize:
            grid.step()
            displayTime += datetime.timedelta(minutes=15)
            startTime = time.time()

        # TODO cap render to 30 or 60 fps

