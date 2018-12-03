# Community Ecology Semester Project

## The Individual-Based Model

The model used here is modified from the [predatorpreywithplot.py](https://sourceforge.net/projects/pycx/files/PyCX-0.1/) file of the [PyCX Project](http://pycx.sourceforge.net/) compiled with Python 2.7.

The system modeled presents two species R, the resource and P, the predator. The system dynamics can be written as follows:

<p align="center">
dR/dt = r<sub>R</sub> ( 1 - R/K<sub>R</sub>) - &alpha;RP </p>
<p align="center">
dP/dt = r<sub>P</sub> ( 1 - P/K<sub>P</sub>) -m
</p>

With r<sub>R</sub> and r<sub>P</sub> the respective reproduction rate for the  K<sub>R</sub> and K<sub>P</sub> the carrying capacities of espectively the prey and predator. The term &alpha;RP corresponds to the predation term and m is the intrinsec mortality for the predator.

### Initialisation
The Individual-Based Model even though it ressembles the above described system is fondamentaly different because individuals are directly modelled on a spatially explicit 100x100 grid. All simulations are initialized placing all prey and predator individuals on the grid using an uniform distribution, ~ U<sup>2</sup> (0, max grid height) (0, max grid width).

### Model Structure
For each time step in the Individual-Based Model those actions are performed:
- All individuals disperse across the grid
- All possible predation events are resolved across the grid
- Dead individuals, from predation and background mortality, are removed from the grid
- All reproduction events are resolved

### Reproduction
The reproduction events are modelled by a random sampling between 0 and 1. The condition for a successfull reproduction event is:
<p align="center">r<sub>X</sub> ( 1 - X/K<sub>X</sub> ) > random</p>
With X being either the prey or predator.

### Predation
Predation events are defined by the variable called ```collisionDistance``` that sets the minimum distance for which predation can occur.
If the distance between a predator and a prey is less than the square of the value of ```collisionDistance``` a predation event occurs:
<p align="center">(x<sub>R</sub> - x<sub>P</sub>)<sup>2</sup> + (y<sub>R</sub> - y<sub>P</sub>)<sup>2</sup> < D</p>

with D = ```collisionDistance```<sup>2</sup>

### Dispersion of Individuals
Every individuals move according the a single parameter, ```NoiseLevel```, which corresponds to their dispersal ability. For each time step each individual moves from its current position with a value obtained from a gaussian distribution ~ N (O, ```NoiseLevel```). The borders of the grid are limiting: individuals moving beyond the maximum height and width are kept at the limits of the grid.










