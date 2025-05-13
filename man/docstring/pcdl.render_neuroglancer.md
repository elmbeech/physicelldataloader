# mcdsts.render_neuroglancer('path/to/ome.tiff')


## input:
```
        tiffpathfile: string.
            path to ome tiff file.

        timestep: integer; default is 0.
            time step, within a possibly collapsed ome tiff file, to render.
            the default will work with single time step ome tiff files.

        intensity_cmap: string; default is 'gray'.
            matlab color map label, used to display expression intensity values.
            if None, no intensity layers will be generated.
            + https://matplotlib.org/stable/users/explain/colors/colormaps.html

```

## output:
```
        viewer: url to the loaded, neuroglancer rendered ome tiff file.

```

## description:
```
        function to load a time step from an ome tiff files, generated
        with make_ome_tiff, into neuroglancer.
    
```