# mcds.plot_scatter()


## input:
```
            focus: string; default is 'cell_type'
                column name within cell dataframe.

            z_slice: floating point number; default is 0.0
                z-axis position to slice a 2D xy-plain out of the
                3D substrate concentration mesh. if z_slice position
                is not an exact mesh center coordinate, then z_slice
                will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.

            z_axis: for a categorical focus: set of labels;
               for a numeric focus: tuple of two floats; default is None
               depending on the focus column variable dtype, default extracts
               labels or min and max values from data.

            alpha: floating point number; default is 1.0
                alpha channel transparency value
                between 1 (not transparent at all) and 0 (totally transparent).

            cmap: dictionary of strings or string; default viridis.
                dictionary that maps labels to colors strings.
                matplotlib colormap string.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html

            title: string; default None
                possible plot title string.

            grid: boolean default True.
                plot axis grid lines.

            legend_loc: string; default is 'lower left'.
                the location of the categorical legend, if applicable.
                possible strings are: best,
                upper right, upper center, upper left, center left,
                lower left, lower center, lower right, center right,
                center.

            xlim: tuple of two floats; default is None
                x axis min and max value.
                default takes min and max from mesh x axis range.

            ylim: tuple of two floats; default is None
                y axis min and max value.
                default takes min and max from mesh y axis range.

            xyequal: boolean; default True
                to specify equal axis spacing for x and y axis.

            s: floating point number; default is 1.0
                scatter plot dot size scale factor.
                with figsizepx extracted from initial.svg, scale factor 1.0
                should be ok. adjust if necessary.

            ax: matplotlib axis object; default setting is None
                the ax object, which will be used as a canvas for plotting.
                None will generate a figure and ax object from scratch.

            figsizepx: list of two integers; default is None
                size of the figure in pixels, (x, y).
                the given x and y will be rounded to the nearest even number,
                to be able to generate movies from the images.
                None tries to take the values from the initial.svg file.
                fall back setting is [640, 480].

            ext: string; default is None
                output image format. possible formats are jpeg, png, and tiff.
                None will return the matplotlib fig object.

            figbgcolor: string; default is None which is transparent (png)
                or white (jpeg, tiff).
                figure background color.

            **kwargs: possible additional keyword arguments input,
                handled by the pandas dataframe plot function.
                + https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html

```

## output:
```
            fig: matplotlib figure, depending on ext, either as object or as file.
                the figure contains the scatter plot and color bar (numerical data)
                or color legend (categorical data).

```

## description:
```
            function returns a (pandas) matplotlib scatter plot,
            inclusive color bar or color legend, for the focus specified,
            either as matplotlib fig object or as jpeg, png, or tiff file.

            jpeg is by definition a lossy compressed image format.
            png is by definition a lossless compressed image format.
            tiff can by definition be a lossy or lossless compressed format.
            https://en.wikipedia.org/wiki/JPEG
            https://en.wikipedia.org/wiki/Portable_Network_Graphics
            https://en.wikipedia.org/wiki/TIFF
        
```