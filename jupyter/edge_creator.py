import numpy as np
import pandas as pd

# number of nodes
s = 90
# number of missing paths from each node (thins edges)
minus = 50

edgevalues = pd.DataFrame()
for i in range(0,s+1):
    rand = int(np.random.rand(1)*minus)
    a = np.int64(np.ones(s-rand)*i)
    b = np.int64(np.arange(s)[rand:s])
    np.random.shuffle(b)
    c = np.random.rand(s-rand)
    d = np.random.rand(s-rand)*5
    coord = pd.DataFrame([a,b,c,d]).transpose()
    edgevalues = pd.concat([edgevalues,coord])
edgevalues.columns = ['i','j','c(ij)','d(ij)']
edgevalues = edgevalues.set_index('i')
edgevalues.to_csv('edge_values.csv')
