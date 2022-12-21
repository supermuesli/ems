# Energy Management System (EMS)

EMS is a greedy energy management system simulation that features energy provider, user, storage and P2X (power to x) components. For each component in the grid, the EMS decides which other component to consume in the next timestep by looking at the workload and proximity. 

This EMS delivers a **greedy energy** solution for a function *f* that tries to maximize the workload of each component. The running average workload per timestep in percent - called **equilibrium** - is featured on the middle right corner of the simulation UI. The higher the equilibrium, the better the energy solution for any scenario.

![showcase](https://github.com/supermuesli/ems/blob/main/assets/images/showcase.gif)

## Usage
Run the simulation by executing
```
make
```

## Controls
- hit **Arrow Up/Down** to increase or decrease the tickrate
- hit **Space** to pause or resume the simulation
- hit **Esc** to exit the simulation
- hit **Left/Right Mouse Click** to add/remove a cell to/from the grid
- hit **Mouse Wheel Up/Down** to zoom in/out 

## Settings
The `assets` directory contains an example of a *grid setting* and a *scenario setting*. 

The grid dictates which components are located where on the grid, as well as information about the time-unspecific desired energy state.

The scenario dictates which components desire which energy state at which time.

## Documentation
Use **pydoc** to check out the documentation located at `docs/`.

## Caveats
- the PyGame window is optimized for 1920x1080 displays
- you might have to increase the `gridSize` in `main.py` if your screen resolution is larger than 1920x1080 and a default grid of 20x20 is too small

## License
MIT License

Copyright (c) 2022 Ferit, Tohidi Far (github.com/supermuesli)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.