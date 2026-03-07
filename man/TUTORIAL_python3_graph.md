# PhysiCell Data Loader Tutorial: pcdl and Python and Graphs

[Gml](https://github.com/elmbeech/physicelldataloader/blob/master/man/publication/himsolt1996gml_a_portable_graph_file_format.pdf) (graph modeling language) is a portable plain text file format for graphs,
that can be read by the popular graph libraries [networkx](https://networkx.org/) (python), [igraph](https://igraph.org/) (C, C++, mathematica, python, R) <!--, [JuliaGraphs](ttps://github.com/JuliaGraphs/GraphIO.jl)-->, and possible other graph analysis software too.

Pcdl can export neighborhood <!-- and lineage tree --> graphs in gml format for downstream analysis.

If you are new to graph theory, then I recommend reading [A Simple Introduction to Graph Theory](https://www.brianheinold.net/graph_theory/A_Simple_Introduction_to_Graph_Theory_Heinold.pdf)
from Prof. Brian Heinold from Mount Saint Mary's University in Emmitsburg, Maryland, USA.
This book will give you a solid  background in graph theory.
Besides, this book is an eye-opener, why and how mathematicians like to prove.


## pcdl: save a graph data into a gml file format from the command line

```bash
pcdl_make_graph_gml output/output00000024.xml neighbor --node_attribute cell_type dead oxygen pressure
```
```bash
pcdl_make_graph_gml output neighbor --node_attribute cell_type dead oxygen pressure
```
```bash
pcdl_make_graph_gml -h
```

## pcdl: save a graph data into a gml file format from within python

```python
import pcdl

mcdsts = pcdl.TimeSeries('output/')
```
```python
mcdsts.make_graph_gml('neighbor', node_attribute=['cell_type', 'dead', 'oxygen', 'pressure'])
```

## networkx: load a graph gml file

```python
import networkx as nx

g = nx.read_gml('output/output00000024_neighbor.gml')
print(g)
print(sorted(g.nodes.keys())[0:4])
print(sorted(g.edges.keys())[0:4])
```
```python
g.nodes['node_0']   # {'cell_type': 'default', 'dead': 0, 'oxygen': 25.304510426523084, 'pressure': 10.519314516003435}
```
```python
g.edges[('node_0', 'node_1')]   # {'label': 'edge_0_1', 'distance_microns': 15}
```


## igraph: load a graph gml file

```python
import igraph as ig

g = ig.Graph.Read_GML('output/output00000024_neighbor.gml')
print(g)
```
```python
ig.summary(g)
```


That's it. The rest is analysis!
