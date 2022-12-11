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
            percent = self.currentKWH/self.desiredKWH * 100
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
            percent = self.currentKWH/self.maxKWH * 100
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
            percent = self.currentKWH/self.desiredKWH * 100
        return percent
        

class Grid:
    def __init__(self, gridData: dict, scenario: dict, gridSize: int = 20, timestepSize: float = 1):
        # mock simulation data of each component in the grid
        self.scenario = scenario

        # size (in px) of each cell in the grid
        self.cellSize = 100
        # size of the square grid
        self.gridSize = gridSize

        # timestepSize in seconds corresponds to 15 elapsed simulation minutes
        self.timestepSize = timestepSize 

        # keep track of simulation day time
        self.simulationDayTime = datetime.datetime(year=1, month=1, day=1, hour=0)
        
        # if the equilibrium (in percent) is 100, it means that every component in the grid is perfectly satisfied.
        # we keep accumulate the equilibrium with each step and average it over the number of steps in order to get
        # a metric that tells us how good the energy distribution works at all times
        self.accumulatedEquilibrium = 0

        # keep track of how many steps have been made. use this counter to compute a running average equilibrium
        self.stepCounter = 1

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

        # distribution keeps track of which component ID consumes which other component ID
        self.dependencyMap = {}

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

        self.resetDepencencyMap()

    # reset dependency map of each component
    def resetDepencencyMap(self):
        self.dependencyMap = {}
        for p in self.providers:
            self.dependencyMap[p.id_] = []
        for u in self.users:
            self.dependencyMap[u.id_] = []
        for s in self.storages:
            self.dependencyMap[s.id_] = []
        for p in self.p2xs:
            self.dependencyMap[p.id_] = []


    # update currentKWH/desiredKWHs for each component in the grid
    def updateScenario(self):
        # TODO interpolate between two scenario timestamps for each timestepsize that fits between those two timestamps 

        currentTime = self.simulationDayTime.strftime("%H:%M")

        if currentTime in self.scenario:
            for key in self.scenario[currentTime]:
                if key == 'providerKWHs':
                    for componentID in self.scenario[currentTime][key]:
                        for p in self.providers:
                            if p.id_ == componentID:
                                # the scenario dictates how much kWh the provider generates at which timestep.
                                # there is, however, a maximum that a provider can generate, so if the current kWh
                                # is not consumed, then the provider won't be able to generate more even if the
                                # scenario would have dictated that to be the case. in the real world, such a 
                                # generator would be put to stop
                                if p.currentKWH + self.scenario[currentTime][key][componentID] < p.maxKWH:
                                    p.currentKWH += self.scenario[currentTime][key][componentID]
                                else:
                                    p.currentKWH = p.maxKWH

                if key == 'userKWHs':
                    for componentID in self.scenario[currentTime][key]:
                        for u in self.users:
                            if u.id_ == componentID:
                                # the users energy needs are strictly timespecific
                                u.desiredKWH = self.scenario[currentTime][key][componentID]
                                u.currentKWH = 0

                if key == 'p2xKWHs':
                    for componentID in self.scenario[currentTime][key]:
                        for p in self.p2xs:
                            if p.id_ == componentID:
                                # the p2x energy needs are strictly timespecific
                                p.desiredKWH = self.scenario[currentTime][key][componentID]
                                p.currentKWH = 0


    # update the running average equilibrium of the grid
    def updateEquilibrium(self):
        compontentCount = 0
        currentAccumulatedEquilibrium = 0
        for p in self.providers:
            if self.cells[p.coordX][p.coordY]:
                currentAccumulatedEquilibrium += p.getSatisfaction()
                compontentCount += 1
        
        for u in self.users:
            if self.cells[u.coordX][u.coordY]:
                currentAccumulatedEquilibrium += u.getSatisfaction()
                compontentCount += 1
        
        for s in self.storages:
            if self.cells[s.coordX][s.coordY]:
                currentAccumulatedEquilibrium += s.getSatisfaction()
                compontentCount += 1

        for p in self.p2xs:
            if self.cells[p.coordX][p.coordY]:
                currentAccumulatedEquilibrium += p.getSatisfaction()
                compontentCount += 1

        currentAverageEquilibrium = currentAccumulatedEquilibrium/compontentCount
        self.accumulatedEquilibrium += currentAverageEquilibrium


    # the running equilibrium is a metric that can explain whether the grid distributes its energy optimally
    # among all of its components
    def getRunningEquilibrium(self):
        return self.accumulatedEquilibrium/self.stepCounter


    # given an active cells position, get all the other surrounding active cells that belong to the same group
    def getActiveNeighbourCells(self, x: int, y: int, visited=[]) -> list:
        group = []

        if (x,y) in visited:
            return group

        if self.cells[x][y]:
            group.append((x, y))
            # check left
            if y > 0:
                for pos in self.getActiveNeighbourCells(x, y-1, visited+group):
                    group.append(pos)

            # check right
            if y < len(self.cells[x]):
                for pos in self.getActiveNeighbourCells(x, y+1, visited+group):
                    group.append(pos)

            # check above
            if x > 0:
                for pos in self.getActiveNeighbourCells(x-1, y, visited+group):
                    group.append(pos)
            
            # check below
            if x < len(self.cells):
                for pos in self.getActiveNeighbourCells(x+1, y, visited+group):
                    group.append(pos)

        return group


    # get all cell groups on the grid
    def getCellGroups(self) -> list:
        groups = []
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                subGroup = self.getActiveNeighbourCells(x, y)
                if subGroup != []:
                    discardSubGroup = False
                    for pos in subGroup:
                        for group in groups:
                            for visitedPos in group:
                                if pos == visitedPos:
                                    discardSubGroup = True
                                    break
                            if discardSubGroup:
                                break
                        if discardSubGroup:
                            break
                    if not discardSubGroup:
                        groups.append(subGroup)

        return groups


    # compute the energy flow for the next 15 minutes
    def step(self):
        # map each component to the component it is going to consume in the next timestep
        # prioritize: providers -> users -> storages -> p2x

        # TODO
        # - only allow consumption if subgrids are connected
        # - use dijkstra to compute shortest path between two components, since the longer the path,
        #   the more energy is lost in the form of heat

        self.resetDepencencyMap()
        self.updateScenario()

        # who get's to consume from provider?
        for p in self.providers:
            if not self.cells[p.coordX][p.coordY]:
                continue
            
            for u in self.users:
                if not self.cells[u.coordX][u.coordY]:
                    continue

                # compute energy consumption
                if p.currentKWH > 0 and u.currentKWH < u.desiredKWH:
                    neededKWH = u.desiredKWH - u.currentKWH
                    p.currentKWH -= neededKWH
                    if p.currentKWH < 0:
                        u.currentKWH -= p.currentKWH
                        p.currentKWH = 0
                    else:
                        u.currentKWH += neededKWH

                    # keep track of component dependency
                    if p.id_ not in self.dependencyMap[u.id_]:
                        self.dependencyMap[u.id_].append(p.id_)

            for s in self.storages:
                if not self.cells[s.coordX][s.coordY]:
                    continue
            
                # compute energy consumption
                if p.currentKWH > 0 and s.currentKWH < s.maxKWH:
                    neededKWH = s.maxKWH - s.currentKWH
                    p.currentKWH -= neededKWH
                    if p.currentKWH < 0:
                        s.currentKWH -= p.currentKWH
                        p.currentKWH = 0
                    else:
                        s.currentKWH += neededKWH

                    # keep track of component dependency
                    if p.id_ not in self.dependencyMap[s.id_]:
                        self.dependencyMap[s.id_].append(p.id_)
            
            for p2x in self.p2xs:
                if not self.cells[p2x.coordX][p2x.coordY]:
                    continue
            
                # compute energy consumption
                if p.currentKWH > 0 and p2x.currentKWH < p2x.desiredKWH:
                    neededKWH = p2x.desiredKWH - p2x.currentKWH
                    p.currentKWH -= neededKWH
                    if p.currentKWH < 0:
                        p2x.currentKWH -= p.currentKWH
                        p.currentKWH = 0
                    else:
                        p2x.currentKWH += neededKWH

                    # keep track of component dependency
                    if p.id_ not in self.dependencyMap[p2x.id_]:
                        self.dependencyMap[p2x.id_].append(p.id_)
                
        # who gets to consume from storages?
        for s in self.storages:
            if not self.cells[s.coordX][s.coordY]:
                continue
        
            for u in self.users:
                if not self.cells[u.coordX][u.coordY]:
                    continue

                # compute energy consumption
                if s.currentKWH > 0 and u.currentKWH < u.desiredKWH:
                    neededKWH = u.desiredKWH - u.currentKWH
                    s.currentKWH -= neededKWH
                    if s.currentKWH < 0:
                        u.currentKWH -= s.currentKWH
                        s.currentKWH = 0
                    else:
                        u.currentKWH += neededKWH

                    # keep track of component dependency
                    if s.id_ not in self.dependencyMap[u.id_]:
                        self.dependencyMap[u.id_].append(s.id_)

            for p2x in self.p2xs:
                if not self.cells[p2x.coordX][p2x.coordY]:
                    continue
            
                # compute energy consumption
                if s.currentKWH > 0 and p2x.currentKWH < p2x.desiredKWH:
                    neededKWH = p2x.desiredKWH - p2x.currentKWH
                    s.currentKWH -= neededKWH
                    if s.currentKWH < 0:
                        p2x.currentKWH -= s.currentKWH
                        s.currentKWH = 0
                    else:
                        p2x.currentKWH += neededKWH

                    # keep track of component dependency
                    if s.id_ not in self.dependencyMap[p2x.id_]:
                        self.dependencyMap[p2x.id_].append(s.id_)

        self.simulationDayTime += datetime.timedelta(minutes=15)
        self.stepCounter += 1
        self.updateEquilibrium()


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
    

    def getPositionOf(self, componentID: str) -> tuple:
        for p in self.providers:
            if p.id_ == componentID:
                return (p.coordX, p.coordY)

        for u in self.users:
            if u.id_ == componentID:
                return (u.coordX, u.coordY)

        for s in self.storages:
            if s.id_ == componentID:
                return (s.coordX, s.coordY)

        for p in self.p2xs:
            if p.id_ == componentID:
                return (p.coordX, p.coordY)

        print('could not find component with id (%s)' % componentID)
        sys.exit(1)