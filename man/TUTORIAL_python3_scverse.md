# PhysiCell Data Loader Tutorial: pcdl and Python and the scVerse

[AnnData](https://anndata.readthedocs.io/en/latest/) is the data standard from the python single cell community.
This means, PhysiCell output transformed into an AnnData object can be analyzed the same way  sc RNA seq data is analyzed.
The whole [scverse](https://scverse.org/) (single cell univers)  becomes accessible.

This includes:
+ [scanpy](https://scanpy.readthedocs.io/en/latest/): for classic single cell analysis.
+ [squidpy](https://squidpy.readthedocs.io/en/stable/): for spatial single cell analysis.
+ [scvi-tools](https://scvi-tools.org/): for single cell machine learning.
+ [muon](https://muon.readthedocs.io/en/latest/): for multimodal omics analysis.
And there is a whole [ecosystem](https://scverse.org/packages/#ecosystem) of libraries, compatible with the AnnData format.

Whatever you d'like to do with your physicell data, it most probably was already done with single cell wet lab data.
That's being said: PhysiCell data is different scdata than scRNA seq data!
For example, scRNA seq data is higher dimensional (e.g. the human genome has over 20000 genes each time step) than PhysiCell data (tens, maybe hundreds of cell attributes).
For example, scRNA seq data is always single time step data because the measurement consumes the sample. PhysiCell data is always time series data, even we look at this moment only at one time step.
This means, the wet lab bioinformatics will partially try to solve problems (for example trajectory inference), that simply are no problems for us and the other way around.
Anyhow, there are a lot of scRNA seq data analysis methods around, which make sense to apply to both of these data types.

For the shake of demonstration, let's do a classic scRNA seq analysis.


## Preparation

Let's install the required analysis libraries
```bash
pip3 install -U scanpy[leiden]  # single cell analysis inclusive leiden graph clustering algorithm.
```

To runs this tutorial,
you can install the 3D unit test dataset into your PhysiCell output folder,
by executing the following command sequence.

&#x26A0; **Warning: all data currently in your PhysiCell/output folder will be overwritten!**

```bash
cd path/to/PhysiCell
```
```bash
make data-cleanup
python3 -c"import pathlib, pcdl, shutil; pcdl.install_data(); s_ipath=str(pathlib.Path(pcdl.__file__).parent.resolve()/'output_3d'); shutil.copytree(s_ipath, 'output', dirs_exist_ok=True)"
```


## Analysis

Load the libraries.

```python
# library
import anndata as ad  # from the scverse
import pcdl
import scanpy as sc  # from the scverse

# versions
print('pcdl version:', pcdl.__version__)
print(sc.logging.print_header())
```

Load the data.

```python
mcdsts = pcdl.TimeSeries('output/')
adata = mcdsts.get_anndata(values=2, scale='maxabs', collapse=True)
print(adata)
```

Let's do an interactive data analysis.\
Please note, sub-library abbreviations used in the scanpy and squidpy library are:

+ gr: graph
+ im: image
+ pl: plotting
+ pp: preprocessing
+ tl: tools

Principal component analysis:

```python
sc.tl.pca(adata)  # process anndata object with the pca tool.
sc.pl.pca(adata)  # plot pca result.
```
```python
sc.pl.pca(adata, color=['current_phase','oxygen'])  # plot the pca results colored by some attributes.
```
```python
sc.pl.pca_variance_ratio(adata)  # plot how much of the variation each principal component captures.
```

Neighborhood graph clustering:

```python
sc.pp.neighbors(adata, n_neighbors=15)  # compute the neighborhood graph with the neighbors preprocess step.
sc.tl.leiden(adata, resolution=0.01)  # cluster the neighborhood graph with the leiden tool.
sc.pl.pca(adata, color='leiden')  # plot the pca results colored by leiden clusters.
```
<!--
#```python
# leiden cluster cell_type mapping
d_leiden = {
#    0: 'differentiated',
#    1: 'stem',
#    2: 'neutrophil',
#    3: 'CD8+_T_cell',
#    4: 'macrophage',
#    5: 'bacteria_a',
#    6: 'blood_vessel',
#    7: 'bacteria_b',
#}
#ls_label = [s_label for _, s_label in sorted(d_leiden.items())]
#ann.rename_categories('leiden', ls_label)
#
#```python
#import seaborn as sns
#sc.metrics.confusion_matrix("cell_type", "leiden", ann.obs)  # pandas dataframe
#ax = sns.heatmap(sc.metrics.confusion_matrix("cell_type", "leiden", ann.obs), cmap='viridis')
#ax.set_title('cell type leiden cluster confusion matrix')
#```
-->

T-sne dimensional reduction embedding:

```python
sc.tl.tsne(adata)  # process anndata object with the tsne tool.
sc.pl.tsne(adata, color=['current_phase','cell_type','leiden'])  # plot the tsne result colored by some attributes.
```

Umap dimensional reduction embedding:

```python
sc.tl.umap(adata)  # process anndata object with the umap tool.
sc.pl.umap(adata, color=['current_phase','oxygen','leiden'])  # plot the umap result colored by some attributes.
sc.pl.umap(ann, save='interaction_16200min_umap.png')  # plot is saved to figures directory.
```

Save anndata object:

```python
# save and load anndata objects
adata.write(f'output/timeseries.h5ad')
```

Load the anndata object (just for fun):

```python
adata = ad.read(f'output/timeseries.h5ad')
print(adata)
```

That's it. Please check out the official scverse documentation to learn more.


## Data Clean Up

After you are done checking out the 3D unit test dataset,
you can uninstall the datasets and remove the data in the output folder,
by executing the following command sequence.

```bash
python3 -c"import pcdl; pcdl.uninstall_data()"
make data-cleanup
```
