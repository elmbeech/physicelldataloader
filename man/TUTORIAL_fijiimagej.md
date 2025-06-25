# PhysiCell Data Loader Tutorial: pcdl and Fiji, Imagej, Icy, QuPath.

[Fiji](https://fiji.sc/) is a free and open source image processing library,
a "batteries-included" distribution of [ImageJ](https://en.wikipedia.org/wiki/ImageJ),
able to read [ome.tiff](https://www.openmicroscopy.org/ome-files/) files.

[Icy](https://icy.bioimageanalysis.org/) and [QuPath](https://github.com/qupath/qupath/wiki/What-is-QuPath%3F) are similar bioimage analysis software applications.

Fiji Imagej, Icy, and QuPath are used by wet lab scientists and bioinformatician to analyze fluorescent and bright field microscopy data.
All these software applications can open the ome.tiff file format.


## Install Fiji Imagej (JDK), Icy, or QuPath  ~ the 64[bit] version!

Please follow the installation instructions on the official homepages.
+ https://imagej.net/software/fiji/
+ https://icy.bioimageanalysis.org/download/
+ https://qupath.github.io/


## Generate ome.tiff files from the command line

```bash
pcdl_make_ome_tiff('output/')
```


## Generate ome.tiff files from within python

```python
import pcdl

mcdsts = pcdl.TimeSeries('output/')
mcdsts.make_ome_tiff()
```


## Open ome.tiff files

Use the graphical user interface to open the ome.tiff files.


## Running Fiji Imagej, Icy, or QuPath

Please work through the official documentation to learn how to run the software.
+ https://imagej.net/learn/
+ https://icy.bioimageanalysis.org/
+ https://qupath.readthedocs.io/en/stable/

That's it. The rest is analysis within fiij imagej!
