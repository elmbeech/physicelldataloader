# mcdsts.make_cell_vtk()


## input:
```
            attribute: list of strings; default is ['cell_type']
                column name within cell dataframe.

```

## output:
```
            ls_vtkpathfile: one 3D glyph vtk file per mcds time step
                that contains cells.

```

## description:
```
            function that generates 3D glyph vtk files for cells.
            one file per mcds time step. cells can have specified attributes
            like cell_type, pressure, dead, etc.
            you can post-process this file in other software like paraview.

            https://www.paraview.org/
        
```