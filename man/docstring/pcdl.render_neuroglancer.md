# mcdsts.render_neuroglancer('path/to/ome.tiff')


## input:
```
        tiffpathfile: string.
            path to ome tiff file.

        timestep: integer, default is 0.
            variable to specify the specific time step to render.
            useful for time series ome.tiff files.
            the default is compatible with single time step ome.tiff files.

        intensity_cmap: string; default is 'gray'.
            matlab color map label, used to display expression intensity values.
            if None, no intensity layers will be generated.
            + https://matplotlib.org/stable/users/explain/colors/colormaps.html

```

## output:
```
        viewer: local url where the loaded, neuroglancer rendered ome tiff file
            can be viewed.

```

## description:
```
        function to load a time step from an ome tiff files, generated
        with make_ome_tiff, into neuroglancer.
    
```