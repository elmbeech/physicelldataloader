# PhysiCell Data Loader Tutorial: pcdl and Paraview

<!--
bue 2024-09-02: vtk and paraview can handle up to 32 bit ometiff images.
fluorescent microscopy ome tiff standard is 16 bit.
+ https://discourse.vtk.org/t/failed-to-read-tiff-64-bit-samples/12118
-->

[Paraview](https://www.paraview.org/) is a free and open source scientific visualization software,
that lets us load and analyze vtk rectilinear grid data and vtk polynomial data, and even ome.tiff data files.

## Install paraview

For installation, please follow the official documentation.
+ https://www.paraview.org/download/


## Generate vtk files from the command line

```bash
pcdl_make_conc_vtk output
```
```bash
pcdl_make_cell_vtk output
```


## Generate vtk files from within python

```python
import pcdl

mcdsts = pcdl.TimeSeries('output/')
mcdsts.make_conc_vtk()
mcdsts.make_cell_vtk()
```


## Load vtk files with paraview
1. **View** / **Pipeline Browser** has to be checked!
2. **View** / **Properties** has to be checked!
3. **File** / **Open...** path/to/PhysiCell/output/output..\_conc.vtr [OK]
4. **File** / **Open...** path/to/PhysiCell/output/output..\_cell.vtp [OK]
5. In the **Pipeline Browser**, click the closed **eyes**, so that they open.
6. In the **Pipeline Browser**, click the output00000000\_cell.vtp\* and under **Properties Coloring** select cell\_type in the dropdown menu.
7. In the **Pipeline Browser**, click the output00000000\_conc.vtr\* and under **Properties Coloring** select the oxygen in the dropdown menu.

For learning more about how to run the software,
please work through the official documentation.
+ https://www.paraview.org/resources/


That's it. The rest is analysis within paraview!
