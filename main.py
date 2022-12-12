from grid import Grid
from render import render
import json

def main():
    filePath = 'assets/settings/grid.json'
    try:
        file = open(filePath, 'r')
        gridData = json.load(file)
    except:
        print('could not open ' + filePath)
        os.exit(1)

    filePath = 'assets/settings/scenario.json'
    try:
        file = open(filePath, 'r')
        scenario = json.load(file)
    except:
        print('could not open ' + filePath)
        os.exit(1)

    g = Grid(gridData=gridData, gridSize=15, scenario=scenario)
    render(grid=g)

if __name__ == '__main__':
    main()
