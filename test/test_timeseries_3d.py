####
# title: test_timeseries_3d.py
#
# language: python3
# author: Elmar Bucher
# date: 2022-10-15
# license: BSD 3-Clause
#
# description:
#   pytest unit test library for the pcdl library TimeSeries class.
#   + https://docs.pytest.org/
#
#   note:
#   assert actual == expected, message
#   == value equality
#   is reference equality
#   pytest.approx for real values
#####


# load library
import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import pcdl
import shutil


# const
s_path_3d = str(pathlib.Path(pcdl.__file__).parent.resolve()/'output_3d')


## download test data ##
if not os.path.exists(s_path_3d):
    pcdl.install_data()


##################
# test for speed #
##################
# BUE: test functions are mirrored test_timeseries_2d.py

## data loading related functions ##

class TestTimeSeries3dInit(object):
    ''' tests for loading a pcdl.TimeSeries data set. '''

    def test_mcdsts_set_verbose_true(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, load=False, verbose=False)
        mcdsts.set_verbose_true()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (mcdsts.verbose)

    def test_mcdsts_set_verbose_false(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, load=False, verbose=True)
        mcdsts.set_verbose_false()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (not mcdsts.verbose)

    ## get_xmlfile and read_mcds command and get_mcds_list ##
    def test_mcdsts_get_xmlfile_list(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, load=False, verbose=True)
        ls_xmlfile = mcdsts.get_xmlfile_list()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_xmlfile[0] == 'output00000000.xml') and \
              (ls_xmlfile[-1] == 'output00000024.xml') and \
              (len(ls_xmlfile) == 25)

    def test_mcdsts_get_mcds_list(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, load=True, verbose=True)
        l_mcds = mcdsts.get_mcds_list()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(mcdsts.l_mcds[0])) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcdsts.l_mcds[-1])) == "<class 'pcdl.timestep.TimeStep'>") and \
              (mcdsts.l_mcds[0].get_time() == 0) and \
              (mcdsts.l_mcds[-1].get_time() == 1440) and \
              (len(mcdsts.l_mcds) == 25) and \
              (mcdsts.l_mcds == l_mcds)

    def test_mcdsts_read_mcds(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, load=False, verbose=True)
        l_mcds_loadfalse  = mcdsts.get_mcds_list()
        mcdsts.read_mcds()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(mcdsts.l_mcds[0])) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcdsts.l_mcds[-1])) == "<class 'pcdl.timestep.TimeStep'>") and \
              (mcdsts.l_mcds[0].get_time() == 0) and \
              (mcdsts.l_mcds[-1].get_time() == 1440) and \
              (len(mcdsts.l_mcds) == 25) and \
              (l_mcds_loadfalse is None)

    def test_mcdsts_read_mcds_xmlfilelist(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, load=False, verbose=True)
        ls_xmlfile = mcdsts.get_xmlfile_list()
        ls_xmlfile = ls_xmlfile[-3:]
        l_mcds = mcdsts.read_mcds(ls_xmlfile)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(mcdsts.l_mcds[0])) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcdsts.l_mcds[-1])) == "<class 'pcdl.timestep.TimeStep'>") and \
              (mcdsts.l_mcds[0].get_time() == 1320) and \
              (mcdsts.l_mcds[-1].get_time() == 1440) and \
              (len(ls_xmlfile) == 3) and \
              (len(mcdsts.l_mcds) == 3) and \
              (mcdsts.l_mcds == l_mcds)


## micro environment related functions ##

