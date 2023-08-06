# pymhopt: Python Wrapper for Optimization Algorithms 

This Python 3 code provides wrapper for symbolic regression providing two implementations a) Genetic Programming with symbolic regression b) multi-objective genetic programming using NSGA-II (https://ieeexplore.ieee.org/document/996017).

## Dependencies
pandas; numpy; scikit-learn; gplearn; graphviz.

## Installation
Run `pip install pymhopt` 

## Example 
See `test.py` for an example. 

## Acknowledgements & Credits

* The gplearn module is used as base for symbolic expression and genetic programming evaluations. (https://gplearn.readthedocs.io/en/stable/)
* The nsga-II algorithm is adapted from [marcovirgolin repo](https://github.com/marcovirgolin/pyNSGP/).
* A fast and elitist multiobjective genetic algorithm: NSGA-II (https://ieeexplore.ieee.org/document/996017)

Note:- This package is still under development & WORK IN PROGRESS, I will aim to cover a bunch of different meta-heuristics optimization algorithms.





