# PhysiCell Data Loader Tutorial: pcdl from the Commandline

The most important commands for down stream data analysis,
available in the pcdl TimeStep and TimeSeries class,
can be run straight from a command line shell, like [bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)), [csh](https://en.wikipedia.org/wiki/C_shell), [dos](https://en.wikipedia.org/wiki/DOS), [fish](https://en.wikipedia.org/wiki/Fish_(Unix_shell)), [ksh](https://en.wikipedia.org/wiki/KornShell), [powershell](https://en.wikipedia.org/wiki/PowerShell), [sh](https://en.wikipedia.org/wiki/Bourne_shell), [tsh](https://en.wikipedia.org/wiki/Tcsh), or [zsh](https://en.wikipedia.org/wiki/Z_shell), to name a view.

The command names are derived from the related python3 function. \
The command parameter mimics the related python3 function arguments as closely as possible. \
You can always call the [help](https://en.wikipedia.org/wiki/Help!) parameter ( pcdl\_command -h),
to access the man page for a pcdl command!

Please spend some time to learn about each of the about 20 commands, by studying its man page.
This will truly make you a power user!


## Preparation

To runs this tutorial,
you can install the 2D unit test dataset into your PhysiCell output folder,
by executing the following command sequence.

&#x26A0; **Warning: all data currently in your PhysiCell/output folder will be overwritten!**

```bash
cd path/to/PhysiCell
```
```bash
make data-cleanup
python3 -c"import pathlib, pcdl, shutil; pcdl.install_data(); s_ipath=str(pathlib.Path(pcdl.__file__).parent.resolve()/'output_2d'); shutil.copytree(s_ipath, 'output', dirs_exist_ok=True)"
```


## Metadata related commands

### &#x2728; pcdl\_get\_version

Outputs PhysiCell, MCDS, and pcdl version on screen.

```bash
pcdl_get_version output
```
```bash
pcdl_get_version output/output00000000.xml
```
```bash
pcdl_get_version -h
```

### &#x2728; pcdl\_get\_unit\_dict

Generate a [csv](https://en.wikipedia.org/wiki/Comma-separated_values) file that maps attribute and units, as specified in the settings.xml.

```bash
pcdl_get_unit_dict output
```
```bash
pcdl_get_unit_dict output/output00000000.xml
```
```bash
pcdl_get_unit_dict -h
```


## Microenvironment related commands

### &#x2728; pcdl\_get\_substrate\_list

Outputs all substrates modeled in the microenvironment on screen.

```bash
pcdl_get_substrate_list output
```
```bash
pcdl_get_substrate_list output/output00000000.xml
```
```bash
pcdl_get_substrate_list -h
```

### &#x2728; pcdl\_get\_conc\_attribute

Generate a [json](https://en.wikipedia.org/wiki/JSON) file, that lists all substrate attributes.
For each such attribute the min and the max value are listed.

In the example below:
+ all substrates attributes are listed, that over the whole time series have at least 2 diffrent values.
+ all substrates attributes are listed, that in this particular time step have at least 2 different values.

```bash
pcdl_get_conc_attribute output 2
```
```bash
pcdl_get_conc_attribute output/output00000000.xml 2
```
```bash
pcdl_get_conc_attribute -h
```

Further readings:
+ [TUTORIAL_python3_json.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_json.md)
+ [TUTORIAL_r.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_r.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)

### &#x2728; pcdl\_get\_conc\_df

Generate a dataframe [csv](https://en.wikipedia.org/wiki/Comma-separated_values) file that lists one voxel per row,
all substrate concentrations.

In the example below, the generated csv contains:
+ all substrate concentration values over the whole time series.
+ all substrate that within this particular time step have more than 2 different concentration values.

```bash
pcdl_get_conc_df output
```
```bash
pcdl_get_conc_df output/output00000000.xml 2
```
```bash
pcdl_get_conc_df -h
```

Further readings:
+ [TUTORIAL_python3_pandas.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_pandas.md)
+ [TUTORIAL_r.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_r.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)

### &#x2728; pcdl\_plot\_contour

For oxygen generate a [jpeg](https://en.wikipedia.org/wiki/JPEG) file
for a single time step or for each time step in the whole time series.

```bash
pcdl_plot_contour output oxygen
```
```bash
pcdl_plot_contour output/output00000000.xml oxygen
```
```bash
pcdl_plot_contour -h
```

### &#x2728; pcdl\_make\_conc\_vtk

Generate a rectilinear grid [vtk](https://en.wikipedia.org/wiki/VTK) file from a single time step,
or rectilinear grid vtk files from the whole time series,
containing all the substrates from the model.

These vtk files can be further analyzed,
for example with the [paraview](https://www.paraview.org/) or [blender](https://www.blender.org/) software,
as described in the extra tutorials.

```bash
pcdl_make_conc_vtk output
```
```bash
pcdl_make_conc_vtk output/output00000000.xml
```
```bash
pcdl_make_conc_vtk -h
```

Further readings:
+ [TUTORIAL_blender.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_blender.md)
+ [TUTORIAL_paraview.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_paraview.md)
+ [TUTORIAL_python3_vtk.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_vtk.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)


## Cell agent related commands

### &#x2728; pcdl\_get\_celltype\_list

Output all cell types modeled.

```bash
pcdl_get_celltype_list output
```
```bash
pcdl_get_celltype_list output/output00000000.xml
```
```bash
pcdl_get_celltype_list -h
```

### &#x2728; pcdl\_get\_cell\_attrribute\_list

Output all recorded cell attributes.

```bash
pcdl_get_cell_attribute_list output
```
```bash
pcdl_get_cell_attribute_list output/output00000000.xml
```
```bash
pcdl_get_cell_attribute_list -h
```

### &#x2728; pcdl\_get\_cell\_attribute

Generate a [json](https://en.wikipedia.org/wiki/JSON) file, that lists all cell attributes.
For each such attribute, the min and the max value are listed.

In the example below:
+ all cell attributes are listed, that over the whole time series have at least 2 different values.
+ all cell attributes are listed, that in this particular time step have at least 2 different values.

```bash
pcdl_get_cell_attribute output 2
```
```bash
pcdl_get_cell_attribute output/output00000000.xml 2
```
```bash
pcdl_get_cell_attribute -h
```

Further readings:
+ [TUTORIAL_python3_json.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_json.md)
+ [TUTORIAL_r.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_r.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)

### &#x2728; pcdl\_get\_cell\_df

Generate a dataframe [csv](https://en.wikipedia.org/wiki/Comma-separated_values) file that lists one cell per row,
all attributes.

In the example below, the generated csv contains:
+ all cell attributes, that over the whole time series have more than 2 different values.
+ from that particular time step all cell attributes available.

```bash
pcdl_get_cell_df output 2
```
```bash
pcdl_get_cell_df output/output00000000.xml
```
```bash
pcdl_get_cell_df -h
```

Further readings:
+ [TUTORIAL_python3_pandas.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_pandas.md)
+ [TUTORIAL_r.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_r.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)

### &#x2728; pcdl\_get\_anndata

From the whole time series or from a single time step, generate h5ad [anndata](https://anndata.readthedocs.io/en/latest/) [hd5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) files.

Anndata is the standard data format in the python single cell community.
Data stored in this format can be analyzed the same way as usually sc RNA seq data is analyzed.

```bash
pcdl_get_anndata output/output00000000.xml
```
```bash
pcdl_get_anndata output
```
```bash
pcdl_get_anndata -h
```

Further readings:
+ [TUTORIAL_python3_scverse.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_scverse.md)
+ [TUTORIAL_r.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_r.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)

### &#x2728; pcdl\_make\_graph\_gml

Generate [gml](https://github.com/elmbeech/physicelldataloader/blob/master/man/publication/himsolt1996gml_a_portable_graph_file_format.pdf) files.
One gml file per time step.

Gml files can be read by graph analysis libraries like [networkx](https://networkx.org/) and [igraph](https://igraph.org/).

```bash
pcdl_make_graph_gml output/output00000000.xml --node_attribute cell_type dead oxygen pressure
```
```bash
pcdl_make_graph_gml output
```
```bash
pcdl_make_graph_gml -h
```

Further readings:
+ [TUTORIAL_python3_graph.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_graph.md)
+ [TUTORIAL_r.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_r.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)

### &#x2728; pcdl\_plot\_scatter

Generate a [jpeg](https://en.wikipedia.org/wiki/JPEG) file that displaying all cells.

In the example below:
+ generate plots for the whole time series, color the cells by cell\_type.
+ generate a plot for a single time step, color the cells by pressure.

```bash
pcdl_plot_scatter output/output00000000.xml pressure
```
```bash
pcdl_plot_scatter output
```
```bash
pcdl_plot_scatter -h
```

### &#x2728; pcdl\_make\_cell\_vtk

Generate a 3D glyph [vtk](https://en.wikipedia.org/wiki/VTK) file from a single time step,
or rectilinear grid vtk files from the whole time series,
with information for the attributes listed.
The default attribute listed is cell\_type.

These vtk files can be further analyzed,
for example with the [paraview](https://www.paraview.org/) or [blender](https://www.blender.org/) software,
as described in the extra tutorials.

```bash
pcdl_make_cell_vtk output/output00000000.xml cell_type dead oxygen pressure
```
```bash
pcdl_make_cell_vtk output
```
```bash
pcdl_make_cell_vtk -h
```

Further readings:
+ [TUTORIAL_blender.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_blender.md)
+ [TUTORIAL_paraview.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_paraview.md)
+ [TUTORIAL_python3_vtk.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_vtk.md)
+ [TUTORIAL_julia.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_julia.md)


## Microenvironment and cell agent related commands

### &#x2728; pcdl\_get\_spatialdata

From a single time step, generate [spatialdata](https://spatialdata.scverse.org/en/stable/) [zarr](https://zarr.dev/) files.
The spatialdata format should, in the long run, become comaptibel with the [OME-NGFF](https://ngff.openmicroscopy.org/latest/index.html) data format.

Spatialdata is the standard data format in the python spatial single cell community.
Data stored in this format can be analyzed the same way as spatial sc RNA seq data is analyzed.

```bash
pcdl_get_spatialdata output/output00000000.xml
```
```bash
pcdl_get_spatialdata output
```
```bash
pcdl_get_spatialdata -h
```

Further readings:
+ [TUTORIAL_python3_scverse.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_scverse.md)

### &#x2728; pcdl\_plot\_timeseries

Generate a time series plot and save it as a [jpeg](https://en.wikipedia.org/wiki/JPEG) file.

The default plots outputs total cell count over time.
However, this is a very powerful command!
Below, we generate a plot for:
+ total cell count
+ cell count per cell\_type
+ mean oxygen concentration detected per cell\_type
+ max oxygen concentration detected per cell\_type
+ mean oxygen concentration detected in the cells.
+ mean oxygen concentration detected in the domain.

```bash
pcdl_plot_timeseries output
```
```bash
pcdl_plot_timeseries output none
```

```bash
pcdl_plot_timeseries output cell_type
```
```bash
pcdl_plot_timeseries output cell_type oxygen
```
```bash
pcdl_plot_timeseries output cell_type oxygen max
```

```bash
pcdl_plot_timeseries output none oxygen
```
```bash
pcdl_plot_timeseries output none oxygen --frame conc
```

```bash
pcdl_plot_timeseries -h
```

### &#x2728; pcdl\_make\_ome\_tiff

Generate an [ome.tiff](https://ome-model.readthedocs.io/en/stable/index.html) file,
to analyze a single time step or the whole time series,
the same way as usually fluorescent microscopy data is analyzed.

By default, the cell\_attribute outputted is the cell ID + 1.
However, any numerical (bool, int, float) cell\_attribute can be outputted.
For example: dead, cells\_per\_voxel, or pressure.

These ome.tiff files can be further analyzed,
for example with the [Napari](https://napari.org/stable/) or [Fiji Imagej](https://fiji.sc/) or [Neuroglancer](https://research.google/blog/an-interactive-automated-3d-reconstruction-of-a-fly-brain/) or [Blender](https://www.blender.org/) or similar software,
as described in the extra tutorials.

```bash
pcdl_make_ome_tiff output/output00000000.xml pressure
```
```bash
pcdl_make_ome_tiff output
```
```bash
pcdl_make_ome_tiff -h
```

Further readings:
+ [TUTORIAL_python3_napari.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_napari.md)
+ [TUTORIAL_fiji_imagej.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_fijiimagej.md)
+ [TUTORIAL_neuroglancer.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_neuroglancer.md)
+ [TUTORIAL_blender.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_blender.md)

### &#x2728; pcdl\_render\_neuroglancer

With this command, you can render a time step ome.tiff file or a time step from a whole time series ome.tiff file straight into [Neuroglancer](https://research.google/blog/an-interactive-automated-3d-reconstruction-of-a-fly-brain/), which is a [WebGL](https://en.wikipedia.org/wiki/WebGL)-based viewer that will render the ome.tiff straight in your browser.

Below, we render a time step into Neuroglancer, first utilizing the time step ome.tiff, then using the whole time series ome.tiff.
You can only render one time step at a time and not a entire time series, like, for example, in napari.
```bash
pcdl_make_ome_tiff output/output00000000.xml
pcdl_render_neuroglancer output_2d/output00000000_oxygen_water_default_blood_cells_ID.ome.tiff
```
```bash
pcdl_make_ome_tiff output
pcdl_render_neuroglancer output_2d/timeseries_oxygen_water_default_blood_cells_ID.ome.tiff 3  # render time step 3 from the time series
```
```bash
pcdl_make_ome_tiff -h
```

Further readings:
+ [TUTORIAL_neuroglancer.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_neuroglancer.md)


## [Making movies](https://en.wikipedia.org/wiki/Making_Movies)

### &#x2728; pcdl\_make\_gif

Make a [gif](https://en.wikipedia.org/wiki/GIF) image from the jpeg plots from a time series.

```bash
pcdl_plot_scatter output
pcdl_make_gif output/cell_cell_type_z0.0/
```
```bash
pcdl_make_gif -h
```

### &#x2728; pcdl\_make\_movie

Make a [mp4](https://en.wikipedia.org/wiki/MP4_file_format) movie from the jpeg plots from a time series.

```bash
pcdl_plot_scatter output
pcdl_make_movie output/cell_cell_type_z0.0/
```
```bash
pcdl_make_movie -h
```


## Data Clean Up

After you are done checking out the 2D unit test dataset,
you can uninstall the datasets and remove the data in the output folder,
by executing the following command sequence.

```bash
python3 -c"import pcdl; pcdl.uninstall_data()"
make data-cleanup
```

That's it!
