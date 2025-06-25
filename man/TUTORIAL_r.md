# PhysiCell Data Loader Tutorial: pcdl and the R programming language

[R](https://cran.r-project.org/index.html) is a programming language for statistical computing,
which, because of its library collection, is very popular among bioinformatician.


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

### Load a csv file into an R DataFrame

Substrate concentration dataframe.

```R
df_conc <- read.csv("output/timeseries_conc.csv", row.names="index")
str(df_conc)
```
```R
colnames(df_conc)
```
```R
rownames(df_conc)
```

Cell agent attribute dataframe.

```R
df_cell <- read.csv("output/timeseries_cell.csv", row.names="index")
str(df_cell)
```
```R
colnames(df_cell)
```
```R
rownames(df_cell)
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

### Load json files into an R data construct

We will use the [jsonlite](https://cran.r-project.org/web/packages/jsonlite/index.html) library to load json files into R.
+ jsonlite publication: https://doi.org/10.48550/arXiv.1403.2805

Install jsonlite package.

```R
install.packages("jsonlite")
```

Load json file.

```R
library("jsonlite")
```
```R
l_conc <- read_json("output/timeseries_conc_attribute_minmax.json")
str(l_conc)
```
```R
l_cell <- read_json("output/timeseries_cell_attribute_minmax.json")
str(l_cell)
```


## &#x2728; Handle gml graph data files

### Save pcdl data structures as gml files from the command line

```bash
cd path/to/PhysiCell
```
```bash
pcdl_make_graph_gml output/output00000024.xml neighbor --node_attribute cell_type dead oxygen pressure
```

### Load gml files into an R data construct

We will use the [igraph](https://cran.r-project.org/web/packages/igraph/index.html) library to load gml files into R.
+ https://r.igraph.org/

Install igaph package.

```R
install.packages("igraph")
```

Load gml file.

```R
library("igraph")
```
```R
g <- read_graph("output/output00000024_neighbor.gml", format = c("gml"))
str(g)
```


## &#x2728; Handle h5ad single cell data files

### Save pcdl data structures as h5ad files from the command line

```bash
cd path/to/PhysiCell
```
```bash
pcdl_get_anndata output/
```

### AnnData, SingleCellExperiment and Seurat

We will use the [schard](https://github.com/cellgeni/schard) R package
to translate the h5ad file into R data structures that can be analyzed
by [singlecellexperiment](https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html)
and [seurat](https://satijalab.org/seurat/).

Special thanks to Marcello Hurtado from the Pancald Lab, who told me that such translation software exist!

#### Install the schard h5ad translator R package

```R
install.packages("devtools")
```
```R
devtools::install_github("cellgeni/schard")
```

Homepage:
+ https://github.com/cellgeni/schard

#### Data analysis with SingleCellExperiment R bioconductor package

Install the SingleCellExperiment software.

```R
install.packages("BiocManager")
BiocManager::install("SingleCellExperiment")
```

Translate the h5ad file to a sce R object

```R
cell.sce = schard::h5ad2sce("output/timeseries_cell_maxabs.h5ad")
str(cell.sce)
```

For how to analyse with singlecellexperiment, please study the official publication and documentation.

+ https://github.com/cellgeni/schard
+ https://pubmed.ncbi.nlm.nih.gov/31792435/
+ https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html

#### Data analysis with Seurat R package

Install the Seurat software.

```R
install.packages('Seurat')
```

Translate the h5ad file to a seurat compatible R objects

```R
cell.seurat = schard::h5ad2seurat("output/timeseries_cell_maxabs.h5ad")
str(cell.seurat)
```
```R
cell.seurat_spatial = schard::h5ad2seurat_spatial("output/timeseries_cell_maxabs.h5ad")
str(cell.seurat_spatial)
```

For how to analyze with seurat, please study the official documentation.

+ https://github.com/cellgeni/schard
+ https://satijalab.org/seurat/


That's it
