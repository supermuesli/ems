from pygame.math import Vector2

class Grid:
    def __init__(self, gridData: dict, gridSize: int = 20, timestepSize: int = 1):
        self.cellSize = 100
        self.gridSize = gridSize

        # timestepSize in seconds corresponds to 15 elapsed simulation minutes
        self.timestepSize = timestepSize 

        # cells that are set to true exist, the other ones don't
        self.cells = []
        for i in range(self.gridSize):
            self.cells.append([False for j in range(self.gridSize)])

        # keep track of which cells are occupied by a component in order to prevent overlaps
        self.occupiedCells = []
        for i in range(self.gridSize):
            self.occupiedCells.append([False for j in range(self.gridSize)])

        # grid components
        self.providers = []
        self.users = []
        self.stores = []
        self.p2xs = []

        # distribution keeps track of which component ID relies on which other component ID
        self.distribution = {}

        # load gridData
        for key in gridData:
            if key == 'cellSize':
                self.cellSize = gridData[key]

            if key == 'gridCells':
                gcs = gridData[key]
                for gc in gcs:
                    for x in range(round(gc[0][0]), round(gc[1][0])+1):
                        for y in range(round(gc[0][1]), round(gc[1][1])+1):
                            self.cells[x][y] = True

            if key == 'providers':
                ps = gridData[key]
                for p in ps:
                    if not self.occupiedCells[p['coordX']][p['coordY']]:
                        self.providers.append(
                            Provider(
                                id=p['id'],
                                coordX=p['coordX'],
                                coordY=p['coordY'],
                                desiredKWH=p['desiredKWH']
                            )
                        )
                        self.occupiedCells[p['coordX']][p['coordY']] = True
                    else:
                        print('could not add provider %s as cell was already occupied' % p['displayName'])

            if key == 'users':
                us = gridData[key]
                for u in us:
                    if not self.occupiedCells[u['coordX']][u['coordY']]:
                        self.users.append(
                            User(
                                id=u['id'],
                                coordX=u['coordX'],
                                coordY=u['coordY'],
                                desiredKWH=u['desiredKWH']
                            )
                        )
                        self.occupiedCells[u['coordX']][u['coordY']] = True
                    else:
                        print('could not add user %s as cell was already occupied' % u['displayName'])


            if key == 'stores':
                ss = gridData[key]
                for s in ss:
                    if not self.occupiedCells[s['coordX']][s['coordY']]:
                        self.stores.append(
                            Store(
                                id=s['id'],
                                coordX=s['coordX'],
                                coordY=s['coordY'],
                                desiredKWH=s['desiredKWH']
                            )
                        )
                        self.occupiedCells[s['coordX']][s['coordY']] = True
                    else:
                        print('could not add store %s as cell was already occupied' % s['displayName'])

            if key == 'p2xs':
                ps = gridData[key]
                for p in ps:
                    if not self.occupiedCells[p['coordX']][p['coordY']]:
                        self.p2xs.append(
                            Store(
                                id=p['id'],
                                coordX=p['coordX'],
                                coordY=p['coordY'],
                                desiredKWH=p['desiredKWH']
                            )
                        )
                        self.occupiedCells[p['coordX']][p['coordY']] = True
                    else:
                        print('could not add p2x %s as cell was already occupied' % p['displayName'])

    def step(self):
        # compute optimal energy flow ->
        # map each component to the component it is going to use in the next timestep

        # check satisfiedness of each component in providers, users, stores, p2xs
        print('step')


class GridComponent:
    def __init__(self, id: int, coordX: int, coordY: int, desiredKWH: int):
        self.id: int = id
        self.coordX: int = coordX
        self.coordY: int = coordY
        self.desiredKWH: int = desiredKWH
        self.currentKWH: int = 0


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

