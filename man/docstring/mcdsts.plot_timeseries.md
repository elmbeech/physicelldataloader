# mcdsts.plot_timeseries()


## input:
```
            self: TimeSeries class instance

            focus_cat: string; default is None
                categorical or boolean data column within dataframe specified under frame.
                default is None, which is total, which is all agents or voxels, no categories.

            focus_num: string; default is None
                numerical data column within dataframe specified under frame.
                default is None, which is count, agent or voxel count.

            aggregate_num: function; default np.nanmean
                aggregation function for focus_num data.

            frame: string; default is cell_df
                to specifies the data dataframe.
                cell: dataframe will be retrieved through the mcds.get_cell_df function.
                conc: dataframe will be retrieved through the mcds.get_conc_df function.

            z_slice: floating point number; default is None
                z-axis position to slice a 2D xy-plain out of the 3D mesh.
                if z_slice position numeric but not an exact mesh center coordinate,
                then z_slice will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.
                if set to None, the whole domain is taken.

            logy: bool; default False
                if True, then y axis is natural log scaled.

            ylim: tuple of two floats; default is None
                y axis min and max value.
                default is None, which automatically detects min and max value.

            secondary_y: bool or list of strings; default False
                whether to plot on the secondary y-axis.
                if a list, which columns to plot on the secondary y-axis.

            subplots: bool or sequence of iterable, default False
                whether to group columns into subplots.
                a sequence of iterable of column labels
                will create a subplot for each group of columns.

            sharex: bool, default False
                in case subplots is True, share x-axis by
                setting some x-axis labels to invisible.

            sharey: bool, default False
                in case subplots is True, share y-axis range and possibly
                setting some y-axis labels to invisible.

            linestyle: string or list of strings, default '-'
                matplotlib line style {'-', '--', '-.', ':', ''},
                over all or per column.

            linewidth: float or list of float, default None
                line width in points.

            cmap: string; default None
                matplotlib colormap string.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html
                achtung: if cmap is given, color will be disregarded.

            color: string or list of string or dictionary; default None
                color string referred to by name, RGB or RGBA code.
                achtung: if cmap is given, color will be disregarded.

            grid: boolean; default True
                plot axis grid lines.

            legend: bool or 'reverse'; default True
                if True or reverse, place legend on axis subplots.

            yunit: string; default None
                string to specify y-axis unit.
                None will not print a unit on the y-axis.

            title: string or list; default None
                title to use for the plot or subplots.
                None will print no title.

            ax: matplotlib axis object; default setting is None
                the ax object, which will be used as a canvas for plotting.
                None will generate a figure and ax object from scratch.

            figsizepx: list of two integers, default is [640, 480]
                size of the figure in pixels, (x, y).
                the given x and y will be rounded to the nearest even number,
                to be able to generate movies from the images.

            ext: string; default is None
                output image format. possible formats are None, jpeg, png, and tiff.
                if None then the matplotlib figure is returned by the function
                and not written to file.

            figbgcolor: string; default is None which is transparent (png)
                or white (jpeg, tiff).
                figure background color.
                only relevant if ext not is None.

            **kwargs: possible additional keyword arguments input,
                handled by the pandas series plot function.
                + https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.plot.html

```

## output:
```
            if ext is None: a fig matplotlib figure, containing the ax axis object, is returned.
            else: an image file is generated under the returned path.

```

## description:
```
            this function to generate a timeseries plot and either returns a
            matplotlib figure or an image file (jpeg, png, tiff).

            jpeg is by definition a lossy compressed image format.
            png is by definition a lossless compressed image format.
            tiff can by definition be a lossy or lossless compressed format.
            https://en.wikipedia.org/wiki/JPEG
            https://en.wikipedia.org/wiki/Portable_Network_Graphics
            https://en.wikipedia.org/wiki/TIFF
        
```