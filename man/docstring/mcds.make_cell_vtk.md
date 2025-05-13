# mcds.make_cell_vtk()


## input:
```
            attribute: list of strings; default is ['cell_type']
                column name within cell dataframe.

```

## output:
```
            s_vtkpathfile: vtk 3D glyph polynomial data file that contains cells.

```

## description:
```
            function that generates vtk 3D glyph polynomial data file for cells.
            cells can have specified attributes like cell_type,
            pressure, dead, etc.
            you can post-process this file in other software like paraview.

            https://www.paraview.org/
        
```