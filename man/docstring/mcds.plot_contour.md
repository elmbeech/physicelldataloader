# mcds.plot_contour()


## input:
```
            focus: string
                column name within conc dataframe, for example substrate name.

            z_slice: floating point number; default is 0.0
                z-axis position to slice a 2D xy-plain out of the
                3D substrate concentration mesh. if z_slice position
                is not an exact mesh center coordinate, then z_slice
                will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.

            vmin: floating point number; default is None
                color scale min value.
                None will take the min value found in the data.

            vmax: floating point number; default is None
                color scale max value.
                None will take the max value found in the data.

            alpha: floating point number; default is 1
                alpha channel transparency value
                between 1 (not transparent at all) and 0 (totally transparent).

            fill: boolean; default is True
                True generates a matplotlib contourf plot.
                False generates a matplotlib contour plot.

            cmap: string; default is viridis
                matplotlib color map color label.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html

            title: string; default None
                possible plot title string.

            grid: boolean; default True
                should be plotted on  a grid or on a blank page?
                True will plot on a grid.

            xlim: tuple of two floating point numbers; default is None
                to specify min and max x axis value.
                None will extract agreeable values from the data.

            ylim: tuple of two floating point numbers; default is None
                to specify min and max y axis value.
                None will extract agreeable values from the data.

            xyequal: boolean; default True
                to specify equal axis spacing for x and y axis.

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
                handled by the matplotlib contour and contourf function.
                + https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html
                + https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contourf.html

```

## output:
```
            fig: matplotlib figure, depending on ext, either as object or as file.
                the figure containing the contour plot and color bar.

```

## description:
```
            function returns a matplotlib contour (or contourf) plot,
            inclusive color bar, for the focus specified, either
            as matplotlib fig object or as jpeg, png, or tiff file.
        
```