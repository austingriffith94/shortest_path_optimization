# shortest_path_optimization
Minimize the distance travelled across a series of nodes, with respective costs. Solves for variable edge congestions.

## Problem
Given a directed graph G = (V,E). Let s and t both exist on V. In this case, s is 0, and t is the final node value. The nominal travel time on a given edge (ij) is cij. If the edge fails (gets congested), then the travel time becomes cij + dij. There are at most L allowable simultaneous edge failures.

The goal is to minimize the worst-case travel cost from s to t. Vary L to observe its affect on the model.

## Theory
The theory and complete derivation of the model can be found [here.](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/derivation%20of%20model/derivation.pdf) If you want to see a full walkthrough of the code for the default data set, you can see check the jupyter folder in the repository, or check the pdf of notebook [here.](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/shortPath%20original%20data/shortPath%20nb.pdf)

## Solution