class TestTimeSeries3dMicroenv(object):
    ''' tests for pcdl.TimeStep micro environment related functions. '''
    mcdsts = pcdl.TimeSeries(s_path_3d, verbose=True)

    def test_mcdsts_get_conc_df(self, mcdsts=mcdsts):
        ldf_conc = mcdsts.get_conc_df(values=2, drop=set(), keep=set(), collapse=False)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(ldf_conc)) == "<class 'list'>") and \
              (str(type(ldf_conc[0])) == "<class 'pandas.core.frame.DataFrame'>") and \
              (ldf_conc[0].shape == (1331, 9)) and \
              (ldf_conc[-1].shape == (1331, 11)) and \
              (len(ldf_conc) == 25)

    def test_mcdsts_get_conc_df_collapse(self, mcdsts=mcdsts):
        df_conc = mcdsts.get_conc_df(values=2, drop=set(), keep=set(), collapse=True)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_conc.shape == (33275, 11))

    def test_mcdsts_get_conc_attribute(self, mcdsts=mcdsts):
        dl_conc = mcdsts.get_conc_attribute(values=1, drop=set(), keep=set(), allvalues=False)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(dl_conc)) == "<class 'dict'>") and \
              (str(type(dl_conc['oxygen'])) == "<class 'list'>") and \
              (str(type(dl_conc['oxygen'][0])) == "<class 'float'>") and \
              (len(dl_conc.keys()) == 2) and \
              (len(dl_conc['oxygen']) == 2)

    def test_mcdsts_get_conc_attribute_values(self, mcdsts=mcdsts):
        dl_conc = mcdsts.get_conc_attribute(values=2, drop=set(), keep=set(), allvalues=False)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(dl_conc)) == "<class 'dict'>") and \
              (str(type(dl_conc['oxygen'])) == "<class 'list'>") and \
              (str(type(dl_conc['oxygen'][0])) == "<class 'float'>") and \
              (len(dl_conc.keys()) == 2) and \
              (len(dl_conc['oxygen']) == 2)

    def test_mcdsts_get_conc_attribute_allvalues(self, mcdsts=mcdsts):
        dl_conc = mcdsts.get_conc_attribute(values=1, drop=set(), keep=set(), allvalues=True)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(dl_conc)) == "<class 'dict'>") and \
              (str(type(dl_conc['oxygen'])) == "<class 'list'>") and \
              (str(type(dl_conc['oxygen'][0])) == "<class 'float'>") and \
              (len(dl_conc.keys()) == 2) and \
              (len(dl_conc['oxygen']) > 2)

    ## plot_contour command ##
    def test_mcdsts_plot_contour_if(self, mcdsts=mcdsts):
        ls_pathfile = mcdsts.plot_contour(
            focus = 'oxygen',
            z_slice = -3.333,  # test if
            extrema = None,  # test if and for loop
            #alpha = 1,  # TimeStep
            #fill = True,  # TimeStep
            #cmap = 'viridis',  # TimeStep
            #title = '',  # test default
            #grid = True,  # TimeStep
            xlim = None,  # test if
            ylim = None,  # test if
            #xyequal = True,  # TimeStep
            figsizepx = None,  # test if
            ext = 'jpeg',
            figbgcolor = None,  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_pathfile[0].replace('\\','/').endswith('/pcdl/output_3d/conc_oxygen_z-5.0/output00000000_oxygen.jpeg')) and \
              (os.path.exists(ls_pathfile[0])) and \
              (os.path.getsize(ls_pathfile[0]) > 2**10) and \
              (ls_pathfile[-1].replace('\\','/').endswith('/pcdl/output_3d/conc_oxygen_z-5.0/output00000024_oxygen.jpeg')) and \
              (os.path.exists(ls_pathfile[-1])) and \
              (os.path.getsize(ls_pathfile[-1]) > 2**10) and \
              (len(ls_pathfile) == 25)
        for s_pathfile in ls_pathfile:
            os.remove(s_pathfile)

    def test_mcdsts_plot_contour_else(self, mcdsts=mcdsts):
        l_fig = mcdsts.plot_contour(
            focus = 'oxygen',
            z_slice = 0.0,  # jump over if
            extrema = [0, 38],  # jump over if
            #alpha = 1,  # TimeStep
            #fill = True,  # TimeStep
            #cmap = 'viridis',  # TimeStep
            title = 'abc',  # test non default
            #grid = True,  # TimeStep
            xlim = [-31, 301],  # jump over if
            ylim = [-21, 201],  # jump over if
            #xyequal = True,  # TimeStep
            figsizepx = [641, 481],  # test non even pixel
            ext = None,
            figbgcolor = 'yellow',  # jump over if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(l_fig[0])) == "<class 'matplotlib.figure.Figure'>") and \
              (str(type(l_fig[-1])) == "<class 'matplotlib.figure.Figure'>") and \
              (len(l_fig) == 25)
        plt.close()


    def test_mcdsts_make_conc_vtk(self, mcdsts=mcdsts):
        ls_pathfile = mcdsts.make_conc_vtk()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_pathfile[0].endswith('/pcdl/output_3d/output00000000_conc.vtr')) and \
              (ls_pathfile[-1].endswith('/pcdl/output_3d/output00000024_conc.vtr')) and \
              (os.path.exists(ls_pathfile[0])) and \
              (os.path.exists(ls_pathfile[-1])) and \
              (os.path.getsize(ls_pathfile[0]) > 2**10) and\
              (os.path.getsize(ls_pathfile[-1]) > 2**10) and\
              (len(ls_pathfile) == 25)
        for s_pathfile in ls_pathfile:
            os.remove(s_pathfile)


