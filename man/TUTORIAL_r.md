# PhysiCell Data Loader Tutorial: pcdl and the R programming language

[R](https://cran.r-project.org/index.html) is a programming language for statistical computing,
which, because of its library collection, is very popular among bioinformatician.


## &#x2728; Run pcdl within R

We are using the [reticulate](https://github.com/rstudio/reticulate) library
to run pcdl within R.

Make sure that the python3 environment is activated, which has pcdl installed.

Fire up an R shell.
```bash
R
```

Package installation.

```R
install.packages("reticulate")
```

Run pcdl.

```R
library("reticulate")

pcdl <- import("pcdl")  # import the pcdl module.
mcdsts <- pcdl$TimeSeries("path/to/PhysiCell/output/")  # load an mcds time series.

py_help(mcdsts$get_cell_df)  # retrieve a function's docstring.
df <- mcdsts$get_cell_df()  # retrieve the cell dataframe.
str(df)
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
or the [SeuratDisk](https://github.com/mojaveazure/seurat-disk) R package
to translate the h5ad file into R data structures that can be analyzed
by [singlecellexperiment](https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html)
and [seurat](https://satijalab.org/seurat/).

Special thanks to Marcello Hurtado from the Pancald Lab, who told me that such translation software exist!

#### Install the schard h5ad translator R package

```R
install.packages("devtools")
```

Install the schard package.

```R
library("devtools")
devtools::install_github("cellgeni/schard")
```

Install the SeuratDisk package.

```R
library("devtools")
devtools::install_github("mojaveazure/seurat-disk")
```

Homepaged:
+ https://github.com/cellgeni/schard
+ https://github.com/mojaveazure/seurat-disk
+ https://mojaveazure.github.io/seurat-disk/articles/convert-anndata.html


#### Data analysis with SingleCellExperiment R bioconductor package

Install the SingleCellExperiment software.

```R
install.packages("BiocManager")
BiocManager::install("SingleCellExperiment")
```

Translate the h5ad file to a sce R object by shard.

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

Translate the h5ad file to a seurat compatible R objects by schard.

```R
library("schard")
```
```R
cell.seurat = schard::h5ad2seurat("output/timeseries_cell_maxabs.h5ad")
str(cell.seurat)
```
```R
cell.seurat_spatial = schard::h5ad2seurat_spatial("output/timeseries_cell_maxabs.h5ad")
str(cell.seurat_spatial)
```

Or translate the h5ad file to a seurat compatible R objects by SeuratDisk.

```R
library("SeuratDisk")
```
```R
SeuratDisk::Convert("output/timeseries_cell_maxabs.h5ad", dest="h5seurat", overwrite=TRUE)
cell.seurat_disk <- SeuratDisk::LoadH5Seurat("output/timeseries_cell_maxabs.h5seurat")
```

For how to analyze with seurat, please study the official documentation.
+ https://github.com/cellgeni/schard
+ https://github.com/mojaveazure/seurat-disk
+ https://mojaveazure.github.io/seurat-disk/articles/convert-anndata.html
+ https://satijalab.org/seurat/


## &#x2728; Handle ome.tiff, tiff, png, and jpeg file format

### Save pcdl data structures as jpeg, png, tiff, and ome.tiff files from the command line

```bash
pcdl_plot_timeseries output/ --ext jpeg
```
```bash
pcdl_plot_timeseries output/ --ext png
```
```bash
pcdl_plot_timeseries output/ --ext tiff
```
```bash
pcdl_make_ome_tiff('output/')
```


### Load jpeg, png, tiff, and ometiff files into a R data structures

We will use the [jpeg](https://cran.r-project.org/web/packages/jpeg/index.html), [png](https://cran.r-project.org/web/packages/png/index.html), [tiff](https://cran.r-project.org/web/packages/tiff/index.html) and [RBioFormats](https://bioconductor.org/packages/release/bioc/vignettes/RBioFormats/inst/doc/RBioFormats.html) libraries to load this images into R.

#### Jpeg images

Install the required R package.

```R
install.packages("jpeg")
```

Load the image.

```R
library("jpeg")
img <- readJPEG("output/timeseries_cell_total_count.jpeg")
str(img)
```

#### Png images

Install the required R package.

```R
install.packages("png")
```

Load the image.

```R
library("png")
img <- readPNG("output/timeseries_cell_total_count.png")
str(img)
```

#### Tiff images

Install the required R package.

```R
install.packages("tiff")
```

Load the image.

```R
library("tiff")
img <- readTIFF("output/timeseries_cell_total_count.tiff")
str(img)
```

#### Ome.tiff images

Install the required R package.

```R
install.packages("BiocManager")
BiocManager::install("RBioFormats")
```

Load the image.

```R
library("RBioFormats")
omeimg <- read.image(""output/timeseries_ID.ome.tiff"")
str(img)
```


That's it
