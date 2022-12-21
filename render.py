from grid import Grid
import sys, pygame, time


# window context
pygame.init()
displayInfo = pygame.display.Info()
windowSize = windowWidth, windowHeight = displayInfo.current_w, displayInfo.current_h
borderWidth = 10
zoomFactor = 1.0
fontSize = 64
font = pygame.font.SysFont(None, fontSize)
screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN)

# colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (100, 100, 100)
red = (255, 0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
purple = (255, 0, 255)

# sprites
providerSprite = pygame.image.load("assets/images/provider.png")
userSprite = pygame.image.load("assets/images/user.png")
storageSprite = pygame.image.load("assets/images/storage.png")
p2xSprite = pygame.image.load("assets/images/p2x.png")


def getRenderRects(grid: Grid):
    providerRects = []
    for p in grid.providers:
        renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
        providerRects.append(
            (
                providerSprite.get_rect().move(
                    (zoomFactor*renderX, zoomFactor*renderY)
                )
            )
        )

    userRects = []
    for u in grid.users:
        renderX, renderY = getRenderPosition(grid.cellSize, u.coordX, u.coordY)
        userRects.append(
            (
                userSprite.get_rect().move(
                    (zoomFactor*renderX, zoomFactor*renderY)
                )
            )
        )

    storageRects = []
    for s in grid.storages:
        renderX, renderY = getRenderPosition(grid.cellSize, s.coordX, s.coordY)
        storageRects.append(
            (
                storageSprite.get_rect().move(
                    (zoomFactor*renderX, zoomFactor*renderY)
                )
            )
        )

    p2xRects = []
    for p in grid.p2xs:
        renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
        p2xRects.append(
            (
                p2xSprite.get_rect().move(
                    (zoomFactor*renderX, zoomFactor*renderY)
                )
            )
        )
    
    return providerRects, userRects, storageRects, p2xRects


def handleWindowClose(event):
    if event.type == pygame.QUIT: 
        sys.exit()


def handleMouseWheel(event):
    global zoomFactor

    if event.type == pygame.MOUSEWHEEL:
        # scroll down
        if event.y == -1:
            zoomFactor *= 0.95

        # scroll up
        if event.y == 1:
            zoomFactor *= 1.05                


def handleMouseClick(grid: Grid, event):
    # mouse click -> add or remove grid cell (not persistent)
    if event.type == pygame.MOUSEBUTTONDOWN:
        # left click -> add cell
        if event.button == 1:
            pos = pygame.mouse.get_pos()
            x, y = getGridPosition(grid.cellSize, pos[0], pos[1])
            grid.cells[x][y] = True
            grid.resetEquilibrium()

        # right click -> remove cell
        if event.button == 3:
            pos = pygame.mouse.get_pos()
            x, y = getGridPosition(grid.cellSize, pos[0], pos[1])
            grid.cells[x][y] = False
            grid.resetEquilibrium()


def handleKeyPress(font, grid: Grid, event):
    font = pygame.font.SysFont(None, round(zoomFactor*fontSize))

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
        handleMouseWheel(event)
        handleKeyPress(font, grid, event)


def getRenderPosition(cellSize: int, x: int, y: int) -> (int, int):
    """ Converts a cell position on the grid to a position on the canvas
    
    Args:
        x(int): x position in grid space
        y(int): y position in grid space
    
    Returns:
        tuple: position tuple (x, y) in render space
    """
    return x*cellSize, y*cellSize



def getGridPosition(cellSize: int, x: float, y: float) -> (int, int):
    """ Converts a position on the canvas to cell position on the grid.

    Args:
        x(float): x position in render space
        y(float): y position in render space
    
    Returns:
        tuple: position tuple (x, y) in grid space
    """

    return round((x/(zoomFactor*cellSize) - 0.5)), round((y/(zoomFactor*cellSize) - 0.5))


def getGridColor(grid: Grid, x: int, y: int) -> tuple:
    """ Get grid color based on satisfaction of component that resides on the given coordiantes.

    Args:
        x(float): x position in grid space
        y(float): y position in grid space
    
    Returns:
        tuple: RGB color: green if satisfaction > 2/3, yellow if > 1/3 and red else 
    """

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


def getZoomedSpriteSize(sprite):
    width, height = sprite.get_size()

    return (zoomFactor*width, zoomFactor*height)


def renderGridCells(grid: Grid):
    for y in range(len(grid.cells)):
        for x in range(len(grid.cells[y])):
            if grid.cells[x][y]:
                renderX, renderY = getRenderPosition(grid.cellSize, x, y)
                pygame.draw.rect(
                    screen, 
                    getGridColor(grid, x, y), 
                    pygame.Rect(
                        zoomFactor*renderX, 
                        zoomFactor*renderY,
                        zoomFactor*grid.cellSize, 
                        zoomFactor*grid.cellSize
                    ),
                    round(zoomFactor*borderWidth)
                )


def renderGridComponents(grid: Grid, providerRects, userRects, storageRects, p2xRects, font):
    font = pygame.font.SysFont(None, round(zoomFactor*fontSize))
    
    # render icons
    for rect in providerRects:
        screen.blit(
            pygame.transform.scale(
                providerSprite, 
                getZoomedSpriteSize(providerSprite)
            ), 
            rect
        )
    
    for rect in userRects:
        screen.blit(
            pygame.transform.scale(
                userSprite, 
                getZoomedSpriteSize(userSprite)
            ), 
            rect
        )
    
    for rect in storageRects:
        screen.blit(
            pygame.transform.scale(
                storageSprite, 
                getZoomedSpriteSize(storageSprite)
            ), 
            rect
        )
    
    for rect in p2xRects:
        screen.blit(
            pygame.transform.scale(
                p2xSprite, 
                getZoomedSpriteSize(p2xSprite)
            ), 
            rect
        )

    # render satisfaction percent text
    for p in grid.providers:
        if grid.cells[p.coordX][p.coordY]:
            percentText = font.render(
                '%d%%' % p.getSatisfaction(), 
                True, 
                getGridColor(
                    grid, 
                    p.coordX, 
                    p.coordY
                )
            )
            
            renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
            screen.blit(
                percentText, 
                (zoomFactor*(renderX + grid.cellSize/5.7), zoomFactor*(renderY + grid.cellSize/1.5))
            )

    for u in grid.users:
        if grid.cells[u.coordX][u.coordY]:
            percentText = font.render(
                '%d%%' % u.getSatisfaction(), 
                True, 
                getGridColor(
                    grid, 
                    u.coordX, 
                    u.coordY)
                )

            renderX, renderY = getRenderPosition(grid.cellSize, u.coordX, u.coordY)
            screen.blit(
                percentText, 
                (zoomFactor*(renderX + grid.cellSize/5.7), zoomFactor*(renderY + grid.cellSize/1.5))
            )

    for s in grid.storages:
        if grid.cells[s.coordX][s.coordY]:
            percentText = font.render(
                '%d%%' % s.getSatisfaction(), 
                True, 
                getGridColor(grid, s.coordX, s.coordY)
            )

            renderX, renderY = getRenderPosition(grid.cellSize, s.coordX, s.coordY)
            screen.blit(
                percentText, 
                (zoomFactor*(renderX + grid.cellSize/5.7), zoomFactor*(renderY + grid.cellSize/1.5))
            )

    for p in grid.p2xs:
        if grid.cells[p.coordX][p.coordY]:
            percentText = font.render(
                '%d%%' % p.getSatisfaction(), 
                True, 
                getGridColor(grid, p.coordX, p.coordY)
            )

            renderX, renderY = getRenderPosition(grid.cellSize, p.coordX, p.coordY)
            screen.blit(
                percentText, 
                (zoomFactor*(renderX + grid.cellSize/5.7), zoomFactor*(renderY + grid.cellSize/1.5))
            )


def renderDisplayTime(font, displayTime):
    font = pygame.font.SysFont(None, round(zoomFactor*fontSize))
    timeText = font.render(displayTime.strftime("%H:%M"), True, white)
    screen.blit(timeText, (zoomFactor*(windowWidth-200), zoomFactor*(70)))


def renderMousePosition(font, cellSize: int):
    font = pygame.font.SysFont(None, round(zoomFactor*fontSize))

    pos = pygame.mouse.get_pos()
    x, y = getGridPosition(cellSize, pos[0], pos[1])

    timeText = font.render('x:%d | y:%d' % (x, y), True, white)
    screen.blit(timeText, (zoomFactor*(windowWidth-200), zoomFactor*(230)))


def renderEquilibrium(font, equilibrium: int):
    font = pygame.font.SysFont(None, round(zoomFactor*fontSize))

    if 2/3 < equilibrium/100:
        color = green
    elif 1/3 < equilibrium/100 < 2/3:
        color = yellow
    else:
        color = red

    timeText = font.render('%d%%' % equilibrium, True, color)
    screen.blit(timeText, (zoomFactor*(windowWidth-200), zoomFactor*(360)))


def renderComponentDependencies(grid):
    for componentID in grid.dependencyMap:
        for adjacentComponentID in grid.dependencyMap[componentID]:
            srcX, srcY = grid.getPositionOf(componentID)
            trgX, trgY = grid.getPositionOf(adjacentComponentID)
            srcRenderX, srcRenderY = getRenderPosition(grid.cellSize, srcX+0.5, srcY+0.5) 
            trgRenderX, trgRenderY = getRenderPosition(grid.cellSize, trgX+0.5, trgY+0.5)

            pygame.draw.line(
                screen, 
                purple, 
                (zoomFactor*srcRenderX, zoomFactor*srcRenderY),
                (zoomFactor*trgRenderX, zoomFactor*trgRenderY),
                round(zoomFactor*borderWidth)
            )


def render(grid: Grid):
    startTime = time.time()
    
    # render loop
    while True:
        # get grid component rectangles
        providerRects, userRects, storageRects, p2xRects = getRenderRects(grid)

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

