# Austin Griffith
# Python 3.6.5
# 4/25/2018

import pandas as pd
import numpy as np
from gurobipy import *
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import networkx as nx

#%%
# pull data
edges = pd.read_csv('edge_data.csv')

# create dictionaries of edge values
c = {}
d = {}
nodes = tuplelist()
for i in edges.index:
    c[edges['i'][i],edges['j'][i]] = edges['c(ij)'][i]
    d[edges['i'][i],edges['j'][i]] = edges['d(ij)'][i]
    nodes.append((edges['i'][i],edges['j'][i]))

maxNodes = max(edges['j'])
minNodes = min(edges['i'])

#%%
# choose start and end nodes
start = 0
end = 49

# allowed edge congestions
gend = 4
gammas = np.linspace(0,gend,gend+1)
g = gammas[0]

#%%
# initialize model
model = Model('Shortest_Path')

# set up x binary variables, set to each location/movement
xVars = model.addVars(nodes, vtype=GRB.BINARY, name='move')
y0 = model.addVar(vtype=GRB.CONTINUOUS, name='y0')
zVars = model.addVars(nodes, lb=0.0, vtype=GRB.CONTINUOUS, name='cong')
model.update()

#%%
# gather all entrance and exit nodes
enterStart = []
leaveStart = []
enterEnd = []
leaveEnd = []
for n in nodes:
    # for start nodes
    if n[0] == start:
        leaveStart.append(xVars[n])
    elif n[1] == start:
        enterStart.append(xVars[n])
    # for end nodes
    if n[0] == end:
        leaveEnd.append(xVars[n])
    elif n[1] == end:
        enterEnd.append(xVars[n])

model.addConstr(quicksum(leaveStart) == 1)
model.addConstr(quicksum(enterStart) == 0)
model.addConstr(quicksum(leaveEnd) == 0)
model.addConstr(quicksum(enterEnd) == 1)
model.update()

#%%
# gather all paths
paths = []
for i in range(minNodes+1,maxNodes):
    pathFrom = []
    pathTo = []
    for n in nodes:
        if n[0] == i:
            pathFrom.append(xVars[n])
        elif n[1] == i:
            pathTo.append(xVars[n])
    paths.append([pathFrom,pathTo])
model.update()

for p in paths:
    model.addConstr(quicksum(p[0]) - quicksum(p[1]) == 0.0)
model.update()

#%%
# get objective function
costObj = []
for n in nodes:
    costObj.append(xVars[n]*c[n])
    model.addConstr(zVars[n] >= xVars[n]*d[n] - y0)
model.update()

#%%
output = []
for g in gammas:
    # optimize
    objective = quicksum(costObj) + g*y0 + quicksum(zVars)
    model.setObjective(objective, GRB.MINIMIZE)

    model.optimize()

    # order the printout of optimal edges
    moves = []
    for m in xVars:
        if xVars[m].x != 0:
            moves.append(m)
    order = [moves[0]]
    for i in range(len(moves)):
        for m in moves:
            if order[i][1] == m[0]:
                order.append(m)
    output.append([g,order,model.objVal])

#%%
# print optimal values and paths
for o in output:
    print('\nFor Gamma: '+str(o[0]))
    print('Path:')
    print(o[1])
    print('Cost of Movement (Objective):')
    print(o[2])
    networkCompletePlot(o,maxNodes)
    networkPathPlot(o,maxNodes,c)

#%%
# set up plotting parameters
params = {'legend.fontsize': 20,
          'figure.figsize': (13,9),
         'axes.labelsize': 20,
         'axes.titlesize':25,
         'xtick.labelsize':15,
         'ytick.labelsize':15}
pylab.rcParams.update(params)
#%%
# graph all nodes
def networkCompletePlot(solution,maxNode):
    G = nx.DiGraph()
    G.add_nodes_from(range(0,maxNode+1))
    for i,j in nodes:
        G.add_edge(i,j)

    # get solution nodes
    sp = [i for i,j in solution[1]]
    sp.append(end)

    colorNode = ['white' if not node in sp else 'red' for node in G.nodes()]
    nx.draw_networkx(G,node_color=colorNode,node_size=200)
    plt.axis('off')
    plt.show()

# graph path, with cost on edge
def networkPathPlot(solution,maxNode,cost):
    # get solution nodes
    sp = [i for i,j in solution[1]]
    sp.append(end)

    # set up random position values
    a = np.arange(maxNode+1)
    b = np.arange(maxNode+1)
    np.random.shuffle(a)
    posArray = np.array([a,b]).transpose()

    positions = {}
    for p in range(0,len(sp)):
        L = posArray[p]
        positions[sp[p]] = (L[0],L[1])

    # set up network graph
    G = nx.DiGraph()
    G.add_nodes_from(sp)

    for i,j in tuplelist(solution[1]):
        G.add_edge(i,j)

    labels = {}
    for i in solution[1]:
        labels[i] = round(c[i],3)

    nx.draw_networkx(G,positions,node_size=250)
    nx.draw_networkx_edge_labels(G,positions,edge_labels=labels)
    plt.axis('off')
    plt.show()

#%%
# graph all nodes
solution = output[0]

G = nx.DiGraph()
G.add_nodes_from(range(minNodes,maxNodes+1))
for i,j in nodes:
    G.add_edge(i,j)

# set up random position values
a = np.arange(maxNodes+1)
b = np.arange(maxNodes+1)
np.random.shuffle(a)
posArray = np.array([a,b]).transpose()

positions = {}
for p in range(0,maxNodes+1):
    L = posArray[p]
    positions[p] = (L[0],L[1])

# get solution nodes
sp = [i for i,j in solution[1]]
sp.append(end)

colorNode = ['white' if not node in sp else 'red' for node in G.nodes()]
colorEdge = ['black' if not edge in solution[1] else 'red' for edge in G.edges()]

nx.draw_networkx(G,positions,node_color=colorNode,node_size=200)
nx.draw_networkx_edges(G,positions,edge_color=colorEdge)
plt.axis('off')
plt.show()

#%%
# set up random position values
a = np.arange(maxNodes+1)
b = np.arange(maxNodes+1)
np.random.shuffle(a)
posArray = np.array([a,b]).transpose()

positions = {}
for p in range(0,len(sp)):
    L = posArray[p]
    positions[sp[p]] = (L[0],L[1])

# set up network graph
G = nx.DiGraph()
G.add_nodes_from(sp)

for i,j in tuplelist(solution[1]):
    G.add_edge(i,j)

labels = {}
for i in solution[1]:
    labels[i] = round(c[i],3)

nx.draw_networkx(G,positions,node_size=250)
nx.draw_networkx_edge_labels(G,positions,edge_labels=labels)
plt.axis('off')
plt.show()




