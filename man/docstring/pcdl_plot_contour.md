```
usage: pcdl_plot_contour [-h] [-v VERBOSE] [--z_slice Z_SLICE] [--vmin VMIN]
                         [--vmax VMAX] [--alpha ALPHA] [--fill FILL]
                         [--cmap CMAP] [--title TITLE] [--grid GRID]
                         [--xlim XLIM [XLIM ...]] [--ylim YLIM [YLIM ...]]
                         [--xyequal XYEQUAL]
                         [--figsizepx FIGSIZEPX [FIGSIZEPX ...]] [--ext EXT]
                         [--figbgcolor FIGBGCOLOR]
                         [path] [focus]

function generates matplotlib contour (or contourf) plots, inclusive color
bar, for the substrate specified, under the returned path.

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .
  focus                 column name within conc dataframe.

options:
  -h, --help            show this help message and exit
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to False for less text output, while
                        processing. default is True.
  --z_slice Z_SLICE     z-axis position to slice a 2D xy-plain out of the 3D
                        mesh. if z_slice position numeric but not an exact
                        mesh center coordinate, then z_slice will be adjusted
                        to the nearest mesh center value, the smaller one, if
                        the coordinate lies on a saddle point. default is 0.0.
  --vmin VMIN           float. None takes min from data. default is None.
  --vmax VMAX           float. None takes max from data. default is None.
  --alpha ALPHA         alpha channel transparency value between 1 (not
                        transparent at all) and 0 (totally transparent).
                        default is 1.0.
  --fill FILL           True generates a matplotlib contourf plot. False
                        generates a matplotlib contour plot. default is True.
  --cmap CMAP           matplotlib colormap string from https://matplotlib.org
                        /stable/tutorials/colors/colormaps.html . default is
                        viridis.
  --title TITLE         title prefix. default is an empty string.
  --grid GRID           plot axis grid lines. default is True.
  --xlim XLIM [XLIM ...]
                        two floats. x axis min and max value. None takes min
                        and max from mesh x axis range. default is None.
  --ylim YLIM [YLIM ...]
                        two floats. y axis min and max value. None takes min
                        and max from mesh y axis range. default is None.
  --xyequal XYEQUAL     to specify equal axis spacing for x and y axis.
                        default is true.
  --figsizepx FIGSIZEPX [FIGSIZEPX ...]
                        size of the figure in pixels (integer), x y. the given
                        x and y will be rounded to the nearest even number, to
                        be able to generate movies from the images. None tries
                        to take the values from the initial.svg file. fall
                        back setting is 640 480. default is None.
  --ext EXT             output image format. possible formats are jpeg, png,
                        and tiff. default is jpeg.
  --figbgcolor FIGBGCOLOR
                        figure background color. None is transparent (png) or
                        white (jpeg, tiff). default is None.

homepage: https://github.com/elmbeech/physicelldataloader
```
