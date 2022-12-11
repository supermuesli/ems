from grid import Grid
import os, json


def mockGrid() -> Grid:
    filePath = 'assets/test_grid.json'
    try:
        file = open(filePath, 'r')
        gridData = json.load(file)
    except:
        print('could not open ' + filePath)
        os.exit(1)

    filePath = 'assets/scenario.json'
    try:
        file = open(filePath, 'r')
        scenario = json.load(file)
    except:
        print('could not open ' + filePath)
        os.exit(1)

    return Grid(gridData=gridData, gridSize=15, scenario=scenario)


def test_getCellGroups():
    g = mockGrid()
    
    activeNeighbourCells00 = g.getActiveNeighbourCells(0, 0)
    
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

    cell1 = (2, 2)
    cell2 = (3, 3)
    d12 = grid.getCellDistance(cell1[0], cell1[1], cell2[0], cell2[1])
    assert d12 == 2

    cell1 = (2, 3)
    cell2 = (3, 3)
    d12 = grid.getCellDistance(cell1[0], cell1[1], cell2[0], cell2[1])
    assert d12 == 1
    
    cell1 = (0, 0)
    cell2 = (3, 3)
    d12 = grid.getCellDistance(cell1[0], cell1[1], cell2[0], cell2[1])
    assert d12 == 6
