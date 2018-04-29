# shortest_path_optimization
Minimize the distance travelled across a series of nodes, with respective costs. Solves for variable edge congestions.

## Problem
Given a directed graph G = (V,E). Let s and t both exist on V. In this case, s is 0, and t is the final node value. The nominal travel time on a given edge (ij) is cij. If the edge fails (gets congested), then the travel time becomes cij + dij. There are at most L allowable simultaneous edge failures.

The goal is to minimize the worst-case travel cost from s to t. Vary L to observe its affect on the model.

## Theory
The theory and complete derivation of the model can be found [here.](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/derivation%20of%20model/derivation.pdf) If you want to see a full walkthrough of the code for the default data set, you can see check the jupyter folder in the repository, or check the pdf of notebook [here.](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/shortPath%20original%20data/shortPath%20nb.pdf)

## Solution
The output for the original set of data shows the effect of allowable edge failures on the management of the the worst-case shortest path. We can see diminishing available optimal paths as the edge failures increase. The difference between no allowable simultaneous failures, and 1 simultaneous failure has the largest increase in the objective value. This should be expected, as the cost of congestion is much larger than the cost of normal movement. Thus, once a congested edge is made to be accounted for on the path, the optimal objective value is drastically increased, by several orders of magnitude. As the edge failures increase, the optimal objective is impacted less, as the extra cost of congestion can be mitigated. We can observe the paths in the following network graphs, with respect to increasing edge failures.

![gamma 1](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/shortPath%20original%20data/output_10_2.png "gamma 1")

![gamma 2](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/shortPath%20original%20data/output_10_5.png "gamma 2")

![gamma 3](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/shortPath%20original%20data/output_10_8.png "gamma 3")

![gamma 4](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/shortPath%20original%20data/output_10_11.png "gamma 4")

![gamma 5](https://github.com/austingriffith94/shortest_path_optimization/blob/master/LaTeX/shortPath%20original%20data/output_10_14.png "gamma 5")
