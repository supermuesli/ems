from grid import Grid
import sys, json


def mockGrid() -> Grid:
    filePath = 'assets/settings/test_grid.json'
    try:
        file = open(filePath, 'r')
        gridData = json.load(file)
    except:
        print('could not open ' + filePath)
        sys.exit(1)

    filePath = 'assets/settings/scenario.json'
    try:
        file = open(filePath, 'r')
        scenario = json.load(file)
    except:
        print('could not open ' + filePath)
        sys.exit(1)

    return Grid(gridData=gridData, gridSize=15, scenario=scenario)


def test_getCellGroups():
    g = mockGrid()
    
    activeNeighbourCells00 = g.getCellSubgroup(0, 0)
    
    actualActiveNeighbourCells00 = [
        (0,0),(1,0),(2,0), 
        (0,1),(1,1),(2,1)
    ]

    assert len(activeNeighbourCells00) == len(actualActiveNeighbourCells00)
    for a in activeNeighbourCells00:
        assert a in actualActiveNeighbourCells00

    cellGroups = g.getCellGroups()
    
    actualCellGroups = [
        [(0,0),(1,0),(2,0), 
         (0,1),(1,1),(2,1)], 
            
        [(4,0),(5,0), 
               (5,1)], 
                
        [(7,0)]
    ]

    assert len(cellGroups) == len(actualCellGroups)
    for c in cellGroups:
        for pos in c:
            posFound = False
            for ac in actualCellGroups:
                for apos in ac:
                    if apos == pos:
                        posFound = True

            assert posFound


def test_getCellDistance():
    grid = mockGrid()

    cell1 = (0, 0)
    cell2 = (2, 1)
    d12 = grid.getCellDistance(cell1[0], cell1[1], cell2[0], cell2[1])
    assert d12 == 3

    cell3 = (0, 0)
    cell4 = (0, 0)
    d34 = grid.getCellDistance(cell3[0], cell3[1], cell4[0], cell4[1])
    assert d34 == 0
    
    cell5 = (1, 1)
    cell6 = (0, 0)
    d56 = grid.getCellDistance(cell5[0], cell5[1], cell6[0], cell6[1])
    assert d56 == 2

    cell7 = (2, 1)
    cell8 = (0, 0)
    d78 = grid.getCellDistance(cell7[0], cell7[1], cell8[0], cell8[1])
    assert d78 == 3


def test_sortComponentsByDistanceTo():
    grid = mockGrid()

    sortedProviders = grid.sortComponentsByDistanceTo(grid.providers, grid.users[0])

    actualSortedProviders = [grid.providers[1], grid.providers[0]]

    assert sortedProviders == actualSortedProviders