## cell related functions ##

class TestTimeSeries3dCell(object):
    ''' tests for pcdl.TimeStep cell related functions. '''
    mcdsts = pcdl.TimeSeries(s_path_3d, verbose=False)

    def test_mcdsts_get_cell_df(self, mcdsts=mcdsts):
        ldf_cell = mcdsts.get_cell_df(values=2, drop=set(), keep=set(), collapse=False)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(ldf_cell)) == "<class 'list'>") and \
              (str(type(ldf_cell[0])) == "<class 'pandas.core.frame.DataFrame'>") and \
              (ldf_cell[0].shape[0] > 9) and \
              (ldf_cell[0].shape[1] == 40) and \
              (ldf_cell[-1].shape[0] > 9) and \
              (ldf_cell[-1].shape[1] == 72) and \
              (len(ldf_cell) == 25)

    def test_mcdsts_get_cell_df_collapse(self, mcdsts=mcdsts):
        df_cell = mcdsts.get_cell_df(values=2, drop=set(), keep=set(), collapse=True)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 73)

    def test_mcdsts_get_cell_attribute(self, mcdsts=mcdsts):
        dl_cell = mcdsts.get_cell_attribute(values=1, drop=set(), keep=set(), allvalues=False)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(dl_cell)) == "<class 'dict'>") and \
              (str(type(dl_cell['dead'])) == "<class 'list'>") and \
              (str(type(dl_cell['dead'][0])) == "<class 'bool'>") and \
              (str(type(dl_cell['cell_count_voxel'])) == "<class 'list'>") and \
              (str(type(dl_cell['cell_count_voxel'][0])) == "<class 'int'>") and \
              (str(type(dl_cell['cell_density_micron3'])) == "<class 'list'>") and \
              (str(type(dl_cell['cell_density_micron3'][0])) == "<class 'float'>") and \
              (str(type(dl_cell['cell_type'])) == "<class 'list'>") and \
              (str(type(dl_cell['cell_type'][0])) == "<class 'str'>") and \
              (len(dl_cell.keys()) == 110) and \
              (len(dl_cell['dead']) == 2) and \
              (len(dl_cell['cell_count_voxel']) == 2) and \
              (len(dl_cell['cell_density_micron3']) == 2) and \
              (len(dl_cell['cell_type']) == 2)

    def test_mcdsts_get_cell_attribute_values(self, mcdsts=mcdsts):
        dl_cell = mcdsts.get_cell_attribute(values=2, drop=set(), keep=set(), allvalues=False)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(dl_cell)) == "<class 'dict'>") and \
              (len(dl_cell.keys()) == 60)

    def test_mcdsts_get_cell_attribute_allvalues(self, mcdsts=mcdsts):
        dl_cell = mcdsts.get_cell_attribute(values=1, drop=set(), keep=set(), allvalues=True)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(dl_cell)) == "<class 'dict'>") and \
              (str(type(dl_cell['dead'])) == "<class 'list'>") and \
              (str(type(dl_cell['dead'][0])) == "<class 'bool'>") and \
              (str(type(dl_cell['cell_count_voxel'])) == "<class 'list'>") and \
              (str(type(dl_cell['cell_count_voxel'][0])) == "<class 'int'>") and \
              (str(type(dl_cell['cell_density_micron3'])) == "<class 'list'>") and \
              (str(type(dl_cell['cell_density_micron3'][0])) == "<class 'float'>") and \
              (str(type(dl_cell['cell_type'])) == "<class 'list'>") and \
              (str(type(dl_cell['cell_type'][0])) == "<class 'str'>") and \
              (len(dl_cell.keys()) == 110) and \
              (len(dl_cell['dead']) == 2) and \
              (len(dl_cell['cell_count_voxel']) > 2) and \
              (len(dl_cell['cell_density_micron3']) > 2) and \
              (len(dl_cell['cell_type']) == 2)

    ## plot_scatter command ##
    def test_mcdsts_plot_scatter_num(self, mcdsts=mcdsts):
        ls_pathfile = mcdsts.plot_scatter(
            focus='pressure',  # case numeric
            z_slice = -3.333,   # test if
            z_axis = None,  # test iff numeric
            #alpha = 1,  # matplotlib
            #cmap = 'viridis',  # matplotlib
            #title = '',  # test default,
            #grid = True,  # matplotlib
            #legend_loc='lower left',  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            #xyequal = True,  # TimeStep
            s = None,  # test if
            figsizepx = None,  # case extract from initial.svg
            ext = 'jpeg',
            figbgcolor = None,  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_pathfile[0].replace('\\','/').endswith('/pcdl/output_3d/cell_pressure_z-5.0/output00000000_pressure.jpeg')) and \
              (os.path.exists(ls_pathfile[0])) and \
              (os.path.getsize(ls_pathfile[0]) > 2**10) and \
              (ls_pathfile[-1].replace('\\','/').endswith('/pcdl/output_3d/cell_pressure_z-5.0/output00000024_pressure.jpeg')) and \
              (os.path.exists(ls_pathfile[-1])) and \
              (os.path.getsize(ls_pathfile[-1]) > 2**10) and \
              (len(ls_pathfile) == 25)
        for s_pathfile in ls_pathfile:
            os.remove(s_pathfile)

    def test_mcdsts_plot_scatter_cat(self, mcdsts=mcdsts):
        l_fig = mcdsts.plot_scatter(
            focus='cell_type',  # case categorical
            z_slice = 0.0,   # jump over if
            z_axis = None,  # test iff  categorical
            #alpha = 1,  # TimeStep
            #cmap = 'viridis',  # TimeStep
            title = 'abc',  # test non default
            #grid = True,  # TimeStep
            #legend_loc='lower left',  # TimeStep
            xlim = None,  # test if
            ylim = None,  # test if
            #xyequal = True,  # TimeStep
            s = None,  # test if
            figsizepx = [641, 481],  # test case non even pixel number
            ext = None,
            figbgcolor = 'cyan',  # jump over if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(l_fig[0])) == "<class 'matplotlib.figure.Figure'>") and \
              (str(type(l_fig[-1])) == "<class 'matplotlib.figure.Figure'>") and \
              (len(l_fig) == 25)
        plt.close()

    def test_mcdsts_make_cell_vtk(self, mcdsts=mcdsts):
        ls_pathfile = mcdsts.make_cell_vtk()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_pathfile[0].endswith('/pcdl/output_3d/output00000000_cell.vtp')) and \
              (ls_pathfile[-1].endswith('/pcdl/output_3d/output00000024_cell.vtp')) and \
              (os.path.exists(ls_pathfile[0])) and \
              (os.path.exists(ls_pathfile[-1])) and \
              (os.path.getsize(ls_pathfile[0]) > 2**10) and\
              (os.path.getsize(ls_pathfile[-1]) > 2**10) and\
              (len(ls_pathfile) == 25)
        for s_pathfile in ls_pathfile:
            os.remove(s_pathfile)


