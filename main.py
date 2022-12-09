from grid import Grid
from render import render
import json

def main():
    print("Primitive Energy Management System")

    filePath = 'assets/grid.json'
    try:
        file = open(filePath, 'r')
        gridData = json.load(file)
    except:
        print('could not open ' + filePath)
        os.exit(1)

    g = Grid(gridData=gridData, gridSize=15)
    render(grid=g)

if __name__ == '__main__':
    main()
