from pygame.math import Vector2


class Grid:
    def __init__(self, gridData: dict, scenario: dict, gridSize: int = 20, timestepSize: int = 1):
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

        # verify and load gridData
        for key in gridData:
            if key == 'cellSize':
                self.cellSize = gridData[key]

            if key == 'gridCells':
                gcs = gridData[key]
                for gc in gcs:
                    for x in range(round(gc[0][0]), round(gc[1][0])+1):
                        for y in range(round(gc[0][1]), round(gc[1][1])+1):
                            if x >= self.gridSize or y >= self.gridSize:
                                print('could not add cell (%d, %d) as cell overflows the grid' % (x, y))
                                continue
        
                            self.cells[x][y] = True

            if key == 'providers':
                ps = gridData[key]
                for p in ps:
                    if p['coordX'] >= self.gridSize or p['coordY'] >= self.gridSize:
                        print('could not add provider "%s" as cell coordinates overflow the grid' % p['displayName'])
                        continue

                    if self.occupiedCells[p['coordX']][p['coordY']]:
                        print('could not add provider "%s" as cell was already occupied' % p['displayName'])
                        continue

                    self.providers.append(
                        Provider(
                            id=p['id'],
                            coordX=p['coordX'],
                            coordY=p['coordY']
                        )
                    )
                    self.occupiedCells[p['coordX']][p['coordY']] = True

            if key == 'users':
                us = gridData[key]
                for u in us:
                    if u['coordX'] >= self.gridSize or u['coordY'] >= self.gridSize:
                        print('could not add user "%s" as cell coordinates overflow the grid' % u['displayName'])
                        continue

                    if self.occupiedCells[u['coordX']][u['coordY']]:
                        print('could not add user %s as cell was already occupied' % u['displayName'])
                        continue

                    self.users.append(
                        User(
                            id=u['id'],
                            coordX=u['coordX'],
                            coordY=u['coordY']
                        )
                    )
                    self.occupiedCells[u['coordX']][u['coordY']] = True

            if key == 'stores':
                ss = gridData[key]
                for s in ss:
                    if s['coordX'] >= self.gridSize or s['coordY'] >= self.gridSize:
                        print('could not add store "%s" as cell coordinates overflow the grid' % s['displayName'])
                        continue

                    if self.occupiedCells[s['coordX']][s['coordY']]:    
                        print('could not add store %s as cell was already occupied' % s['displayName'])
                        continue

                    self.stores.append(
                        Store(
                            id=s['id'],
                            coordX=s['coordX'],
                            coordY=s['coordY']
                        )
                    )
                    self.occupiedCells[s['coordX']][s['coordY']] = True
                        
            if key == 'p2xs':
                ps = gridData[key]
                for p in ps:
                    if p['coordX'] >= self.gridSize or p['coordY'] >= self.gridSize:
                        print('could not add p2x "%s" as cell coordinates overflow the grid' % p['displayName'])
                        continue

                    if self.occupiedCells[p['coordX']][p['coordY']]:    
                        print('could not add p2x %s as cell was already occupied' % p['displayName'])
                        continue

                    self.p2xs.append(
                        Store(
                            id=p['id'],
                            coordX=p['coordX'],
                            coordY=p['coordY']
                        )
                    )
                    self.occupiedCells[p['coordX']][p['coordY']] = True
                    
        # verify and load scenario
        for hour in scenario:
            for key in scenario[hour]:
                if key == 'providerKWHs':
                    for componentID in scenario[hour][key]:
                        for p in self.providers:
                            if p.id == componentID:
                                p.desiredKWH = scenario[hour][key][componentID]

    def step(self):
        # compute optimal energy flow ->
        # map each component to the component it is going to use in the next timestep

        # check satisfiedness of each component in providers, users, stores, p2xs
        for p in self.providers:
            for u in self.users:
                for s in self.stores:
                    for p2x in self.p2xs:
                        # self.distribution[..] = ..
                        pass


class GridComponent:
    def __init__(self, id: int, coordX: int, coordY: int):
        self.id: int = id
        self.coordX: int = coordX
        self.coordY: int = coordY
        self.desiredKWH: int = 1
        self.currentKWH: int = 0


class Provider(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int):
        super().__init__(id, coordX, coordY)


class User(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int):
        super().__init__(id, coordX, coordY)


class Store(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int):
        super().__init__(id, coordX, coordY)


class P2x(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int):
        super().__init__(id, coordX, coordY)

