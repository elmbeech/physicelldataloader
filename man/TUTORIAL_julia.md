# PhysiCell Data Loader Tutorial: pcdl and the Julia language

[Julia](https://julialang.org/) is a scientific computing language.


## &#x2728; Run pcdl within Julia

We are using the [PyCall.js](https://github.com/JuliaPy/PyCall.jl) library
to run pcdl within Julia.

Make sure that the python3 environment is activated, which has pcdl installed.

Fire up a Juila shell.
```bash
julia
```

Pakage installation.

```julia
using Pkg
Pkdg.add("PyCall")
```

Run pcdl.

```julia
using PyCall

pcdl = pyimport("pcdl")  # import the pcdl module.
mcdsts = pcdl.TimeSeries("path/to/PhysiCell/output/")  # load an mcds time series.

?mcdsts.get_cell_df()  # retrieve a function's docstring.
df = mcdsts.get_cell_df()  # retrieve the cell dataframe.
```

## &#x2728; Handle csv files

### Save pcdl data structures as csv files from the command line

```bash
cd path/to/PhysiCell
```
```bash
pcdl_get_conc_df output
```
```bash
pcdl_get_cell_df output
```

### Load a csv file into jula data structures

We are using the [DataFrames.js](https://dataframes.juliadata.org/stable/) library,
to load the csv files.

Package installation.

```julia
using Pkg
Pkdg.add("CSV")
Pkdg.add("DataFrames")
```

Load csv into a dataframe.

```julia
using CSV
using DataFrames
```
```julia
df_cell = CSV.File("output/timeseries_cell.csv") |> DataFrame
```
```julia
df_conc = CSV.File("output/timeseries_cell.csv") |> DataFrame
```


## &#x2728; Handle json files

### Save pcdl data structures as json files from the command line

```bash
cd path/to/PhysiCell
```
```bash
pcdl_get_conc_attribute output 2
```
```bash
pcdl_get_cell_attribute output 2
```

### Load json files into a julia data structures

We are using the [JSON3.js](https://github.com/quinnj/JSON3.jl) library,
to load the json files.

Package installation.

```julia
using Pkg
Pkg.add("JSON3")
```

Load json.

```julia
using JSON3
```
```julia
json_string = read("output/timeseries_conc_attribute_minmax.json", String)
j_conc = JSON3.read(json_string)
```
```julia
json_string = read("output/timeseries_cell_attribute_minmax.json", String)
j_cell = JSON3.read(json_string)
```


## &#x2728; Handle gml graph files

### Save pcdl data structures as gml files from the command line

```bash
cd path/to/PhysiCell
```
```bash
pcdl_make_graph_gml output/output00000024.xml neighbor --node_attribute cell_type dead oxygen pressure
```

### Load gml files into a julia data structures

&#x26A0; **bue 2024-09-04:** this is currently not working, since, for now, GraphIO cannot handle the graph, node, or edge metadata in the file ( https://github.com/JuliaGraphs/GraphIO.jl/issues/46 ).

We will use the [GraphIO.js](https://github.com/JuliaGraphs/GraphIO.jl) library,
to load gml files.

Package installation.

```julia
using Pkg
Pkg.add("GraphIO")
Pkg.add("Graphs")
Pkg.add("ParserCombinator")
```

Load gml.

```julia
using GraphIO
using Graphs
using ParserCombinator
```
```julia
graph = loadgraph("output/output00000024_neighbor.gml", GraphIO.GML.GMLFormat())
```

Please study the Graphs documentation to learn how to analyze graph data.

+ https://github.com/JuliaGraphs/Graphs.jl
+ https://juliagraphs.org/Graphs.jl/stable/


## &#x2728; Handle h5ad single cell data files

### Save pcdl data structures as h5ad files from the command line

```bash
cd path/to/PhysiCell
```
```bash
pcdl_get_anndata output/
```

### Load h5ad files into a julia data structures

We will use scverse's [Muon.jl](https://github.com/scverse/Muon.jl) library,
to load h5ad files.

Package installation.

```julia
using Pkg
Pkg.add("Muon")
```

Load h5ad.

```julia
using Muon
```
```julia
adata = readh5ad("output/timeseries_cell_maxabs.h5ad")
```

Please study the Muon and AnnData documentation to learn how to analyze this data.
+ https://github.com/scverse/Muon.jl/tree/main
+ https://github.com/scverse/anndata


## &#x2728; Handle ome.tiff, tiff, png, and jpeg file format

### Save pcdl data structures as jpeg, png, tiff, and ome.tiff files from the command line

```bash
pcdl_plot_contour output/output00000021.xml oxygen --ext tiff
```
```bash
pcdl_plot_contour output/output00000021.xml oxygen
```
```bash
pcdl_plot_scatter output/output00000021.xml
```
```bash
pcdl_make_ome_tiff('output/')
```

### Load jpeg, png, tiff, and ometiff files into a julia data structures

&#x26A0; **bue 2024-09-04:** ome.tiff files currently cannot be loaded ( github issue: https://github.com/tlnagy/OMETIFF.jl/issues/112 ).

We will use the [Images](https://github.com/JuliaImages/Images.jl) library, and it's [OMETIFF](https://github.com/tlnagy/OMETIFF.jl) extension,
to load jpeg, png, tiff, and ome.tiff files

Package installation.

```julia
using Pkg
Pkg.add("FileIO")
Pkg.add("Images")
Pkg.add("OMETIFF")
```

Load image file.

```julia
using FileIO
```
```julia
omeimg = load("output/timeseries_ID.ome.tiff")
```
```julia
img = load("output/cell_cell_type_z0.0/output00000021_cell_type.jpeg")
```

<!--
## &#x2728; Handle vtk rectiliniar grid and polynomial data files

Package installation.

```julia
using Pkg
Pkg.add("ReadVTK")
```

Try to load vtk rectiliniar grid file (vtr) and polynomial data file (vtp).

```julia
using ReadVTK
```
```julia
vr_conc = VTKFile("output/output00000021_conc.vtr")
```
```julia
vp_cell = VTKFile("output/output00000021_cell.vtp")
```

bue 20240904: fails with ERROR: AssertionError: header_type == "UInt64".
at their homepage under what does not work is written: probably reading from vtk files that were not created by WriteVTK.jl will fail.
does not sound to me like this will work any time in the near future. so I will leave it there.

+ https://github.com/JuliaVTK/ReadVTK.jl
-->

That's it!
