from pygame.math import Vector2

class Grid:
    def __init__(self, gridData: dict, gridSize: int = 100, timestepSize: int = 1):
        self.gridSize = gridSize
        self.timestepSize = timestepSize # timestepSize in seconds corresponds to 15 elapsed simulation minutes

        self.connections = []
        self.providers = []
        self.users = []
        self.stores = []
        self.p2xs = []

        # load gridData
        for key in gridData:
            if key == 'gridConnections':
                cs = gridData[key]
                for c in cs:
                    self.connections.append(
                        (
                            Vector2(round(c[0][0]*gridSize), round(c[0][1]*gridSize)), 
                            Vector2(round(c[1][0]*gridSize), round(c[1][1]*gridSize))
                        )
                    )

            if key == 'providers':
                ps = gridData[key]
                for p in ps:
                    self.providers.append(
                        Provider(
                            id=p['id'],
                            coordX=p['coordX']*gridSize,
                            coordY=p['coordY']*gridSize,
                            maxKWH=p['maxKWH']
                        )
                    )

            if key == 'users':
                us = gridData[key]
                for u in us:
                    self.users.append(
                        User(
                            id=u['id'],
                            coordX=u['coordX']*gridSize,
                            coordY=u['coordY']*gridSize,
                            maxKWH=u['maxKWH']
                        )
                    )

            if key == 'stores':
                ss = gridData[key]
                for s in ss:
                    self.stores.append(
                        Store(
                            id=s['id'],
                            coordX=s['coordX']*gridSize,
                            coordY=s['coordY']*gridSize,
                            maxKWH=s['maxKWH']
                        )
                    )

            if key == 'p2xs':
                ps = gridData[key]
                for p in ps:
                    self.p2xs.append(
                        Store(
                            id=p['id'],
                            coordX=p['coordX']*gridSize,
                            coordY=p['coordY']*gridSize,
                            maxKWH=p['maxKWH']
                        )
                    )
                

    def step(self):
        # compute optimal energy flow in the next timestep
        print('step')

class GridComponent:
    def __init__(self, id: int, coordX: int, coordY: int, maxKWH: int):
        self.id: int = id
        self.coordX: int = coordX
        self.coordY: int = coordY
        self.maxKWH: int = maxKWH


class Provider(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, maxKWH: int):
        super().__init__(id, coordX, coordY, maxKWH)


class User(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, maxKWH: int):
        super().__init__(id, coordX, coordY, maxKWH)


class Store(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, maxKWH: int):
        super().__init__(id, coordX, coordY, maxKWH)


class P2x(GridComponent):
    def __init__(self, id: int, coordX: int, coordY: int, maxKWH: int):
        super().__init__(id, coordX, coordY, maxKWH)

