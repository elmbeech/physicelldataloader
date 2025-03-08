![physicellcdataloader logo & title](man/img/physicelldataloader_title_v3.0.0.png)

## Abstract:

physicelldataloader (pcdl) provides a platform independent, python3 based, [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) installable interface
to load output, generated with the [PhysiCell](https://github.com/MathCancer/PhysiCell) agent-based modeling and diffusion solver framework,
into [python3](https://en.wikipedia.org/wiki/Python_(programming_language)).

pcdl was forked from the original [PhysiCell-Tools](https://github.com/PhysiCell-Tools) [python-loader](https://github.com/PhysiCell-Tools/python-loader) implementation.

The pcdl python3 library maintains three branches:

+ **Branch version 1** is the original PhysiCell-Tools/python-loader code.
+ **Branch version 2** will be strictly compatible with the original PhysiCell-Tools/python-loader code, although pip installable.
+ **Branch version 3** might break with old habits, although tries to be as much downward compatible as possible.
  The aim of the v3 branch is to get a very lean and agile python3 physicell output interface for the ones coming from the python3 world.


## Header:

+ Language: python [>= 3.9](https://devguide.python.org/versions/)
+ Library dependencies: anndata, bioio, matplotlib, numpy, pandas, (requests), scipy, vtk
+ Date of origin original PhysiCell-Tools python-loader: 2019-09-02
+ Date of origin pcdl fork: 2022-08-30
+ Doi: https://doi.org/10.5281/ZENODO.8176399
+ License: [BSD-3-Clause](https://en.wikipedia.org/wiki/BSD_licenses)
+ User manual: this README.md file
+ Source code: [https://github.com/elmbeech/physicelldataloader](https://github.com/elmbeech/physicelldataloader)


## HowTo Guide:

+ [installation and troubleshooting](https://github.com/elmbeech/physicelldataloader/tree/master/man/HOWTO.md)


## Tutorial:

Basics Tutorials:

1. [pcdl background](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_introduction.md)
1. [pcdl processing mcds time steps in python3](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_timestep.md)
1. [pcdl processing mcds time series in python3](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_timeseries.md)
1. [pcdl from the command line](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_commandline.md)

Extras tutorials python3 language:
+ [pcdl and python3 and json](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_json.md)
+ [pcdl and python3 and pandas](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_pandas.md)
+ [pcdl and python3 and scipy and scanpy](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_scverse.md)
+ [pcdl and python3 and graphs](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_graph.md)
+ [pcdl and python3 and matplotlib](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_matplotlib.md)
+ [pcdl and python3 and vtk](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_vtk.md)
+ [pcdl and python3 and ome.tiff, tiff, png, and jpeg](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_ometiff.md)
+ [pcdl and python3 and napari](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_napari.md)

Extras tutorials for other languages than python3:

+ [pcdl and julia](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_julia.md)
+ [pcdl and matlab](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_matlab_octave.md)
+ [pcdl and R](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_r.md)

Extras tutorials for GUI software:

+ [pcdl and paraview](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_paraview.md)
+ [pcdl and blender](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_blender.md)
+ [pcdl and napari](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_python3_napari.md)
+ [pcdl and fiji imagej](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_fijiimagej.md)
<!--
+ [pcdl and neuroglancer](https://github.com/elmbeech/physicelldataloader/tree/master/man/TUTORIAL_(python3)_neuroglancer.md)
-->

Slides:

+ [presentations given](https://github.com/elmbeech/physicelldataloader/tree/master/man/lecture)


## Reference Manual:

+ [API application interface](https://github.com/elmbeech/physicelldataloader/tree/master/man/REFERENCE.md)


## Discussion:

To be developed.


## About Documentation:

Within the pcdl library, we tried to stick to the documentation policy laid out by Daniele Procida in his "[what nobody tells you about documentation](https://www.youtube.com/watch?v=azf6yzuJt54)" talk at PyCon 2017 in Portland, Oregon.


## Contributions:

+ original PhysiCell-Tools python-loader implementation: Patrick Wall, Randy Heiland, Paul Macklin
+ fork pcdl implementation: Elmar Bucher
+ fork pcdl co-programmer: Furkan Kurtoglu, Jennifer Eng, Heber Rocha
+ fork pcdl continuous testing and feedbacks: Aneequa Sundus, John Metzcar
+ student prj on pcdl:
  Benjamin Jacobs (make\_gml),
  Katie Pletz (beta testing),
  Marshal Gress (plot\_scatter),
  Nick Oldfather (unit test model),
  Thierry-Pascal Fleurant (plot\_timeseries)

Developers, please make pull requests to the https://github.com/elmbeech/physicelldataloader/tree/development branch. Thanks!


## Cite:

```bibtex
@Misc{bucher2023,
  author    = {Bucher, Elmar and Wall, Patrick and Rocha, Heber and Kurtoglu, Furkan and Eng, Jennifer and Sundus, Aneequa, and Metzcar, John and Heiland, Randy and Macklin, Paul},
  title     = {elmbeech/physicelldataloader: pcdl platform-independent, pip-installable interface to load PhysiCell agent-based modeling framework output into python3.},
  year      = {2023},
  copyright = {Open Access},
  doi       = {10.5281/ZENODO.8176399},
  publisher = {Zenodo},
}
```


## Road Map:

+ evt generate lineage tree graph output files.
+ evt add neuroglancer ome.tiff support.
+ evt add DataDiVR support.

## Release Notes:
+ version 3.3.4 (2025-03-07): elmbeech/physicelldataloader
    + replace the **aicsimageio** library dependency with its successor **bioio**. special thanks to Joel Eliason!
    + **make_ome_tiff** can handle automatically generated file names with > 255 characters. special thank to Genevieve Stein-O'Brien and DanielBergman!
    + **get_mesh_spacing** handels now an edge case correctly that would have resulted in a division by zero. special thanks to Randy Heiland!

+ version 3.3.3 (2025-01-10): elmbeech/physicelldataloader
    + bug fix **plot_contour** plot orientation. special thanks to Marco Ruscone!
    + add test data for new improved **unittest physicell model**. special thanks to Nick Oldfather!
    + add pyMCDS **make_conc_vtk** on the fly visualization. special thanks to Randy Heiland and Nick Oldfather!
    + pyMCDS and pyMCDSts **make_graph_gml** and pyAnnData **get_anndata** handles now spring\_attached\_cells graph too.

+ version 3.3.2 (2024-11-24): elmbeech/physicelldataloader
    + **Warnings** will no longer be piped to standard output if verbose is set to False.
    + pyMCDS **make_ome_tiff** function rewriten to be less RAM hungry and more versatile.

+ version 3.3.1 (2024-09-22): elmbeech/physicelldataloader
    + bugfix pyMCDS custom vectors loading.

+ version 3.3.0 (2024-08-22): elmbeech/physicelldataloader
    + **pip install pcdl**: will again install all library dependencies. The fine-tuned version was too confssing.
    + pyMCDS handels now intracellular **physinboss** data too; data is stored in cell\_df.
    + rename pyMCDS get\_cell\_variables to **get_celltype_list** for conciseness and order list by ID.
    + rename pyMCDS get\_substrate\_names to **get_substrate_list** for conciseness and order list by ID.
    + rename pyMCDS get\_scatter to **plot_scatter** for conciseness.
    + rename pyMCDS get\_contour to **plot_contour** for conciseness.
    + rename pyMCDSts make\_imgcell to **plot_scatter** for conciseness.
    + rename pyMCDSts make\_imgconc to **plot_contour** for conciseness.
    + rename pyMCDSts get\_cell\_df\_states to **get_cell_attribute** for conciseness.
    + rename pyMCDSts get\_conc\_df\_states to **get_conc_attribute** for conciseness.
    + rewrite pyMCDS mcds.get\_unit\_se into **mcds.get_unit_dict**.
    + new pyCLI **pcdl_get_anndata** command line interface function.
    + new pyCLI **pcdl_get_celltype_list** command line interface function.
    + new pyCLI **pcdl_get_cell_attribute** command line interface function.
    + new pyCLI **pcdl_get_cell_df** command line interface function.
    + new pyCLI **pcdl_get_substrate_list** command line interface function.
    + new pyCLI **pcdl_get_conc_attribute** command line interface function.
    + new pyCLI **pcdl_get_conc_df** command line interface function.
    + new pyCLI **pcdl_get_graph_gml** command line interface function.
    + new pyCLI **pcdl_get_unit_dict** command line interface function.
    + new pyCLI **pcdl_get_version** command line interface function.
    + new pyCLI **pcdl_make_cell_vtk** command line interface function.
    + new pyCLI **pcdl_make_conc_vtk** command line interface function.
    + new pyCLI **pcdl_make_gif** command line interface function.
    + new pyCLI **pcdl_make_movie** command line interface function.
    + new pyCLI **pcdl_make_ome_tiff** command line interface function.
    + new pyCLI **pcdl_plot_contour** command line interface function.
    + new pyCLI **pcdl_plot_scatter** command line interface function.
    + new pyCLI **pcdl_plot_timeseries** command line interface function.
    + new pyMCDS **mcds.get_mesh_mnp** function, the mesh version from mcds.get\_voxel\_ijk.
    + new pyMCDS **make_conc_vtk** function, to save substrate data as rectilinear grid vtk file.
    + new pyMCDS **make_cell_vtk** function, to save cell data as glyph vtk file.
    + new pyMCDS **make_graph_gml** function, to save graphs in a networkx and igraph compatible file format.
    + new pyMCDS **make_ome_tiff** function, to save the output data in ome tiff file format.
    + new pyMCDS **set_verbosity_true** function, to complete pcdl.TimeStep(verbosity=True/False) experience.
    + new pyMCDS **set_verbosity_false** function, to complete pcdl.TimeStep(verbosity=True/False) experience.
    + new pyMCDSts **get_cell_df** function, to extract one big dataframe or a list of dataframes from the whole time series.
    + new pyMCDSts **get_conc_df** function, to extract one big dataframe or a list of dataframes from the whole time series.
    + new pyMCDSts **make_cell_vtk** function, to save substrate data as rectilinear grid vtk files. special thanks to Furkan Kurtoglu!
    + new pyMCDSts **make_conc_vtk** function, to save cell data as glyph vtk files. special thanks to Furkan Kurtoglu!
    + new pyMCDSts **make_graph_gml** function, to save graphs in a networkx and igraph compatible files format. special thanks to Benjamin Jacobs!
    + new pyMCDSts **make_ome_tiff** function, to save the output data in ome tiff file format.
    + new pyMCDSts **plot_timeseries** function, to plot time series. special thanks to Thierry-Pascal Fleurant!
    + new pyMCDSts **set_verbosity_true** function, to complete the pcdl.TimeSeries(verbosity=True/False) experience.
    + new pyMCDSts **set_verbosity_false** function to complete the pcdl.TimeSeries(verbosity=True/False) experience.

+ version 3.2.13 (2023-09-18): elmbeech/physicelldataloader
    + rename pyMCDSts make\_imgsubs to **make_imgconc** for consistency.
    + add **man/lecture/20230917_pcdl_repl_programming_analysis_plots.pdf** slide deck.

+ version 3.2.12 (2023-08-12): elmbeech/physicelldataloader
    + add **man/jupyter/pcdl_repl_programming.ipynb** : Jupyter notebook to give an idea about how to work with pcdl in a python3 REPL.
    + add **man/lecture/20230808_pcws2023_session07_pcdl.pdf** slide deck.
    + add github **continuous integration** for all supported python3 versions, all supported operating systems.

+ version 3.2.11 (2023-08-08): elmbeech/physicelldataloader
    + **pip install pcdl**: will only install the bare minimum library dependencies.
    + **pip install pcdl[data]**: will install the minimum dependencies plus the dependencies to download the test dataset.
    + **pip install pcdl[scverse]**: will install the minimum dependencies plus the dependencies needed to generate an anndata object.
    + **pip install pcdl[all]**: will always install all dependencies.
    + new TimeSeries **get_annmcds_list** function, which points to the self.l\_annmcds object.
    + new pyMCDS **get_scatter** function is split off from pyMCDSts make\_imgcell.
    + pyMCDSts **make_imgcell** and **make_imgsubs** bug fixes.
    + TimeStep and TimeSeries **get_anndata** evolution.

+ version 3.2.10 (2023-07-24): elmbeech/physicelldataloader
    + rename pyMCDSts get\_cell\_df\_columns\_states to **get_cell_df_states** for conciseness.
    + rename pyMCDSts get\_conc\_df\_columns\_states to **get_conc_df_states** for conciseness.

+ version 3.2.9 (2023-07-23): elmbeech/physicelldataloader
    + new class **TimeStep** can do everything pyMCDS can do and more.
    + new class **TimeSeries** can do everything pyMCDSts can do and more.
    + new TimeStep **get_anndata** function to transform physicell output into [AnnData](https://anndata.readthedocs.io/en/latest/) objects.
    + new TimeSeries **get_anndata** function to transform physicell output into [AnnData](https://anndata.readthedocs.io/en/latest/) objects.
    + internal pyAnnData **scaler** function.
    + internal pyAnnData **\_anndextract** function.
    + pyMCDS **_\_init__** seetingxml parameter changed from boolean to string to accept other PhysiCell\_settings.xml filenames than the default.
    + pyMCDS **get_cell_df** drop and keep parameters to declare a set of columns to be dropped or kept.
    + pyMCDS **get_conc_df** drop and keep parameters to declare a set of columns to be dropped or kept.
    + new pyMCDS **get_conc_df** shorthand for get\_concentration\_df.
    + pyMCDSts get\_cell\_minstate\_col reimplementation as **get_cell_df_columns_states** function.
    + pyMCDSts get\_concentartion\_minstate\_col reimplementation as **get_conc_df_columns_states** function.
    + new pyMCDSts **get_mcds_list** function which points to the self.l\_mcds object.

+ version 3.2.8 (2023-06-21): elmbeech/physicelldataloader
    + pyMCDS **get_concentration_df** states parameter to filter out non-informative variables.
    + pyMCDS **get_cell_df** states parameter to filter out non-informative variables.
    + pyMCDSts **_\_init__** load parameter to specify if the whole time series data straight at object initialization should be loaded.
    + new pyMCDSts **get_cell_minstate_col** function to scan the whole time series for informative attributes.
    + new pyMCDSts **get_concentartion_minstate_col** function to scan the whole time series for informative attributes.

+ version 3.2.7 (2023-06-20): elmbeech/physicelldataloader
    + pyMCDS and pyMCDSts **_\_init__** custom\_type parameter to specify other custom\_data variable types (int, bool, str) then the generic float.

+ version 3.2.5 (2023-06-19): elmbeech/physicelldataloader
    + pyMCDS resolves incompatibility with earlier PhysiCell and MultiCellDS versions.

+ version 3.2.4 (2023-06-17): elmbeech/physicelldataloader
    + pyMCDS **_\_init__** seetingxml parameter for cases where in the output folder no PhysiCell\_settings.xml can be found.
    + pyMCDSts **mcdsts.make_imgcell** extrema parameter is replaced by the z\_axis parameter to account for numerical and categorical variable types.

+ version 3.2.2 (2023-06-16): elmbeech/physicelldataloader
    + pyMCDS **mcds.get_cell_df** sets distinct boolean, categorical, integer number, and real number variable types. categorical number codes are translated. for all spatial variables, the vector length value is calculated and added automatically.
    + new pyMCDS **mcds.get_celltype_dict** function.
    + new pyMCDS **mcds.get_substrate_dict** function.
    + pyMCDSts **mcdsts.make_imgcell** and **mcdsts.make_imgsubs** functions improved.

+ version 3.2.1 (2023-06-12): elmbeech/physicelldataloader
    + pypa odyssey is coming to an end.
    + change build system from setuptools to hatching.
    + change the library name from pcDataLoader to pcdl.
    + to make the library installation more lightweight, test data was excluded from the basic installation.
      given the computer is connected to the internet, test data can easily be installed and removed with the **pcdl.install_data()** and **pcdl.uninstall_data()** functions now.

+ version 3.0.7 (2023-06-08): elmbeech/physicelldataloader
    + pyMCDSts: replaces the svg dependent **mcdsts.make_jpeg**, **mcdsts.make_png**, and **mcdsts.make_tiff** with **mcdsts.make_imgcell** and **mcdsts.make_imgsubs** which generate images straight out of the loaded data. the **mcdsts.make_gif** and **mcdsts.make_movie** functions were adjusted accordingly. special thanks to Marshal Gress!
    + pyMCDSts: **mcdsts.read_mcds** loads now automatically all mcds snapshots if no xmlfile\_list is provided (default).

+ version 3.0.6 (2023-04-29): elmbeech/physicelldataloader
    + pyMCDS **\_read_xml** is now able to load time steps with zero cells.
    + pyMCDS **mcds.get_contour** can handle more input parameters.

+ version 3.0.5 (2023-02-26): elmbeech/physicelldataloader pyMCDS **mcds.get_contour**  plots span now the whole domain and not only to the border voxel centers.
+ version 3.0.4 (2023-02-21): elmbeech/physicelldataloader pyMCDS **mcds.get_contour** function, to easily generate for substrates matplotlib contourf and contour plots because they do not exist as pandas plots.
+ version 3.0.3 (2023-02-19): elmbeech/physicelldataloader branch 3 has no longer anndata and, as such, hdf5 dependency.
+ version 3.0.2 (2023-01-06): elmbeech/physicelldataloader bugfix installing package data.
+ version 3.0.0 (2023-01-06): elmbeech/physicelldataloader
    + **pyMCDS** parameter **xml_file** can now handle path/file.xml (unix) or path\file.xml (dos) input, as long output_path is the default.
    + **pyMCDS** has a new additional boolean **microenv** parameter, to specify if the microenvironment (substrates) should be read (for completeness) or not (for speed increase and less memory usage).
    + **pyMCDS** has a new additional boolean **graph** parameter, to specify if the attached and neighbor graph should be read.
    + **pyMCDS** has a new additional boolean **verbose** parameter, to specify if there should be text output while processing.
    + pyMCDS **mcds.get_2D_mesh** was renamed to **mcds.get_mesh_2D** for consistency.
    + pyMCDS **mcds.get_linear_voxels** was renamed to **mcds.get_mesh_coordinate** for consistency.
    + pyMCDS **mcds.get_containing_voxel_ijk** was renamed to **mcds.get_voxel_ijk** for briefness.
    + pyMCDS **mcds.get_voxel_spacing** returns now 3 specific values, one for x, y, and z, instead of 1 general value.
    + pyMCDS **mcds.get_concentrations** was renamed to **mcds.get_concentration** for consistency
    + pyMCDS **mcds.get_concentrations_at** was renamed to **mcds.get_concentration_at** for consistency
    + pyMCDS **mcds.get_concentration_at** if z_slice is not a mesh center value, the function will by default adjust to the nearest and no longer break.
    + pyMCDS **mcds.get_cell_variables** and **mcds.get_substrate_names** return now a strictly alphabetically ordered list.
    + pyMCDS **mcds.get_cell_df** returns now a pandas dataframe with the cell IDs as the index and not as a column.
      additionally, this dataframe contains now voxel, mesh_center, substrate parameter, substrate concentration, and cell density information too.
    + new pyMCDS **mcds.get_concentration_df** function.
    + new pyMCDS **mcds.get_substrate_df** function.
    + new pyMCDS **mcds.get_unit_se** function.
    + new pyMCDS **mcds.get_multicellds_version** function.
    + new pyMCDS **mcds.get_physicell_version** function.
    + new pyMCDS **mcds.get_runtime** function.
    + new pyMCDS **mcds.get_timestamp** function.
    + new pyMCDS **mcds.get_voxel_ijk_range** function.
    + new pyMCDS **mcds.get_voxel_ijk_axis** function.
    + new pyMCDS **mcds.get_voxel_spacing** function.
    + new pyMCDS **mcds.get_voxel_volume** function.
    + new pyMCDS **mcds.get_mesh_mnp_range** function.
    + new pyMCDS **mcds.get_mesh_mnp_axis** function.
    + new pyMCDS **mcds.get_xyz_range** function.
    + new pyMCDS **mcds.is_in_mesh** function.
    + new pyMCDS **mcds.get_attached_graph_dict** function.
    + new pyMCDS **mcds.get_neigbor_graph_dict** function.
    + class **pyMCDS_timeseries** was renamed to **pyMCDSts** and completely rewritten.
    + new pyMCDSts **get_xmlfile_list** function.
    + new pyMCDSts **read_mcds** function.
    + new pyMCDSts **make_jpeg** function.
    + new pyMCDSts **make_png** function.
    + new pyMCDSts **make_tiff** function.
    + new pyMCDSts **make_gif** function.
    + new pyMCDSts **make_movie** function.
    + all **plotting** functions were removed because pcdl only focuses on making the raw data in python3 easy to access for in-depth analysis.
    + cell position coordinates are now constantly labeled as **x,y,z**, mesh center coordinates as **m,n,p**, and voxel coordinates as **i,j,k**.
    + the underling [mcds object data dictionary structure](https://github.com/elmbeech/physicelldataloader/tree/master/man/img/physicelldataloader_data_dictionary_v3.0.0.png) has changed.
    + [pytest](https://en.wikipedia.org/wiki/Pytest) unit tests exist now for all pyMCDS and pyMCDSts functions.

+ version 2.0.3 (2023-06-16): elmbeech/physicelldataloader pypa odyssey is coming to an end.
+ version 2.0.2 (2023-01-06): elmbeech/physicelldataloader reset patch voxel spacing bugfix, so that branch2 is full compatible with branch1 again. use branch3 for a bugfixed version!
+ version 2.0.1 (2022-11-08): elmbeech/physicelldataloader beta release patch voxel spacing bugfix.
+ version 2.0.0 (2022-08-30): elmbeech/physicelldataloader pip installable release, derived from and compatible with PhysiCell-Tools/python-loader release 1.1.0 (2022-07-20).

+ version 1.1.1 (2022-07-01): elmbeech/physicelldataloader deprecated np.float replaced with np.float64.
+ version 1.1.0 (2022-05-09): Physicell-Tools/python-loader release compatible with pre-v1.10.x of PhysiCell.
+ version 1.0.1 (2020-01-25): Physicell-Tools/python-loader time-series related bug fix.
+ version 1.0.0 (2019-09-28): Physicell-Tools/python-loader first public release!
