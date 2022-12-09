from grid import Grid
from pygame.math import Vector2
import sys, pygame, time, datetime


# misc
epsilon = 1**(-8)

# window context
windowSize = windowWidth, windowHeight = 1600, 1200
screen = pygame.display.set_mode(windowSize)

# colors
black = (0, 0, 0)
white = (255, 255, 255)

# sprites
providerSprite = pygame.image.load("assets/images/provider.png")
userSprite = pygame.image.load("assets/images/user.png")
storeSprite = pygame.image.load("assets/images/store.png")
p2xSprite = pygame.image.load("assets/images/p2x.png")


def getRects(grid: Grid):
    providerRects = []
    for p in grid.providers:
        providerRects.append(
            providerSprite.get_rect().move(
                p.coordX, p.coordY
            )
        )

    userRects = []
    for u in grid.users:
        userRects.append(
            userSprite.get_rect().move(
                u.coordX, u.coordY
            )
        )

    storeRects = []
    for s in grid.stores:
        storeRects.append(
            storeSprite.get_rect().move(
                s.coordX, s.coordY
            )
        )

    p2xRects = []
    for p in grid.p2xs:
        p2xRects.append(
            p2xSprite.get_rect().move(
                p.coordX, p.coordY
            )
        )
    
    return providerRects, userRects, storeRects, p2xRects


def handleEvents():
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

            # key press esc -> quit
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            # key press space -> pause
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    print('Pause')
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: 
                                sys.exit()

                            if event.type == pygame.KEYDOWN: 
                                if event.key == pygame.K_ESCAPE:
                                    sys.exit()

                            if event.type == pygame.KEYDOWN: 
                                if event.key == pygame.K_SPACE:
                                    print('Resume')
                                    paused = False


def renderGrid(grid: Grid):
    borderWidthPx = 10
    for c in grid.connections:
        # c[0] src   c[1] trg
        for x in range(round(c[0].x), round(c[1].x)+grid.gridSize, grid.gridSize):
            for y in range(round(c[0].y), round(c[1].y)+grid.gridSize, grid.gridSize):
                pygame.draw.rect(
                    screen, 
                    black, 
                    pygame.Rect(
                        x, 
                        y,
                        grid.gridSize, 
                        grid.gridSize
                    ),
                    borderWidthPx
                )


def renderGridComponents(providerRects, userRects, storeRects, p2xRects):
    for rect in providerRects:
        screen.blit(providerSprite, rect)
    for rect in userRects:
        screen.blit(userSprite, rect)
    for rect in storeRects:
        screen.blit(storeSprite, rect)
    for rect in p2xRects:
        screen.blit(p2xSprite, rect)


def renderDisplayTime(displayTime):
    font = pygame.font.SysFont(None, 64)
    timeText = font.render(displayTime.strftime("%H:%M"), True, black)
    screen.blit(timeText, (windowWidth-200, 70))


def renderEnergyManagement(grid, providerRects, userRects, storeRects, p2xRects):
    # TODO
    pass


def render(grid: Grid):
    pygame.init()
    
    # get grid component rectangles
    providerRects, userRects, storeRects, p2xRects = getRects(grid)

    startTime = time.time()
    displayTime = datetime.datetime(year=1, month=1, day=1, hour=0)

    # render loop
    while True:
        # handle window events
        handleEvents()

        # clear canvas with black
        screen.fill(white)

        # buffer grid
        renderGrid(grid)

        # buffer grid components
        renderGridComponents(providerRects, userRects, storeRects, p2xRects)

        # buffer energy management decisions
        renderEnergyManagement(grid, providerRects, userRects, storeRects, p2xRects)

        # buffer display time
        renderDisplayTime(displayTime)

        # dump buffer (render)
        pygame.display.flip()

        # evaluate timestep and make the next step if needed
        endTime = time.time()
        if endTime - startTime > grid.timestepSize:
            grid.step()
            displayTime += datetime.timedelta(minutes=15)
            startTime = time.time()

