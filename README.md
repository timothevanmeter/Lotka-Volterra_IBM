# Community Ecology Semester Project

## The Individual-Based Model

The model used here is modified from the [predatorpreywithplot.py](https://sourceforge.net/projects/pycx/files/PyCX-0.1/) file of the [PyCX Project](http://pycx.sourceforge.net/) compiled with Python 2.7.

The system modeled presents two species R, the resource and P, the predator. The system dynamics can be written as follows:

- dR/dt = r<sub>R</sub> ( 1 - R/K<sub>R</sub>) - &alpha;RP
- dP/dt = r<sub>P</sub> ( 1 - P/K<sub>P</sub>) -m

With K<sub>R</sub> and K<sub>P</sub> the carrying capacities of espectively the prey and predator. The term &alpha;RP corresponds to the predation term and m is the intrinsec mortality for the predator.

The Individual-Based Model even though it ressembles the above described system is fondamentaly different because individuals are directly modelled on a spatially explicit 100x100 grid. All simulations are initialized placing all prey and predator individuals on the grid using an uniform distribution, ~ U (0, max grid height)(0, max grid width).

$$  X_{bitch}  $$


