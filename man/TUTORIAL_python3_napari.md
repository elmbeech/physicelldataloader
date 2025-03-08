# PhysiCell Data Loader Tutorial: pcdl and Python and Napari

[Napari](https://napari.org/stable/) is both a python library and a GUI software.
Napari is used by wetlab scientists and bioinformatician to analyze fluorescent microscopy data.
Napari can read [ome.tiff](https://www.openmicroscopy.org/ome-files/) files.
https://github.com/AllenCellModeling/napari-aicsimageio


## Install napari

```bash
pip3 install napari[all]
```


### Generate ome.tiff files from the command line

```bash
pcdl_make_ome_tiff('output/')
```


### Generate ome.tiff files from within python

```python
import pcdl

mcdsts = pcdl.TimeSeries('output/')
mcdsts.make_ome_tiff()
```


### Open ome.tiff files in napari from within python

```python
import napari

viewer = napari.Viewer()
viewer.open('output/timeseries_ID.ome.tiff')
```


### Open ome.tiff files in napari from the command line

```bash
napari output/timeseries_ID.ome.tiff
```

## Running napari

Please work through the official documentation to learn how to run the software.
+ https://napari.org/stable/tutorials/start_index.html

That's it. The rest is analysis within napari!
