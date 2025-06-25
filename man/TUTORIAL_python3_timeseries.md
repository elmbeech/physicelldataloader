# PhysiCell Data Loader Tutorial: pcdl and Python and MCDS TimeSeries

If not already done so, please install the latest version of physicelldataloader (pcdl), as described in the [HowTo](https://github.com/elmbeech/physicelldataloader/blob/master/man/HOWTO.md) section.
And maybe read about the pcdl [background](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_introduction.md) information.
And perhaps, work thorough the [TUTORIAL_python3_timestep.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_timestep.md)


An exciting thing about modeling is to have time series data.
Pcdl's TimeSeries class is here to make the handling of a time series of MCD snapshots easy.

All analysis functions available for TimeStep are available for TimeSeries too,
and we will not further discuss them here.
For the details, please read the TimeStep tutorial and study the docstrings!

For microenvironment data, these are the functions:
<!--
+ mcdsts.get_substrate_list()  # bue: will never be implementd
-->
```python
mcdsts.get_conc_df()
```
```python
mcdsts.plot_contour('substrate')
```
```python
mcdsts.make_conc_vtk()
```

For cell data, these are the functions:
<!--
+ mcdsts.get_celltype_list()  # bue: will never be implementd
+ mcdsts.get_cell_attribute_list()  # bue: will never be implementd
-->
```python
mcdsts.get_cell_df()
```
```python
mcdsts.get_anndata()
```
```python
mcdsts.make_graph_gml()
```
```python
mcdsts.plot_scatter()
```
```python
mcdsts.make_cell_vtk()
```

For microenvironment and cell data, these are the functions:
```python
mcdsts.make_ome_tiff()
```
```python
mcdsts.render_neuroglancer(mcdsts.make_ome_tiff(), timestep=0)
```

Yet, there are additional functions, that only make sense for TimeSeries,
and those functions will be discussed in this chapter.

For handling TimeSeries, these are the functions:
+ `mcdsts.get_xmlfile_list()`
+ `mcdsts.read_mcds()`
+ `mcdsts.get_mcds_list()`
+ `mcdsts.get_annmcds_list()`

For microenvironment data, this is the function:
+ `mcdsts.get_conc_attribute()`

For cell data, this is the function:
+ `mcdsts.get_cell_attribute()`

For microenvironment and cell data, this is the function:
+ `mcdsts.plot_timeseries()`

Besides, there are functions to render a set of jpeg, png, or tiff images into a movie.
+ `mcdsts.make_movie()` and `pcdl.make_movie()`
+ `mcdsts.make_gif()` and `pcdl.make_gif()`



## Preparation

To run this tutorial,
you can either work the data that is currently in your output folder,
or you can install the 2D unit test dataset into your PhysiCell output folder,
by executing the following command sequence.

&#x26A0; **Warning: if you run this sequence, all data currently in your PhysiCell/output folder will be overwritten!**

```bash
cd path/to/PhysiCell
```
```bash
make data-cleanup
python3 -c"import pathlib, pcdl, shutil; pcdl.install_data(); s_ipath=str(pathlib.Path(pcdl.__file__).parent.resolve()/'output_2d'); shutil.copytree(s_ipath, 'output', dirs_exist_ok=True)"
```



## Loading an MCDS Time Series


Like in the TimeStep class, for memory consumption and processing speed control,
we can specify if we want to load microenvironment data and graph data from the snapshots we later on analyze.
Additionally, we can specify, if for first even want to load data at all,
or if we only would like to load the output xml file list, which we will see, can be manipulated before actual data is loaded.

By default, all data from all snapshots is loaded.
Side note: for paths, in general, unix (slash) and windows (backslash) notation will work.

```python
import pcdl  # the physicell data loader library
print('pcdl version:', pcdl.__version__)  # it is easy to figure out which pcdl version you run

mcdsts = pcdl.TimeSeries('output/')
```

Fine tuned what data from a time step will be loaded
Here we only load cell data, not even information about cell type ID:label mapping.

```python
import pcdl  # the physicell data loader library,
print('pcdl version:', pcdl.__version__)  # it is easy to figure out which pcdl version you run

mcdsts = pcdl.TimeSeries(s_path, custom_data_type={}, load=True, microenv=False, graph=False, settingxml=None)
```

Fine tuned which time steps are loaded.
Here we generate a mcdsts TimeSeris object, wihtout loading any data.

```python
import pcdl  # the physicell data loader library,
print('pcdl version:', pcdl.__version__)  # it is easy to figure out which pcdl version you run

mcdsts = pcdl.TimeSeries(s_path, load=False)
```

The **get_xmlfile_list** function will return a list of "absolute path to output xml file" strings.
This list can be manipulated, and later be fed into the **read_xml** function, to only read chosen time steps into memory.

For example, if you want only to analyze hour 11, 12, and 13 from your run.

```python
ls_xml = mcdsts.get_xmlfile_list()  # ['/path/to/output00000000.xml', ..., ...]
ls_xml_11_12_13 = ls_xml[11:14]  # ['/path/to/output00000011.xml', ..., ...]
```

For example, if data from every other hour will be enough, you can filter for every even time step.

```python
ls_xml = mcdsts.get_xmlfile_list()  # ['/path/to/output00000000.xml', ..., ...]
ls_xml_even = [s_xml for i, s_xml in enumerate(ls_xml) if (i%2 == 0)]  # ['/path/to/output00000000.xml', ..., ...]
```

The **read_xml** function will finally read the snapshots into RAM.

Load snapshot 11, 12, and 13
```python
mcdsts.read_mcds(ls_xml_11_12_13)
len(mcdsts.get_mcds_list())  # 3
```

Load all even snapshots
```
mcdsts.read_mcds(ls_xml_even)
len(mcdsts.get_mcds_list())  # 13
```

Single snapshots can now be accessed by indexing.
With a single snapshot, you may work exactly in the same way as with an object loaded by TimeStep.

```python
mcdsts.get_mcds_list()[12].get_time()  # 720.0
```

It is very easy to loop over the whole time series.

```python
for mcds in mcdsts.get_mcds_list():
    print(mcds.get_mcds_list().get_time())
```

If you translate your time series into [anndata]((https://anndata.readthedocs.io/en/latest/) Objects,
using the collapse=False argument, you will endup with a similar list for anndata objects.

```python
mcdsts.get_anndata(values=2, scale='maxabs', collapse=False)
mcdsts.get_annmcds_list()  # [AnnData object with n_obs × n_vars ..., ..., ...]
```



## Microenvironment Data Related Functions (Continuum Variables)

Substrates that have no variance, zero entropy, that have in every inch of the domain overall time steps the exact same concentration, carry no information.
There is no need to analyze such substrate.
We can triage for substrate.

All substrates:

```python
dl_conc = mcdsts.get_conc_attribute()
dl_conc.keys()
```

All substrates with variances:

```python
dl_conc = mcdsts.get_conc_attribute(values=2)
dl_conc.keys()
```

Detected min max oxygen value:
```python
dl_conc = mcdsts.get_conc_attribute()
dl_conc['oxygen']
```

Number of different oxygen values registered:

```python
dl_conc = mcdsts.get_conc_attribute(allvalues=True)
len(dl_conc['oxygen'])
```

```python
help(mcdsts.get_conc_attribute)
```



## Cell Data Related Functions (Discrete Cells)

Cell variables that show no variance, zero entropy, that have in all agent overall time steps always exactly the same value, carry no information.
There is no need to analyze such cell attributes.
We can triage for interesting attributes.

List all tracked cell attributes:

```python
dl_cell = mcdsts.get_cell_attribute()
dl_cell.keys()
```

List all tracked cell attributes with variances:

```python
dl_cell = mcdsts.get_cell_attribute(values=2)
dl_celll.keys()
```

Detected min max pressure value:

```python
dl_cell = mcdsts.get_cell_attribute()
dl_cell['pressure']
```

Number of different pressure values registered:

```python
dl_cell = mcdsts.get_cell_attribute(allvalues=True)
len(dl_cell['pressure'])
```

```python
help(mcdsts.get_cell_attribute)
```



## Microenvironment and Cell Data Related Functions

For visualization, the TimeSeries class has a versatile time series plot function.
Below are some examples, from what all can be plotted.

Total cell count:

```python
mcdsts.plot_timeseries()
```

Cell count per cell type:

```python
mcdsts.plot_timeseries('cell_type')
```

Mean oxygen concentration detected per cell\_type:

```python
mcdsts.plot_timeseries(cell_type oxygen)
```

Max oxygen concentration detected per cell\_type:

```python
mcdsts.plot_timeseries(cell_type oxygen max)
```

mean oxygen concentration detected in the cells:

```python
mcdsts.plot_timeseries(output none oxygen)
```

mean oxygen concentration detected in the domain:

```python
mcdsts.plot_timeseries(none oxygen --frame conc)
```

Please study the docstring to grasp the full power of this function.

```python
help(mcdsts.plot_timeseries)
```



## Making Movies

With PhysiCell it is not only possible to take data snapshots,
but as well [svg](https://en.wikipedia.org/wiki/SVG) vector graphics images snapshots. \
PhysiCell's [Makefile](https://en.wikipedia.org/wiki/Make_(software)) has code
to translate those svg images into [jpeg](https://en.wikipedia.org/wiki/JPEG) and [gif](https://en.wikipedia.org/wiki/GIF) images,
making use of the [image magick](https://en.wikipedia.org/wiki/ImageMagick) library. \
The Makefile also has  code to translate the jpeg images into a [mp4](https://en.wikipedia.org/wiki/MP4_file_format) movie,
therefore utilizing the [ffmpeg](https://en.wikipedia.org/wiki/FFmpeg) library.\
TimeSeries instances provide similar functionality, although the jpeg (or [png](https://en.wikipedia.org/wiki/Portable_Network_Graphics) or [tiff](https://en.wikipedia.org/wiki/TIFF)) images
are generated straight from data and not from the svg files.
However, mp4 movies and gif images are generated in the same way.
This means the mcdsts.make\_gif function will only run if image magick
and mcdsts.make\_movie function will only run if ffmpeg is installed on your computer.

For microenvironment data:

```python
mcdsts.plot_contour(focus='oxygen')  # generate jpeg images colored by oxygen values
```
```python
mcdsts.make_gif(s_path)  # generate gif image
mcdsts.make_movie(s_path)  # generate mp4 movie
```
```python
pcdl.make_gif(s_path)  # generate gif image
pcdl.make_movie(s_path)  # generate mp4 movie
```

For cell data:

```python
mcdsts.plot_scatter()  # generate jpeg images colored by cell_type
```
```python
mcdsts.make_gif('output/cell_cell_type_z0.0/')a  # generate gif image
mcdsts.make_movie('output/cell_cell_type_z0.0/')  # generate mp4 movie
```
```python
pcdl.make_gif('output/cell_cell_type_z0.0/')  # generate gif image
pcdl.make_movie('output/cell_cell_type_z0.0/')  # generate mp4 movie
```



### Data Clean Up

After you are done checking out the 2D unit test dataset,
you can uninstall the datasets and remove the data in the output folder,
by executing the following command sequence.

```bash
python3 -c"import pcdl; pcdl.uninstall_data()"
make data-cleanup
```


That's it!
