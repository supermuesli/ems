# Energy Management System (EMS)

EMS is a primitive energy management system simulation that features energy providers, users, storages and P2X (power to x) components. For each component in the grid, the EMS decides which other component to consume in the next timestep by looking at the workload and proximity. 

This EMS delivers a **greedy energy** solution for a function *f* that tries to maximize the workload of each component. The running average workload per timestep in percent - called **equilibrium** - is featured on the middle right corner of the simulation UI. The higher the equilibrium, the better the energy solution for a given scenario.

![showcase](https://github.com/supermuesli/ems/blob/main/assets/images/showcase.gif)

## Controls
- hit **Arrow Up/Down** to increase or decrease the tickrate
- hit **Space** to pause or resume the simulation
- hit **Esc** to exit the simulation
- hit **Left/Right Mouse Click** to add/remove a cell to/from the grid

## Settings
The `assets` directory contains an example of a *grid setting* and a *scenario setting*. 

The grid dictates which components are located where on the grid, as well as information about the time-unspecific desired energy state.

The scenario dictates which components desire which energy state at which time.
