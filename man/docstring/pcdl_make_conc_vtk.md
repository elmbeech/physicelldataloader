```
usage: pcdl_make_conc_vtk [-h] [-v VERBOSE] [--ext EXT] [path]

function generates rectilinear grid vtk files, one per mcds time step,
contains distribution of substrates over microenvironment. you can post-
process this files in other software like paraview
(https://www.paraview.org/).

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .

options:
  -h, --help            show this help message and exit
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to False for less text output, while
                        processing. default is True.
  --ext EXT             file extension for the vtk rectilinear grid file.

homepage: https://github.com/elmbeech/physicelldataloader
```
