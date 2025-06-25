# PhysiCell Data Loader Tutorial: pcdl and Neuroglancer.

[Neuroglancer](https://research.google/blog/an-interactive-automated-3d-reconstruction-of-a-fly-brain/) is a [WebGL](https://en.wikipedia.org/wiki/WebGL)-based viewer for volumetric data.
It is capable of displaying arbitrary (non axis-aligned) cross-sectional views of volumetric data, as well as 3-D meshes and line-segment based models (skeletons).

[Ome.tiff](https://www.openmicroscopy.org/ome-files/) is the open microscopy image standard format used by wet lab scientists to store (fluorescent) microscopy data.

In 2022, in the middle of the pandemic, a small group of programmers undertook at the Image Analysis Working Group of the Cancer Systems Biology Consortium & Physical Sciences-Oncology Network [hackathon](https://github.com/IAWG-CSBC-PSON/hack2022-10-neuroglancer) the endeavor to write a python3 script that directly can render ome.tiff files into Neurogalncer.
This script was adapted for the pcdl project.


### &#x2728; command line

With pcdl it is very easy to generate time step and time series ome.tiff files from regular PhysiCell output straight from the command line and render them into Neuroglancer.

#### command line time step
Generate time step 6 ome.tiff

```bash
pcdl_make_ome_tiff pcdl_make_ome_tiff output_2d/output00000006.xml
```

Render time step 6 ome.tiff

```bash
pcdl_render_neuroglancer output_2d/output00000006_oxygen_water_default_blood_cells_ID.ome.tiff
```

#### command line time series

Generate time series ome.tiff

```bash
pcdl_make_ome_tiff output/
```

Render timer series time step 0.

```bash
pcdl_render_neuroglancer output/timeseries_oxygen_water_default_blood_cells_ID.ome.tiff
```

Render time series time step 12.

```bash
pcdl_render_neuroglancer output/timeseries_oxygen_water_default_blood_cells_ID.ome.tiff 12
```

#### command line man pages

```bash
pcdl_make_ome_tiff -h
```
```bash
pcdl_render_neuroglancer -h
```

### &#x2728; python
With pcdl it is very easy to generate within python3 time steps and time series ome.tiff files from regular PhysiCell output and render them into Neuroglancer.

#### python time step

Generate and directly render time step 6.
```python
import pcdl

mcds = pcdl.TimeStep('output_2d/output00000006.xml')
mcds.render_neuroglancer(mcds.make_ome_tiff())
```

#### python time series

Generate time series, then render.
```python
import pcdl

mcdsts = pcdl.TimeSeries('output_2d/')
s_pathfile = mcdsts.make_ome_tiff()
mcdsts.render_neuroglancer(s_pathfile)  #  time step 0
```
```python
mcdsts.render_neuroglancer(s_pathfile, 12)  #  time step 12
```

#### python docstrings

```python
import pcdl
help(pcdl.render_neuroglancer)
```

### &#x2728; Further readings

Please work through the official documentation to learn how to run the Neuroglancer software.
+ https://github.com/google/neuroglancer
+ https://neuroglancer-docs.web.app/index.html
+ https://research.google/blog/an-interactive-automated-3d-reconstruction-of-a-fly-brain/

That's it. The rest is analysis within neuroglancer!
