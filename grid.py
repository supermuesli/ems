import datetime, sys
from pygame.math import Vector2


class GridComponent:
    def __init__(self, id_: str, coordX: int, coordY: int):
        self.id_: str = id_
        self.coordX: int = coordX
        self.coordY: int = coordY
        self.currentKWH: int = 0
        self.desiredKWH: int = 0


class Provider(GridComponent):
    def __init__(self, id_: str, coordX: int, coordY: int, maxKWH: int):
        super().__init__(id_, coordX, coordY)
        self.maxKWH = maxKWH


    # returns the satisfaction of this component in percent
    def getSatisfaction(self) -> float:
        percent = 0
        if self.currentKWH == 0:
            percent = 100
        else:
            percent = (1 - self.currentKWH/self.maxKWH) * 100
        return percent


class User(GridComponent):
    def __init__(self, id_: str, coordX: int, coordY: int):
        super().__init__(id_, coordX, coordY)

    
    # returns the satisfaction of this component in percent
    def getSatisfaction(self) -> float:
        percent = 0
        if self.desiredKWH == 0:
            percent = 100
        else:
            percent = self.currentKWH/self.desiredKWH
        return percent


class Storage(GridComponent):
    def __init__(self, id_: str, coordX: int, coordY: int, maxKWH: int):
        super().__init__(id_, coordX, coordY)
        self.maxKWH = maxKWH
    

    # returns the satisfaction of this component in percent
    def getSatisfaction(self) -> float:
        percent = 0
        if self.maxKWH == 0:
            percent = 100
        else:
            percent = self.currentKWH/self.maxKWH
        return percent


class P2x(GridComponent):
    def __init__(self, id_: str, coordX: int, coordY: int):
        super().__init__(id_, coordX, coordY)


    # returns the satisfaction of this component in percent
    def getSatisfaction(self) -> float:
        percent = 0
        if self.desiredKWH == 0:
            percent = 100
        else:
            percent = self.currentKWH/self.desiredKWH
        return percent
        

class Grid:
    def __init__(self, gridData: dict, scenario: dict, gridSize: int = 20, timestepSize: int = 1):
        self.scenario = scenario

        self.cellSize = 100
        self.gridSize = gridSize

        # timestepSize in seconds corresponds to 15 elapsed simulation minutes
        self.timestepSize = timestepSize 

        self.displayTime = datetime.datetime(year=1, month=1, day=1, hour=0)

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
        self.storages = []
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
                            id_=p['id'],
                            coordX=p['coordX'],
                            coordY=p['coordY'],
                            maxKWH=p['maxKWH']
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
                            id_=u['id'],
                            coordX=u['coordX'],
                            coordY=u['coordY']
                        )
                    )
                    self.occupiedCells[u['coordX']][u['coordY']] = True

            if key == 'storages':
                ss = gridData[key]
                for s in ss:
                    if s['coordX'] >= self.gridSize or s['coordY'] >= self.gridSize:
                        print('could not add storage "%s" as cell coordinates overflow the grid' % s['displayName'])
                        continue

                    if self.occupiedCells[s['coordX']][s['coordY']]:    
                        print('could not add storage %s as cell was already occupied' % s['displayName'])
                        continue

                    self.storages.append(
                        Storage(
                            id_=s['id'],
                            coordX=s['coordX'],
                            coordY=s['coordY'],
                            maxKWH=s['maxKWH']
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
                        P2x(
                            id_=p['id'],
                            coordX=p['coordX'],
                            coordY=p['coordY']
                        )
                    )
                    self.occupiedCells[p['coordX']][p['coordY']] = True

        # load scenario data
        self.updateScenario()

    # update currentKWH/desiredKWHs for each component in the grid
    def updateScenario(self):
        currentTime = self.displayTime.strftime("%H:%M")

        if currentTime in self.scenario:
            for key in self.scenario[currentTime]:
                if key == 'providerKWHs':
                    for componentID in self.scenario[currentTime][key]:
                        for p in self.providers:
                            if p.id_ == componentID:
                                # the scenario dictates how much kWh the provider generates at which timestep.
                                # there is, however, a maximum that a provider can generate, so if the current kWh
                                # is not consumed, then the provider won't be able to generate more even if the
                                # scenario would have dictated that to be the case
                                if p.currentKWH + self.scenario[currentTime][key][componentID] < p.maxKWH:
                                    p.currentKWH += self.scenario[currentTime][key][componentID]
                                else:
                                    p.currentKWH = self.scenario[currentTime][key][componentID]

                if key == 'userKWHs':
                    for componentID in self.scenario[currentTime][key]:
                        for u in self.users:
                            if u.id_ == componentID:
                                # the users energy needs are strictly timespecific
                                u.desiredKWH = self.scenario[currentTime][key][componentID]

                if key == 'p2xKWHs':
                    for componentID in self.scenario[currentTime][key]:
                        for p in self.providers:
                            if p.id_ == componentID:
                                # the p2x energy needs are strictly timespecific
                                p.currentKWH = self.scenario[currentTime][key][componentID]


    # compute the energy flow for the next 15 minutes
    def step(self):
        # compute optimal energy flow ->
        # map each component to the component it is going to use in the next timestep

        # check satisfaction of each component in providers, users, storages, p2xs
        for p in self.providers:
            for u in self.users:
                for s in self.storages:
                    for p2x in self.p2xs:
                        # self.distribution[..] = ..
                        pass
    

        self.displayTime += datetime.timedelta(minutes=15)
        self.updateScenario()


    def getComponentAt(self, x: int, y: int) -> GridComponent:
        for p in self.providers:
            if p.coordX == x and p.coordY == y:
                return p
        for u in self.users:
            if u.coordX == x and u.coordY == y:
                return u
        for s in self.storages:
            if s.coordX == x and s.coordY == y:
                return s
        for p in self.p2xs:
            if p.coordX == x and p.coordY == y:
                return p

        print('could not find component at position (%d, %d)' % (x, y))
        sys.exit(1)
    