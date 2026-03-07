```
usage: pcdl_plot_timeseries [-h] [--custom_data_type [CUSTOM_DATA_TYPE ...]]
                            [--microenv MICROENV] [--physiboss PHYSIBOSS]
                            [--settingxml SETTINGXML] [-v VERBOSE]
                            [--frame FRAME] [--cat_drop [CAT_DROP ...]]
                            [--cat_keep [CAT_KEEP ...]] [--z_slice Z_SLICE]
                            [--logy LOGY] [--ylim YLIM [YLIM ...]]
                            [--secondary_y SECONDARY_Y [SECONDARY_Y ...]]
                            [--subplots SUBPLOTS] [--sharex SHAREX]
                            [--sharey SHAREY] [--linestyle LINESTYLE]
                            [--linewidth LINEWIDTH] [--cmap CMAP]
                            [--color COLOR [COLOR ...]] [--grid GRID]
                            [--legend LEGEND] [--yunit YUNIT] [--title TITLE]
                            [--figsizepx FIGSIZEPX [FIGSIZEPX ...]]
                            [--ext EXT] [--figbgcolor FIGBGCOLOR]
                            [path] [focus_cat] [focus_num] [aggregate_num]

this function to generate a timeseries plot and either returns a matplotlib
figure or an image file (jpeg, png, tiff).

positional arguments:
  path                  path to the PhysiCell output directory. default is . .
  focus_cat             categorical or boolean data column within dataframe
                        specified under frame. default is None, which is
                        total, which is all agents or voxels, no categories.
                        default is None.
  focus_num             numerical data column within dataframe specified under
                        frame. default is None, which is count, agent or voxel
                        count. default is None.
  aggregate_num         aggregation function {max, mean, median, min, std,
                        var} for focus_num data. default is mean.

options:
  -h, --help            show this help message and exit
  --custom_data_type [CUSTOM_DATA_TYPE ...]
                        parameter to specify custom_data variable types other
                        than float (namely: int, bool, str) like this
                        var:dtype myint:int mybool:bool mystr:str . downstream
                        float and int will be handled as numeric, bool as
                        Boolean, and str as categorical data. default is an
                        empty string.
  --microenv MICROENV   should the microenvironment data be loaded? setting
                        microenv to False will use less memory and speed up
                        processing. default is True.
  --physiboss PHYSIBOSS
                        if found, should physiboss state data be extracted and
                        loaded into the df_cell dataframe? default is True.
  --settingxml SETTINGXML
                        the settings.xml that is loaded, from which the cell
                        type ID label mapping, is extracted, if this
                        information is not found in the output xml file. set
                        to None or False if the xml file is missing! default
                        is False.
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to False for less text output, while
                        processing. default is True.
  --frame FRAME         to specifies the data dataframe. cell: dataframe will
                        be retrieved through the mcds.get_cell_df function.
                        conc: dataframe will be retrieved through the
                        mcds.get_conc_df function. default is cell.
  --cat_drop [CAT_DROP ...]
                        if focus is a categorical attribute, set of category
                        labels to be dropped for the dataframe. Attention:
                        when the cat_keep parameter is given, then the
                        cat_drop parameter has to be an empty string! default
                        is an empty string.
  --cat_keep [CAT_KEEP ...]
                        if focus is a categorical attribute, set of category
                        labels to be kept in the dataframe. default is an
                        empty string.
  --z_slice Z_SLICE     z-axis position to slice a 2D xy-plain out of the 3D
                        mesh. if z_slice position numeric but not an exact
                        mesh center coordinate, then z_slice will be adjusted
                        to the nearest mesh center value, the smaller one, if
                        the coordinate lies on a saddle point. if set to None,
                        the whole domain is taken. default is None.
  --logy LOGY           if True, then y axis is natural log scaled. default is
                        False.
  --ylim YLIM [YLIM ...]
                        two floats. y axis min and max value. default is None,
                        which automatically detects min and max value. default
                        is None.
  --secondary_y SECONDARY_Y [SECONDARY_Y ...]
                        whether to plot on the secondary y-axis. if a listing
                        of string, which columns to plot on the secondary
                        y-axis. default is False.
  --subplots SUBPLOTS   whether to split the plot into subplots, one per
                        column. default is False.
  --sharex SHAREX       in case subplots is True, share x-axis by setting some
                        x-axis labels to invisible. default is False.
  --sharey SHAREY       in case subplots is True, share y-axis range and
                        possibly setting some y-axis labels to invisible.
                        default is False.
  --linestyle LINESTYLE
                        matplotlib line style {-, --, .-, :} string. default
                        is - .
  --linewidth LINEWIDTH
                        line width in points, float. default is None.
  --cmap CMAP           matplotlib colormap string from https://matplotlib.org
                        /stable/tutorials/colors/colormaps.html . default is
                        None.
  --color COLOR [COLOR ...]
                        listing of color strings referred to by name, RGB or
                        RGBA code. default is None.
  --grid GRID           plot axis grid lines. default is True.
  --legend LEGEND       if True or reverse, place legend on axis subplots.
                        default is True.
  --yunit YUNIT         string to specify y-axis unit. None will not print a
                        unit on the y-axis. default is None.
  --title TITLE         title to use for the plot. None will print no title.
                        default is None.
  --figsizepx FIGSIZEPX [FIGSIZEPX ...]
                        size of the figure in pixels (integer), x y. the given
                        x and y will be rounded to the nearest even number, to
                        be able to generate movies from the images. default is
                        640 480.
  --ext EXT             output format. possible image formats are jpeg, jpg,
                        png, tif, and tiff. for retrieving a datafarme file
                        use csv. default is jpeg.
  --figbgcolor FIGBGCOLOR
                        figure background color. None is transparent (png) or
                        white (jpeg, tiff). default is None.

homepage: https://github.com/elmbeech/physicelldataloader
```
