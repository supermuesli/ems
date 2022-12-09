from pygame.math import Vector2

class Grid:
    def __init__(self, gridData: dict, gridSize: int = 100, timestepSize: int = 1):
        self.gridSize = gridSize
        self.timestepSize = timestepSize # timestepSize in seconds corresponds to 15 elapsed simulation minutes

        self.cells = []
        for i in range(gridSize):
            self.cells.append([False for j in range(gridSize)])

        self.providers = []
        self.users = []
        self.stores = []
        self.p2xs = []

        # load gridData
        for key in gridData:
            if key == 'gridCells':
                gcs = gridData[key]
                for gc in gcs:
                    for x in range(round(gc[0][0]), round(gc[1][0])+1):
                        for y in range(round(gc[0][1]), round(gc[1][1])+1):
                            self.cells[x][y] = True

            if key == 'providers':
                ps = gridData[key]
                for p in ps:
                    self.providers.append(
                        Provider(
                            id=p['id'],
                            coordX=p['coordX'],
                            coordY=p['coordY'],
                            desiredKWH=p['desiredKWH']
                        )
                    )

            if key == 'users':
                us = gridData[key]
                for u in us:
                    self.users.append(
                        User(
                            id=u['id'],
                            coordX=u['coordX'],
                            coordY=u['coordY'],
                            desiredKWH=u['desiredKWH']
                        )
                    )

            if key == 'stores':
                ss = gridData[key]
                for s in ss:
                    self.stores.append(
                        Store(
                            id=s['id'],
                            coordX=s['coordX'],
                            coordY=s['coordY'],
                            desiredKWH=s['desiredKWH']
                        )
                    )

            if key == 'p2xs':
                ps = gridData[key]
                for p in ps:
                    self.p2xs.append(
                        Store(
                            id=p['id'],
                            coordX=p['coordX'],
                            coordY=p['coordY'],
                            desiredKWH=p['desiredKWH']
                        )
                    )
                

    def step(self):
        # compute optimal energy flow ->
        # map each component to the component it is going to use in the next timestep
        print('step')

class GridComponent:
    def __init__(self, id: int, coordX: int, coordY: int, desiredKWH: int):
        self.id: int = id
        self.coordX: int = coordX
        self.coordY: int = coordY
        self.desiredKWH: int = desiredKWH


class Provider(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, desiredKWH: int):
        super().__init__(id, coordX, coordY, desiredKWH)


class User(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, desiredKWH: int):
        super().__init__(id, coordX, coordY, desiredKWH)


class Store(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, desiredKWH: int):
        super().__init__(id, coordX, coordY, desiredKWH)


class P2x(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, desiredKWH: int):
        super().__init__(id, coordX, coordY, desiredKWH)