## graph related functions ##
class TestTimeSeries3dGraph(object):
    ''' tests for pcdl.TimeStep graph related functions. '''
    mcdsts = pcdl.TimeSeries(s_path_3d, verbose=False)

    ## graph related functions ##
    def test_mcdsts_get_graph_gml_attached_defaultattr(self, mcdsts=mcdsts):
        ls_pathfile = mcdsts.make_graph_gml(graph_type='attached', edge_attribute=True, node_attribute=[])
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_pathfile[0].endswith('/pcdl/output_3d/output00000000_attached.gml')) and \
              (ls_pathfile[-1].endswith('/pcdl/output_3d/output00000024_attached.gml')) and \
              (os.path.exists(ls_pathfile[0])) and \
              (os.path.exists(ls_pathfile[-1])) and \
              (len(ls_pathfile) == 25)
        for s_pathfile in ls_pathfile:
            os.remove(s_pathfile)

    def test_mcdsts_get_graph_gml_neighbor_noneattr(self, mcdsts=mcdsts):
        ls_pathfile = mcdsts.make_graph_gml(graph_type='neighbor', edge_attribute=False, node_attribute=[])
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_pathfile[0].endswith('/pcdl/output_3d/output00000000_neighbor.gml')) and \
              (ls_pathfile[-1].endswith('/pcdl/output_3d/output00000024_neighbor.gml')) and \
              (os.path.exists(ls_pathfile[0])) and \
              (os.path.exists(ls_pathfile[-1])) and \
              (len(ls_pathfile) == 25)
        for s_pathfile in ls_pathfile:
            os.remove(s_pathfile)

    def test_mcdsts_get_graph_gml_neighbor_allattr(self, mcdsts=mcdsts):
        ls_pathfile = mcdsts.make_graph_gml(graph_type='neighbor', edge_attribute=True, node_attribute=['dead','cell_count_voxel','cell_density_micron3','cell_type'])
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (ls_pathfile[0].endswith('/pcdl/output_3d/output00000000_neighbor.gml')) and \
              (ls_pathfile[-1].endswith('/pcdl/output_3d/output00000024_neighbor.gml')) and \
              (os.path.exists(ls_pathfile[0])) and \
              (os.path.exists(ls_pathfile[-1])) and \
              (len(ls_pathfile) == 25)
        for s_pathfile in ls_pathfile:
            os.remove(s_pathfile)

