# mcds.make_ome_tiff()


## input:
```
            cell_attribute: strings; default is 'ID', which will result in a
                cell segmentation mask.
                column name within the cell dataframe.
                the column data type has to be numeric (bool, int, float)
                and cannot be string.
                the result will be stored as 32 bit float.

            conc_cutoff: dictionary string to real; default is an empty dictionary.
                if a contour from a substrate not should be cut by greater
                than zero (shifted to integer 1), another cutoff value can be
                specified here.

            focus: set of strings; default is a None
                set of substrate and cell_type names to specify what will be
                translated into ome tiff format.
                if None, all substrates and cell types will be processed.

            file: boolean; default True
                if True, an ome tiff file is the output.
                if False, a numpy array with shape czyx is the output.

```

## output:
```
            a_tczyx_img: numpy array or ome tiff file.

```

## description:
```
            function to transform chosen mcds output into an 1[um] spaced
            czyx (channel, z-axis, y-axis, x-axis) ome tiff file or numpy array,
            one substrate or cell_type per channel.
            an ome tiff file is more or less:
            a numpy array, containing the image information
            and a xml, containing the microscopy metadata information,
            like the channel labels.
            the ome tiff file format can for example be read by the napari
            or fiji (imagej) software.

            https://napari.org/stable/
            https://fiji.sc/
        
```