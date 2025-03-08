# PhysiCell Data Loader Tutorial: pcdl and Python and the Ome.tiff, Tiff, Png, and Jpeg File Format

In pcdl output from [TimeSteps](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_timestep.md) and [TimeSeries](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_timeseries.md) can be stotred as [ome.tiff](https://www.openmicroscopy.org/ome-files/), [tiff](https://www.loc.gov/preservation/digital/formats/fdd/fdd000022.shtml), [png](http://libpng.org/pub/png/), and [jpeg](https://jpeg.org/jpeg/) files.

Tiff, png, and jpeg are raster graphic file formats.

Ome.tiff is the open microscopy image standard.
This means, being able to export PhysiCell output in ome.tiff files format
enables us to study PhysiCell output the same way
as commonly fluorescent microscopy data is analyzed by wetlab scientists.
Please have a look at [TUTORIAL_python3_napari.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_napari.md)
and [TUTORIAL_fiji_imagej.md](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_fijiimagej.md) to learn more.


Additionally ome.tiff, tiff, png, and jpeg files can as well be loaded back in to python as [numpy](https://numpy.org/) array, for example with the [sci-kit image](https://scikit-image.org/) library (image data only).

Besides that, ome.tiff files can be loaded with the [bioio](https://github.com/bioio-devs/bioio) library (image and metadata).


### Save pcdl data constructs from the command line into tiff and ome.tiff files

```bash
pcdl_make_ome_tiff('output/')
```
```bash
pcdl_plot_contour output/output00000012.xml oxygen
```
```bash
pcdl_plot_scatter output/output00000012.xml
```


### Save pcdl data constructs from within python into tiff and ome.tiff files

```python
import pcdl

mcdsts = pcdl.TimeSeries('output/')
mcdsts.get_mcds_list()[12].plot_contour(focus='oxygen', ext='tiff')
mcdsts.get_mcds_list()[12].plot_scatter(ext='tiff')
mcdsts.make_ome_tiff()
```


### Load tiff files as numpy array into python

```python
from skimage import io

a_conc = io.imread('output/conc_oxygen_z0.0/output00000012_oxygen.tiff')
a_conc.shape  # (480, 640, 4)
```
```python
from skimage import io

a_cell = io.imread('output/cell_cell_type_z0.0/output00000012_cell_type.tiff')
a_cell.shape  # (480, 640, 4)
```
```python
from skimage import io

a_ome = io.imread('output/timeseries_ID.ome.tiff')
a_ome.shape  # (25, 2, 200, 300)
```


### Load ome.tiff files as BioImage object into python

```python
from bioio import BioImage

img = BioImage('output/timeseries_ID.ome.tiff')
img.shape  # (25, 2, 1, 200, 300)
```
```python
img.dims  # <Dimensions [T: 25, C: 2, Z: 1, Y: 200, X: 300]>
```
```python
img.channel_names  # [np.str_('oxygen'), np.str_('cancer_cell')]
```

That's it. The rest is analysis!