## ome.tiff related functions ##
class TestTimeSeries3dOmeTiff(object):
    ''' tests for pcdl.TimeStep graph related functions. '''
    mcdsts = pcdl.TimeSeries(s_path_3d, verbose=False)

    ## graph related functions ##
    def test_mcdsts_make_ome_tiff_defaultattr_00(self, mcdsts=mcdsts):
        la_ometiff = mcdsts.make_ome_tiff(cell_attribute='ID', conc_cutoff={}, focus=None, file=False, collapse=False)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (type(la_ometiff) is list) and \
              (type(la_ometiff[0]) is np.ndarray) and \
              (type(la_ometiff[-1]) is np.ndarray) and \
              (la_ometiff[0].dtype == np.float32) and \
              (la_ometiff[-1].dtype == np.float32) and \
              (la_ometiff[0].shape == (4, 11, 200, 300)) and \
              (la_ometiff[-1].shape ==  (4, 11, 200, 300)) and \
              (len(la_ometiff) == 25)

    def test_mcdsts_make_ome_tiff_defaultattr_01(self, mcdsts=mcdsts):
        a_ometiff = mcdsts.make_ome_tiff(cell_attribute='ID', conc_cutoff={}, focus=None, file=False, collapse=True)
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (type(a_ometiff) is np.ndarray) and \
              (a_ometiff.dtype == np.float32) and \
              (a_ometiff.shape == (25, 4, 11, 200, 300))


## time series related functions ##

class TestTimeSeries3dTimeseries(object):
    ''' tests for pcdl.TimeStep graph related functions. '''
    mcdsts = pcdl.TimeSeries(s_path_3d, verbose=False)

    ## plot_timeseries command ##
    def test_mcdsts_plot_timeseries_none_none_none_cell_ax_jpeg(self, mcdsts=mcdsts):
        fig, ax = plt.subplots()
        s_pathfile = mcdsts.plot_timeseries(
            focus_cat = None,  # test if {None/total, 'cell_type'}
            focus_num = None,  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'cell',  # test if else {'df_cell', 'df_conc'}
            z_slice = None,  # test timeseries
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True, # pandas
            yunit = None,  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = ax,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = 'jpeg',  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (s_pathfile.endswith('/pcdl/output_3d/timeseries_cell_total_count.jpeg')) and \
              (os.path.exists(s_pathfile))
        os.remove(s_pathfile)

    def test_mcdsts_plot_timeseries_cat_none_yunit_cell(self, mcdsts=mcdsts):
        fig = mcdsts.plot_timeseries(
            focus_cat = 'cell_type',  # test if {None/total, 'cell_type'}
            focus_num = None,  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'df_cell',  # test if else {'df_cell', 'df_conc'}
            z_slice = -0.3,  # test if if
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True,
            yunit = 'mmHg',  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = None,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = None,  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcdsts_plot_timeseries_none_num_yunit_cell(self, mcdsts=mcdsts):
        fig = mcdsts.plot_timeseries(
            focus_cat = None,  # test if {None/total, 'cell_type'}
            focus_num = 'oxygen',  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'df_cell',  # test if else {'df_cell', 'df_conc'}
            z_slice = -0.3,  # test if if
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True,
            yunit = 'mmHg',  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = None,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = None,  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcdsts_plot_timeseries_cat_num_none_cell(self, mcdsts=mcdsts):
        fig = mcdsts.plot_timeseries(
            focus_cat = 'cell_type',  # test if {None/total, 'cell_type'}
            focus_num = 'oxygen',  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'cell',  # test if else {'df_cell', 'df_conc'}
            z_slice = -0.3,  # test if if
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True,
            yunit = None,  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = None,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = None,  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcdsts_plot_timeseries_none_none_none_conc_ax_jpeg(self, mcdsts=mcdsts):
        fig, ax = plt.subplots()
        s_pathfile = mcdsts.plot_timeseries(
            focus_cat = None,  # test if {None/total, 'voxel_i'}
            focus_num = None,  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'conc',  # test if else {'df_cell', 'df_conc'}
            z_slice = None,  # test timeseries
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True,
            yunit = None,  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = ax,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = 'jpeg',  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (s_pathfile.endswith('/pcdl/output_3d/timeseries_conc_total_count.jpeg')) and \
              (os.path.exists(s_pathfile))
        os.remove(s_pathfile)
        plt.close()

    def test_mcdsts_plot_timeseries_cat_none_yunit_conc(self, mcdsts=mcdsts):
        fig = mcdsts.plot_timeseries(
            focus_cat = 'voxel_i',  # test if {None/total, 'voxel_i'}
            focus_num = None,  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'df_conc',  # test if else {'df_cell', 'df_conc'}
            z_slice = -0.3,  # test if if
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True,
            yunit = 'mmHg',  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = None,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = None,  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcdsts_plot_timeseries_none_num_yunit_conc(self, mcdsts=mcdsts):
        fig = mcdsts.plot_timeseries(
            focus_cat = None,  # test if {None/total, 'voxel_i'}
            focus_num = 'oxygen',  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'df_conc',  # test if else {'df_cell', 'df_conc'}
            z_slice = -0.3,  # test if if
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True,
            yunit = 'mmHg',  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = None,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = None,  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcdsts_plot_timeseries_cat_num_none_conc(self, mcdsts=mcdsts):
        fig = mcdsts.plot_timeseries(
            focus_cat = 'voxel_i',  # test if {None/total, 'voxel_i'}
            focus_num = 'oxygen',  # test if {None/count, 'oxygen'}
            #aggregate_num = np.mean,  # pandas
            frame = 'conc',  # test if else {'df_cell', 'df_conc'}
            z_slice = -0.3,  # test if if
            #logy = False,  # pandas
            #ylim = None,  # pandas
            #secondary_y = None,  # pandas
            #subplots = False,  # pandas
            #sharex = False,  # pandas
            #sharey = False,  # pandas
            #linestyle = '-',  # pandas
            #linewidth = None,  # pandas
            #cmap = None,  # pandas
            #color = None,  # pandas
            #grid = True,  # pandas
            #legend = True,
            yunit = None,  # test if {None, 'mmHg'}
            #title = None, pandas
            ax = None,  # test if else {None, ax}
            figsizepx = [641, 481],  # test non even pixel number
            ext = None,  # test if else {'jpeg', None}
            figbgcolor = None  # test if
        )
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()


## anndata time series related functions ##
class TestTimeSeries3dAnnData(object):
    ''' test for pcdl.TestSeries class. '''

    # get_anndata
    # get_annmcds_list {integrated}
    # value {1, _2_}
    # collaps {True, _False_}
    # keep_mcds {True, _False_}

    ## get_anndata command ##
    def test_mcdsts_get_anndata(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, verbose=True)
        ann = mcdsts.get_anndata(values=1, drop=set(), keep=set(), scale='maxabs', collapse=True, keep_mcds=True)
        l_annmcds = mcdsts.get_annmcds_list()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (len(mcdsts.l_mcds) == 25) and \
              (l_annmcds == mcdsts.l_annmcds) and \
              (mcdsts.l_annmcds is None) and \
              (str(type(ann)) == "<class 'anndata._core.anndata.AnnData'>") and \
              (ann.X.shape[0] > 9) and \
              (ann.X.shape[1] == 105) and \
              (ann.obs.shape[0] > 9) and \
              (ann.obs.shape[1] == 8) and \
              (ann.obsm['spatial'].shape[0] > 9) and \
              (ann.obsm['spatial'].shape[1] == 3) and \
              (len(ann.obsp) == 0) and \
              (ann.var.shape == (105, 0)) and \
              (len(ann.uns) == 0)

    def test_mcdsts_get_anndata_value(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, verbose=True)
        ann = mcdsts.get_anndata(values=2, drop=set(), keep=set(), scale='maxabs', collapse=True, keep_mcds=True)
        l_annmcds = mcdsts.get_annmcds_list()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (len(mcdsts.l_mcds) == 25) and \
              (l_annmcds == mcdsts.l_annmcds) and \
              (mcdsts.l_annmcds is None) and \
              (str(type(ann)) == "<class 'anndata._core.anndata.AnnData'>") and \
              (ann.X.shape[0] > 9) and \
              (ann.X.shape[1] == 56) and \
              (ann.obs.shape[0] > 9) and \
              (ann.obs.shape[1] == 7) and \
              (ann.obsm['spatial'].shape[0] > 9) and \
              (ann.obsm['spatial'].shape[1] == 3) and \
              (len(ann.obsp) == 0) and \
              (ann.var.shape == (56, 0)) and \
              (len(ann.uns) == 0)

    def test_mcdsts_get_anndata_collapsefalse(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, verbose=True)
        ann = mcdsts.get_anndata(values=1, drop=set(), keep=set(), scale='maxabs', collapse=False, keep_mcds=True)
        l_annmcds = mcdsts.get_annmcds_list()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (len(mcdsts.l_mcds) == 25) and \
              (l_annmcds == mcdsts.l_annmcds) and \
              (str(type(mcdsts.l_annmcds)) == "<class 'list'>") and \
              (len(mcdsts.l_annmcds) == 25) and \
              (all([str(type(ann)) == "<class 'anndata._core.anndata.AnnData'>" for ann in mcdsts.l_annmcds])) and \
              (mcdsts.l_annmcds[24].X.shape[0] > 9) and \
              (mcdsts.l_annmcds[24].X.shape[1] == 105) and \
              (mcdsts.l_annmcds[24].obs.shape[0] > 9) and \
              (mcdsts.l_annmcds[24].obs.shape[1] == 7) and \
              (mcdsts.l_annmcds[24].obsm['spatial'].shape[0] > 9) and \
              (mcdsts.l_annmcds[24].obsm['spatial'].shape[1] == 3) and \
              (len(mcdsts.l_annmcds[24].obsp) == 4) and \
              (mcdsts.l_annmcds[24].var.shape == (105, 0)) and \
              (len(mcdsts.l_annmcds[24].uns) == 2)

    def test_mcdsts_get_anndata_keepmcdsfalse(self):
        mcdsts = pcdl.TimeSeries(s_path_3d, verbose=True)
        ann = mcdsts.get_anndata(values=1, drop=set(), keep=set(), scale='maxabs', collapse=True, keep_mcds=False)
        l_annmcds = mcdsts.get_annmcds_list()
        assert(str(type(mcdsts)) == "<class 'pcdl.timeseries.TimeSeries'>") and \
              (len(mcdsts.l_mcds) == 0) and \
              (l_annmcds == mcdsts.l_annmcds) and \
              (mcdsts.l_annmcds is None) and \
              (str(type(ann)) == "<class 'anndata._core.anndata.AnnData'>") and \
              (ann.X.shape[0] > 9) and \
              (ann.X.shape[1] == 105) and \
              (ann.obs.shape[0] > 9) and \
              (ann.obs.shape[1] == 8) and \
              (ann.obsm['spatial'].shape[0] > 9) and \
              (ann.obsm['spatial'].shape[1] == 3) and \
              (len(ann.obsp) == 0) and \
              (ann.var.shape == (105, 0)) and \
              (len(ann.uns) == 0)

