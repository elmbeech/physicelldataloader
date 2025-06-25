#####
# title: test_snapshot_2d.py
#
# language: python3
# author: Elmar Bucher
# date: 2022-10-15
# license: BSD 3-Clause
#
# description:
#   pytest unit test library for the pcdl library TimeStep class.
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
import pandas as pd
import pathlib
import pcdl


# const
s_path_2d = str(pathlib.Path(pcdl.__file__).parent.resolve()/'output_2d')
s_file_2d = 'output00000024.xml'
s_pathfile_2d = f'{s_path_2d}/{s_file_2d}'


## download test dataset ##
if not os.path.exists(s_path_2d):
    pcdl.install_data()


# const
s_path_2d = str(pathlib.Path(pcdl.__file__).parent.resolve()/'output_2d')
s_file_2d = 'output00000024.xml'
s_pathfile_2d = f'{s_path_2d}/{s_file_2d}'


# test data
if not os.path.exists(s_path_2d):
    pcdl.install_data()


## data loading related functions ##

class TestTimeStepInit(object):
    ''' tests for loading a pcdl.TimeStep data set. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)
    df_cell = mcds.get_cell_df()
    def test_mcds_init_microenv(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)

    def test_mcds_init_graph(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcds.data['cell']['dei_graph']['attached_cells'])) == "<class 'dict'>") and \
              (str(type(mcds.data['cell']['dei_graph']['neighbor_cells'])) == "<class 'dict'>") and \
              (len(mcds.data['cell']['dei_graph']['attached_cells']) > 9) and \
              (len(mcds.data['cell']['dei_graph']['neighbor_cells']) > 9)

    #def test_mcds_init_physiboss(self, mcds=mcds):
    #    assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
    #          (mcds.data['cell']['physiboss'] == None)

    def test_mcds_init_settingxml(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (set(df_cell.columns).issuperset({'default_fusion_rates'})) and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)


class TestTimeStepInitMicroenvFalse(object):
    ''' tests for loading a pcdl.TimeStep data set with microenv false. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=False, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)
    df_cell = mcds.get_cell_df()
    def test_mcds_init_microenv(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 116)

    def test_mcds_init_graph(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcds.data['cell']['dei_graph']['attached_cells'])) == "<class 'dict'>") and \
              (str(type(mcds.data['cell']['dei_graph']['neighbor_cells'])) == "<class 'dict'>") and \
              (len(mcds.data['cell']['dei_graph']['attached_cells']) > 9) and \
              (len(mcds.data['cell']['dei_graph']['neighbor_cells']) > 9)

    #def test_mcds_init_physiboss(self, mcds=mcds):
    #    assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
    #          (mcds.data['cell']['physiboss'] == None)

    def test_mcds_init_settingxml(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (set(df_cell.columns).issuperset({'default_fusion_rates'})) and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 116)


class TestTimeStepInitGraphFalse(object):
    ''' tests for loading a pcdl.TimeStep data set with graph false. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=False, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)
    df_cell = mcds.get_cell_df()
    def test_mcds_init_microenv(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)

    def test_mcds_init_graph(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcds.data['cell']['dei_graph']['attached_cells'])) == "<class 'dict'>") and \
              (str(type(mcds.data['cell']['dei_graph']['neighbor_cells'])) == "<class 'dict'>") and \
              (len(mcds.data['cell']['dei_graph']['attached_cells']) == 0) and \
              (len(mcds.data['cell']['dei_graph']['neighbor_cells']) == 0)

    #def test_mcds_init_physiboss(self, mcds=mcds):
    #    assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
    #          (mcds.data['cell']['physiboss'] == None)

    def test_mcds_init_settingxml(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (set(df_cell.columns).issuperset({'default_fusion_rates'})) and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)


class TestTimeStepInitPhysibossFalse(object):
    ''' tests for loading a pcdl.TimeStep data set with physiboss false. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=False, settingxml='PhysiCell_settings.xml', verbose=True)
    df_cell = mcds.get_cell_df()
    def test_mcds_init_microenv(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)

    def test_mcds_init_graph(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcds.data['cell']['dei_graph']['attached_cells'])) == "<class 'dict'>") and \
              (str(type(mcds.data['cell']['dei_graph']['neighbor_cells'])) == "<class 'dict'>") and \
              (len(mcds.data['cell']['dei_graph']['attached_cells']) > 9) and \
              (len(mcds.data['cell']['dei_graph']['neighbor_cells']) > 9)

    #def test_mcds_init_physiboss(self, mcds=mcds):
    #    assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
    #          (mcds.data['cell']['physiboss'] == None)

    def test_mcds_init_settingxml(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (set(df_cell.columns).issuperset({'default_fusion_rates'})) and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)


class TestTimeStepInitSettingxmlFalse(object):
    ''' tests for loading a pcdl.TimeStep data set with settingxml false. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml=False, verbose=True)
    df_cell = mcds.get_cell_df()
    def test_mcds_init_microenv(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)

    def test_mcds_init_graph(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcds.data['cell']['dei_graph']['attached_cells'])) == "<class 'dict'>") and \
              (str(type(mcds.data['cell']['dei_graph']['neighbor_cells'])) == "<class 'dict'>") and \
              (len(mcds.data['cell']['dei_graph']['attached_cells']) > 9) and \
              (len(mcds.data['cell']['dei_graph']['neighbor_cells']) > 9)

    #def test_mcds_init_physiboss(self, mcds=mcds):
    #    assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
    #          (mcds.data['cell']['physiboss'] == None)

    def test_mcds_init_settingxml(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (set(df_cell.columns).issuperset({'default_fusion_rates'})) and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)


class TestTimeStepInitSettingxmlNone(object):
    ''' tests for loading a pcdl.TimeStep data set with settingxml none. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml=None, verbose=True)
    df_cell = mcds.get_cell_df()
    def test_mcds_init_microenv(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)

    def test_mcds_init_graph(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(mcds.data['cell']['dei_graph']['attached_cells'])) == "<class 'dict'>") and \
              (str(type(mcds.data['cell']['dei_graph']['neighbor_cells'])) == "<class 'dict'>") and \
              (len(mcds.data['cell']['dei_graph']['attached_cells']) > 9) and \
              (len(mcds.data['cell']['dei_graph']['neighbor_cells']) > 9)

    #def test_mcds_init_physiboss(self, mcds=mcds):
    #    assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
    #          (mcds.data['cell']['physiboss'] == None)

    def test_mcds_init_settingxml(self, mcds=mcds, df_cell=df_cell):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (set(df_cell.columns).issuperset({'default_fusion_rates'})) and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)


class TestTimeStepInitVerboseTrue(object):
    ''' tests for loading a pcdl.TimeStep data set and set_verbose_false function. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    def test_mcds_verbose_true(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (mcds.verbose)

    def test_mcds_set_verbose_false(self, mcds=mcds):
        mcds.set_verbose_false()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (not mcds.verbose)


class TestTimeStepInitVerboseFalse(object):
    ''' tests for loading a pcdl.TimeStep data set and set_verbose_true function. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=False)

    def test_mcds_verbose_false(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (not mcds.verbose)

    def test_mcds_set_verbose_true(self, mcds=mcds):
        mcds.set_verbose_true()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (mcds.verbose)


## metadata related functions ##

class TestTimeStepMetadata(object):
    ''' tests for pcdl.TimeStep metadata related functions. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    def test_mcds_get_multicellds_version(self, mcds=mcds):
        s_mcdsversion = mcds.get_multicellds_version()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(s_mcdsversion)) == "<class 'str'>") and \
              (s_mcdsversion == 'MultiCellDS_2')

    def test_mcds_get_physicell_version(self, mcds=mcds):
        s_pcversion = mcds.get_physicell_version()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(s_pcversion)) == "<class 'str'>") and \
              (s_pcversion == 'PhysiCell_1.14.1')

    def test_mcds_get_timestamp(self, mcds=mcds):
        s_timestamp = mcds.get_timestamp()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(s_timestamp)) == "<class 'str'>") and \
              (s_timestamp == '2025-01-05T08:08:22Z')

    def test_mcds_get_time(self, mcds=mcds):
        r_time = mcds.get_time()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(r_time)) == "<class 'float'>") and \
              (r_time == 1440.0)

    def test_mcds_get_runtime(self, mcds=mcds):
        r_runtime = mcds.get_runtime()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(r_runtime)) == "<class 'float'>") and \
              (r_runtime == 1.952156)


## setting related functions ##

class TestTimeStepSetting(object):
    ''' tests for pcdl.TimeStep setting related functions. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    def test_mcds_get_unit_dict(self, mcds=mcds):
        ds_unit = mcds.get_unit_dict()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ds_unit)) == "<class 'dict'>") and \
              (len(ds_unit) == 108) and \
              (ds_unit['oxygen'] == 'dimensionless')


## mesh related functions ##

class TestTimeStepMesh(object):
    ''' tests for pcdl.TimeStep mesh related functions. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    def test_mcds_get_voxel_ijk_range(self, mcds=mcds):
        lti_range = mcds.get_voxel_ijk_range()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(lti_range)) == "<class 'list'>") and \
              (str(type(lti_range[0])) == "<class 'tuple'>") and \
              (str(type(lti_range[0][0])) == "<class 'int'>") and \
              (lti_range == [(0, 10), (0, 10), (0, 0)])

    def test_mcds_get_mesh_mnp_range(self, mcds=mcds):
        ltr_range = mcds.get_mesh_mnp_range()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ltr_range)) == "<class 'list'>") and \
              (str(type(ltr_range[0])) == "<class 'tuple'>") and \
              (str(type(ltr_range[0][0])) == "<class 'numpy.float64'>") and \
              (ltr_range == [(-15, 285), (-10, 190), (0, 0)])

    def test_mcds_get_xyz_range(self, mcds=mcds):
        ltr_range = mcds.get_xyz_range()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ltr_range)) == "<class 'list'>") and \
              (str(type(ltr_range[0])) == "<class 'tuple'>") and \
              (str(type(ltr_range[0][0])) == "<class 'numpy.float64'>") and \
              (ltr_range == [(-30, 300), (-20, 200), (-5, 5)])

    def test_mcds_get_voxel_ijk_axis(self, mcds=mcds):
        lai_axis = mcds.get_voxel_ijk_axis()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(lai_axis)) == "<class 'list'>") and \
              (str(type(lai_axis[0])) == "<class 'numpy.ndarray'>") and \
              (str(type(lai_axis[0][0])).startswith("<class 'numpy.int")) and \
              (len(lai_axis) == 3) and \
              (lai_axis[0].shape == (11,)) and \
              (lai_axis[1].shape == (11,)) and \
              (lai_axis[2].shape == (1,))

    def test_mcds_get_mesh_mnp_axis(self, mcds=mcds):
        lar_axis = mcds.get_mesh_mnp_axis()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(lar_axis)) == "<class 'list'>") and \
              (str(type(lar_axis[0])) == "<class 'numpy.ndarray'>") and \
              (str(type(lar_axis[0][0])) == "<class 'numpy.float64'>") and \
              (len(lar_axis) == 3) and \
              (lar_axis[0].shape == (11,)) and \
              (lar_axis[1].shape == (11,)) and \
              (lar_axis[2].shape == (1,))

    def test_mcds_get_mesh_flat_false(self, mcds=mcds):
        aar_mesh = mcds.get_mesh(flat=False)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(aar_mesh)) == "<class 'numpy.ndarray'>") and \
              (aar_mesh.dtype == np.float64) and \
              (aar_mesh.shape == (3, 11, 11, 1))

    def test_mcds_get_mesh_flat_true(self, mcds=mcds):
        aar_mesh = mcds.get_mesh(flat=True)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(aar_mesh)) == "<class 'numpy.ndarray'>") and \
              (aar_mesh.dtype == np.float64) and \
              (aar_mesh.shape == (2, 11, 11))

    def test_mcds_get_mesh_2d(self, mcds=mcds):
        aar_mesh_flat = mcds.get_mesh(flat=True)
        aar_mesh_2d = mcds.get_mesh_2D()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(aar_mesh_2d)) == "<class 'numpy.ndarray'>") and \
              (aar_mesh_2d.dtype == np.float64) and \
              (aar_mesh_2d.shape == (2, 11, 11))

    def test_mcds_get_mesh_coordinate(self, mcds=mcds):
        # cube coordinates
        ar_m_cube, ar_n_cube, ar_p_cube = mcds.get_mesh(flat=False)
        er_m_cube = set(ar_m_cube.flatten())
        er_n_cube = set(ar_n_cube.flatten())
        er_p_cube = set(ar_p_cube.flatten())
        # linear coordinates
        aar_voxel = mcds.get_mesh_coordinate()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(aar_voxel)) == "<class 'numpy.ndarray'>") and \
              (aar_voxel.dtype == np.float64) and \
              (aar_voxel.shape == (3, 121)) and \
              (set(aar_voxel[0]) == er_m_cube) and \
              (set(aar_voxel[1]) == er_n_cube) and \
              (set(aar_voxel[2]) == er_p_cube)

    def test_mcds_get_voxel_volume(self, mcds=mcds):
        r_volume = mcds.get_voxel_volume()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(r_volume)) == "<class 'numpy.float64'>") and \
              (r_volume == 6000.0)

    # bue: check else in 3D
    def test_mcds_get_mesh_spacing(self, mcds=mcds):
        lr_spacing = mcds.get_mesh_spacing()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(lr_spacing)) == "<class 'list'>") and \
              (str(type(lr_spacing[0])) == "<class 'numpy.float64'>") and \
              (str(type(lr_spacing[1])) == "<class 'numpy.float64'>") and \
              (str(type(lr_spacing[-1])) == "<class 'numpy.float64'>") and \
              (lr_spacing == [30.0, 20.0, 10.0])

    def test_mcds_get_voxel_spacing(self, mcds=mcds):
        lr_spacing = mcds.get_voxel_spacing()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(lr_spacing)) == "<class 'list'>") and \
              (str(type(lr_spacing[0])) == "<class 'numpy.float64'>") and \
              (str(type(lr_spacing[-1])) == "<class 'numpy.float64'>") and \
              (lr_spacing == [30.0, 20.0, 10.0])

    def test_mcds_is_in_mesh(self, mcds=mcds):
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (mcds.is_in_mesh(x=0, y=0, z=0, halt=False)) and \
              (not mcds.is_in_mesh(x=301, y=0, z=0, halt=False)) and \
              (not mcds.is_in_mesh(x=0, y=201, z=0, halt=False)) and \
              (not mcds.is_in_mesh(x=0, y=0, z=6, halt=False))

    def test_mcds_get_mesh_mnp(self, mcds=mcds):
        li_mesh_0 = mcds.get_mesh_mnp(x=0, y=0, z=0, is_in_mesh=True) # if b_calc
        li_mesh_1 = mcds.get_mesh_mnp(x=15, y=10, z=0, is_in_mesh=True) # if b_calc
        li_mesh_2 = mcds.get_mesh_mnp(x=30, y=20, z=0, is_in_mesh=True) # if b_calc
        li_mesh_none = mcds.get_mesh_mnp(x=-31, y=-21, z=-6, is_in_mesh=True) # else b_calc
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(li_mesh_0)) == "<class 'list'>") and \
              (str(type(li_mesh_0[0])) == "<class 'numpy.float64'>") and \
              (li_mesh_0 == [-15.0, -10.0, 0.0]) and \
              (li_mesh_1 == [15.0, 10.0, 0.0]) and \
              (li_mesh_2 == [15.0, 10.0, 0.0]) and \
              (li_mesh_none is None)

    def test_mcds_get_voxel_ijk(self, mcds=mcds):
        li_voxel_0 = mcds.get_voxel_ijk(x=0, y=0, z=0, is_in_mesh=True) # if b_calc
        li_voxel_1 = mcds.get_voxel_ijk(x=15, y=10, z=0, is_in_mesh=True) # if b_calc
        li_voxel_2 = mcds.get_voxel_ijk(x=30, y=20, z=0, is_in_mesh=True) # if b_calc
        li_voxel_none = mcds.get_voxel_ijk(x=-31, y=-21, z=-6, is_in_mesh=True) # else b_calc
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(li_voxel_0)) == "<class 'list'>") and \
              (str(type(li_voxel_0[0])) == "<class 'int'>") and \
              (li_voxel_0 == [0, 0, 0]) and \
              (li_voxel_1 == [1, 1, 0]) and \
              (li_voxel_2 == [2, 2, 0]) and \
              (li_voxel_none is None)


## micro environment related functions ##

class TestTimeStepMicroenv(object):
    ''' tests for pcdl.TimeStep micro environment related functions. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    def test_mcds_get_substrate_name(self, mcds=mcds):
        ls_substrate = mcds.get_substrate_list()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ls_substrate)) == "<class 'list'>") and \
              (str(type(ls_substrate[0])) == "<class 'str'>") and \
              (ls_substrate == ['oxygen','water'])

    def test_mcds_get_substrate_dict(self, mcds=mcds):
        ds_substrate = mcds.get_substrate_dict()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ds_substrate)) == "<class 'dict'>") and \
              (str(type(ds_substrate['0'])) == "<class 'str'>") and \
              (len(ds_substrate) == 2)

    def test_mcds_get_substrate_df(self, mcds=mcds):
        df_substrate = mcds.get_substrate_df()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_substrate)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_substrate.shape == (2, 2))

    def test_mcds_get_conc_df(self, mcds=mcds):
        df_conc = mcds.get_conc_df(z_slice=None, halt=False, values=1, drop=set(), keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_conc.shape == (121, 11))

    def test_mcds_get_conc_df_zslice_center(self, mcds=mcds):
        df_conc = mcds.get_conc_df(z_slice=0, halt=False, values=1, drop=set(), keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_conc.shape == (121, 11))

    def test_mcds_get_conc_df_zslice_outofcenter(self, mcds=mcds):
        df_conc = mcds.get_conc_df(z_slice=-6, halt=False, values=1, drop=set(), keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_conc.shape == (121, 11))

    def test_mcds_get_conc_df_values(self, mcds=mcds):
        df_conc = mcds.get_conc_df(z_slice=None, halt=False, values=2, drop=set(), keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_conc.shape == (121, 11))

    def test_mcds_get_conc_df_drop(self, mcds=mcds):
        df_conc = mcds.get_conc_df(z_slice=None, halt=False, values=1, drop={'oxygen'}, keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_conc.shape == (121, 10))

    def test_mcds_get_conc_df_keep(self, mcds=mcds):
        df_conc = mcds.get_conc_df(z_slice=None, halt=False, values=1, drop=set(), keep={'oxygen'})
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_conc.shape == (121, 10))

    def test_mcds_plot_contour(self, mcds=mcds):
        fig = mcds.plot_contour(
            'oxygen',
            z_slice = -3.333,  # test if
            vmin = None,  # test if
            vmax = None,  # test if
            #alpha = 1,  # matplotlib
            fill = False,  # contour case
            #cmap = 'viridis',  matplotlib
            title = 'test_mcds_plot_contour',  # test if
            #grid = False, # matplotlib
            xlim = [-31, 301],  # test if
            ylim = [-21, 201],  # test if
            xyequal = True, # test if
            ax = None,  # ok
            figsizepx = None,  # test if
            ext = None, # test fig case
            figbgcolor = None,  # not at file
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcds_plot_contourf(self, mcds=mcds):
        fig, ax = plt.subplots()
        s_pathfile = mcds.plot_contour(
            'oxygen',
            z_slice = 0,  # jum over if
            vmin = None,  # test if
            vmax = None,  # test if
            #alpha = 1,  # matplotlib
            fill = True,  # contourf case
            #cmap = 'viridis',  # matplotlib
            title = 'test_mcds_plot_contourf',  # test if
            #grid = True,  # matplotlib
            xlim = None,  # jump over if
            ylim = None,  # jump over if
            xyequal = True,  # test if
            ax = ax,  # use axis from existing matplotlib figure
            figsizepx = [641, 481],  # test non even pixel
            ext = 'tiff',  # test file case
            figbgcolor = 'yellow',  # jump over if
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('/pcdl/output_2d/conc_oxygen_z0/output00000024_oxygen.tiff')) and \
              (os.path.exists(s_pathfile)) and \
              (os.path.getsize(s_pathfile) > 2**10)
        os.remove(s_pathfile)

    def test_mcds_make_conc_vtk(self, mcds=mcds):
        s_pathfile = mcds.make_conc_vtk()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('/pcdl/output_2d/output00000024_conc.vtr')) and \
              (os.path.exists(s_pathfile)) and \
              (os.path.getsize(s_pathfile) > 2**10)
        os.remove(s_pathfile)

## cell related functions ##

class TestTimeStepCell(object):
    ''' tests for pcdl.TimeStep cell related functions. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    def test_mcds_get_cell_attribute_list(self, mcds=mcds):
        ls_cellattr = mcds.get_cell_attribute_list()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ls_cellattr)) == "<class 'list'>") and \
              (str(type(ls_cellattr[0])) == "<class 'str'>") and \
              (len(ls_cellattr) == 110)

    def test_mcds_get_celltype_list(self, mcds=mcds):
        ls_celltype = mcds.get_celltype_list()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ls_celltype)) == "<class 'list'>") and \
              (str(type(ls_celltype[0])) == "<class 'str'>") and \
              (len(ls_celltype) == 2)

    def test_mcds_get_celltype_dict(self, mcds=mcds):
        ds_celltype = mcds.get_celltype_dict()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ds_celltype)) == "<class 'dict'>") and \
              (str(type(ds_celltype['0'])) == "<class 'str'>") and \
              (len(ds_celltype) == 2)

    def test_mcds_get_cell_df(self, mcds=mcds):
        df_cell = mcds.get_cell_df(values=1, drop=set(), keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 122)

    def test_mcds_get_cell_df_values(self, mcds=mcds):
        df_cell = mcds.get_cell_df(values=2, drop=set(), keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 66)

    def test_mcds_get_cell_df_drop(self, mcds=mcds):
        df_cell = mcds.get_cell_df(values=1, drop={'oxygen'}, keep=set())
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 121)

    def test_mcds_get_cell_df_keep(self, mcds=mcds):
        df_cell = mcds.get_cell_df(values=1, drop=set(), keep={'oxygen'})
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_cell.shape[0] > 9) and \
              (df_cell.shape[1] == 13)

    # scatter categorical
    def test_mcds_plot_scatter_cat_if(self, mcds=mcds):
        fig = mcds.plot_scatter(
            focus='cell_type',  # case categorical
            z_slice = -3.333,   # test if
            z_axis = None,  # test if case categorical
            #alpha = 1,  # matplotlib
            cmap = 'viridis',  # else case es_categorical
            title = 'test_mcds_plot_scatter_cat', # matplotlib
            #grid = True,  # matplotlib
            #legend_loc = 'lower left',  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True,  # test if
            #s = None,  # matplotlib
            ax = None,  # generate matplotlib figure
            figsizepx = None,  # test if case ax none
            ext = None,  # test fig case
            figbgcolor = None,  # not a file
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcds_plot_scatter_cat_else1(self, mcds=mcds):
        s_pathfile = mcds.plot_scatter(
            focus='cell_type',  # case categorical
            z_slice = 0,  # jump over if
            z_axis = {'cancer_cell'},  # test else case categorical
            #alpha = 1,  # matplotlib
            cmap = {'cancer_cell': 'maroon'},  # test if case es_categorical
            title ='test_mcds_plot_scatter_else',  # matplotlib
            #grid = True,  # matplotlib
            #legend_loc = 'lower left',  # matplotlib
            xlim = [-31, 301],  # jump over if
            ylim = [-21, 201],  # jump over if
            xyequal = False,  # jump over if
            #s = None,  # matplotlib
            ax = None,  # use axis from existing matplotlib figure
            figsizepx = [701, 501],  # jump over if case ax none
            ext = 'tiff',  # test file case
            figbgcolor = 'cyan',  # jump over if
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('/pcdl/output_2d/cell_cell_type_z0/output00000024_cell_type.tiff')) and \
              (os.path.exists(s_pathfile)) and \
              (os.path.getsize(s_pathfile) > 2**10)
        os.remove(s_pathfile)

    def test_mcds_plot_scatter_cat_else2(self, mcds=mcds):
        fig, ax = plt.subplots()
        mcds.plot_scatter(
            focus='cell_type',  # case categorical
            z_slice = 0,  # jump over if
            z_axis = {'cancer_cell'},  # test else case categorical
            #alpha = 1,  # matplotlib
            cmap = 'viridis',  # test else case es_categorical
            title ='test_mcds_plot_scatter_else2',  # matplotlib
            #grid = True,  # matplotlib
            #legend_loc = 'lower left',  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True,  # test if
            #s = None,  # matplotlib
            ax = ax,  # use axis from existing matplotlib figure
            #figsizepx = None,  # test case ax ax
            #ext = None,  # test fig case
            #figbgcolor = None,  # not a file
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    # scatter numerical
    def test_mcds_plot_scatter_num_if(self, mcds=mcds):
        fig = mcds.plot_scatter(
            focus='oxygen',  # case numeric
            z_slice = -3.333,   # test if
            z_axis = None,  # test if numeric
            #alpha = 1,  # matplotlib
            #cmap = 'viridis',  # matplotlib
            #title = None, # matplotlib
            #grid = True,  # matplotlib
            #legend_loc = 'lower left',  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            #xyequal = True,  # test if
            #s = None,  # matplotlib
            #ax = None,  # generate matplotlib figure
            #figsizepx = None,  # test if
            #ext = None,  # test fig case
            #figbgcolor = None,  # not a file
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcds_plot_scatter_num_else(self, mcds=mcds):
        fig = mcds.plot_scatter(
            focus='oxygen',  # case numeric
            z_slice = 0,   # jump over if
            z_axis = [0, 38],  # test else numeric
            #alpha = 1,  # matplotlib
            #cmap = 'viridis',  # matplotlib
            #title = None, # matplotlib
            #grid = True,  # matplotlib
            #legend_loc = 'lower left',  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            #xyequal = True,  # test if
            #s = None,  # matplotlib
            #ax = None,  # generate matplotlib figure
            #figsizepx = None,  # test if
            #ext = None,  # test fig case
            #figbgcolor = None,  # not a file
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(fig)) == "<class 'matplotlib.figure.Figure'>")
        plt.close()

    def test_mcds_make_cell_vtk_attribute_default(self, mcds=mcds):
        s_pathfile = mcds.make_cell_vtk(
            #attribute=['cell_type'],
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('/pcdl/output_2d/output00000024_cell.vtp')) and \
              (os.path.exists(s_pathfile)) and \
              (os.path.getsize(s_pathfile) > 2**10)
        os.remove(s_pathfile)

    def test_mcds_make_cell_vtk_attribute_zero(self, mcds=mcds):
        s_pathfile = mcds.make_cell_vtk(attribute=[])
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('/pcdl/output_2d/output00000024_cell.vtp')) and \
              (os.path.exists(s_pathfile)) and \
              (os.path.getsize(s_pathfile) > 2**10)
        os.remove(s_pathfile)

    def test_mcds_make_cell_vtk_attribute_many(self, mcds=mcds):
        s_pathfile = mcds.make_cell_vtk(
            attribute=['dead', 'cell_count_voxel', 'pressure', 'cell_type'],
        )
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('/pcdl/output_2d/output00000024_cell.vtp')) and \
              (os.path.exists(s_pathfile)) and \
              (os.path.getsize(s_pathfile) > 2**10)
        os.remove(s_pathfile)


## graph related functions ##

class TestTimeStepGraph(object):
    ''' tests for pcdl.TimeStep graph related functions. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    # graph dictionatry
    def test_mcds_get_attached_graph_dict(self, mcds=mcds):
        dei_graph = mcds.data['cell']['dei_graph']['attached_cells']
        #print('graph attached:', sorted(dei_graph.items()))
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(dei_graph)) == "<class 'dict'>") and \
              (str(type(dei_graph[10])) == "<class 'set'>") and \
              (len(dei_graph[10]) == 0) and \
              (len(dei_graph) > 9)

    def test_mcds_get_neighbor_graph_dict(self, mcds=mcds):
        dei_graph = mcds.data['cell']['dei_graph']['neighbor_cells']
        #print('graph neighbor:', sorted(dei_graph.items()))
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(dei_graph)) == "<class 'dict'>") and \
              (str(type(dei_graph[10])) == "<class 'set'>") and \
              (len(dei_graph[10]) == 6) and \
              (str(type(next(iter(dei_graph)))) == "<class 'int'>") and \
              (len(dei_graph) > 9)

    # attached graph gml files
    def test_mcds_make_graph_gml_attached_defaultattr(self, mcds=mcds):
        s_pathfile = mcds.make_graph_gml(graph_type='attached', edge_attribute=True, node_attribute=[])
        f = open(s_pathfile)
        s_file = f.read()
        f.close()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('pcdl/output_2d/output00000024_attached.gml')) and \
              (os.path.exists(s_pathfile)) and \
              (s_file.find('Creator "pcdl_v') > -1) and \
              (s_file.find('graph [\n  id 1440\n  comment "time_min"\n  label "attached_graph"\n  directed 0\n') > -1) and \
              (s_file.find('node [\n    id') > -1) and \
              (s_file.find('edge [\n    source') == -1) and \
              (s_file.find('distance_microns') == -1)
        os.remove(s_pathfile)

    def test_mcds_make_graph_gml_attached_edgeattrfalse(self, mcds=mcds):
        s_pathfile = mcds.make_graph_gml(graph_type='attached', edge_attribute=False, node_attribute=[])
        f = open(s_pathfile)
        s_file = f.read()
        f.close()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('pcdl/output_2d/output00000024_attached.gml')) and \
              (os.path.exists(s_pathfile)) and \
              (s_file.find('Creator "pcdl_v') > -1) and \
              (s_file.find('graph [\n  id 1440\n  comment "time_min"\n  label "attached_graph"\n  directed 0\n') > -1) and \
              (s_file.find('node [\n    id') > -1) and \
              (s_file.find('edge [\n    source') == -1) and \
              (s_file.find('distance_microns') == -1)
        os.remove(s_pathfile)

    def test_mcds_make_graph_gml_neighbor_nodeattrtrue(self, mcds=mcds):
        s_pathfile = mcds.make_graph_gml(graph_type='neighbor', edge_attribute=True, node_attribute=['dead','cell_count_voxel','cell_density_micron3','cell_type'])  # bool,int,float,str
        f = open(s_pathfile)
        s_file = f.read()
        f.close()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('pcdl/output_2d/output00000024_neighbor.gml')) and \
              (os.path.exists(s_pathfile)) and \
              (s_file.find('Creator "pcdl_v') > -1) and \
              (s_file.find('graph [\n  id 1440\n  comment "time_min"\n  label "neighbor_graph"\n  directed 0\n') > -1) and \
              (s_file.find('node [\n    id') > -1) and \
              (s_file.find('dead') == -1) and \
              (s_file.find('cell_count_voxel') == -1) and \
              (s_file.find('cell_density_micron3') == -1) and \
              (s_file.find('cell_type') == -1) and \
              (s_file.find('edge [\n    source') > -1) and \
              (s_file.find('distance_microns')> -1)
        os.remove(s_pathfile)

    # neighbor graph gml file
    def test_mcds_make_graph_gml_neighbor_defaultattr(self, mcds=mcds):
        s_pathfile = mcds.make_graph_gml(graph_type='neighbor', edge_attribute=True, node_attribute=[])
        f = open(s_pathfile)
        s_file = f.read()
        f.close()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('pcdl/output_2d/output00000024_neighbor.gml')) and \
              (os.path.exists(s_pathfile)) and \
              (s_file.find('Creator "pcdl_v') > -1) and \
              (s_file.find('graph [\n  id 1440\n  comment "time_min"\n  label "neighbor_graph"\n  directed 0\n') > -1) and \
              (s_file.find('node [\n    id') > -1) and \
              (s_file.find('edge [\n    source') > -1) and \
              (s_file.find('distance_microns') > -1)
        os.remove(s_pathfile)

    def test_mcds_make_graph_gml_neighbor_edgeattrfalse(self, mcds=mcds):
        s_pathfile = mcds.make_graph_gml(graph_type='neighbor', edge_attribute=False, node_attribute=[])
        f = open(s_pathfile)
        s_file = f.read()
        f.close()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('pcdl/output_2d/output00000024_neighbor.gml')) and \
              (os.path.exists(s_pathfile)) and \
              (s_file.find('Creator "pcdl_v') > -1) and \
              (s_file.find('graph [\n  id 1440\n  comment "time_min"\n  label "neighbor_graph"\n  directed 0\n') > -1) and \
              (s_file.find('node [\n    id') > -1) and \
              (s_file.find('edge [\n    source') > -1) and \
              (s_file.find('distance_microns') == -1)
        os.remove(s_pathfile)

    def test_mcds_make_graph_gml_neighbor_nodeattrtrue(self, mcds=mcds):
        s_pathfile = mcds.make_graph_gml(graph_type='neighbor', edge_attribute=True, node_attribute=['dead','cell_count_voxel','cell_density_micron3','cell_type'])  # bool,int,float,str
        f = open(s_pathfile)
        s_file = f.read()
        f.close()
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('pcdl/output_2d/output00000024_neighbor.gml')) and \
              (os.path.exists(s_pathfile)) and \
              (s_file.find('Creator "pcdl_v') > -1) and \
              (s_file.find('graph [\n  id 1440\n  comment "time_min"\n  label "neighbor_graph"\n  directed 0\n') > -1) and \
              (s_file.find('node [\n    id') > -1) and \
              (s_file.find('dead') > -1) and \
              (s_file.find('cell_count_voxel') > -1) and \
              (s_file.find('cell_density_micron3') > -1) and \
              (s_file.find('cell_type') > -1) and \
              (s_file.find('edge [\n    source') > -1) and \
              (s_file.find('distance_microns') > -1)
        os.remove(s_pathfile)


## ome tiff related functions ##

class TestTimeStepOmeTiff(object):
    ''' tests for pcdl.TimeStep graph related functions. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    ## ome tiff related functions ##
    def test_mcds_make_ome_tiff_default(self, mcds=mcds):
        s_pathfile = mcds.make_ome_tiff(cell_attribute='ID', conc_cutoff={}, focus=None, file=True)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (s_pathfile.replace('\\','/').endswith('pcdl/output_2d/output00000024_oxygen_water_default_blood_cells_ID.ome.tiff')) and \
              (os.path.exists(s_pathfile)) and \
              (os.path.getsize(s_pathfile) > 2**10)
        os.remove(s_pathfile)

    def test_mcds_make_ome_tiff_bool(self, mcds=mcds):
        a_ometiff = mcds.make_ome_tiff(cell_attribute='dead', conc_cutoff={}, focus=None, file=False)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(a_ometiff)) == "<class 'numpy.ndarray'>") and \
              (a_ometiff.dtype == np.float32) and \
              (a_ometiff.shape == (4, 1, 200, 300)) and \
              (a_ometiff[2].min() == 0.0) and \
              (a_ometiff[3].min() == 0.0) and \
              (a_ometiff[0].max() >= 1.0) and \
              (a_ometiff[1].max() >= 1.0) and \
              (a_ometiff[2].max() >= 1.0) and \
              (a_ometiff[3].max() >= 1.0)

    def test_mcds_make_ome_tiff_int(self, mcds=mcds):
        a_ometiff = mcds.make_ome_tiff(cell_attribute='cell_count_voxel', conc_cutoff={}, focus=None, file=False)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(a_ometiff)) == "<class 'numpy.ndarray'>") and \
              (a_ometiff.dtype == np.float32) and \
              (a_ometiff.shape == (4, 1, 200, 300)) and \
              (a_ometiff[2].min() == 0.0) and \
              (a_ometiff[3].min() == 0.0) and \
              (a_ometiff[0].max() >= 1.0) and \
              (a_ometiff[1].max() >= 1.0) and \
              (a_ometiff[2].max() >= 1.0) and \
              (a_ometiff[3].max() >= 1.0)

    def test_mcds_make_ome_tiff_float(self, mcds=mcds):
        a_ometiff = mcds.make_ome_tiff(cell_attribute='pressure', conc_cutoff={}, focus=None, file=False)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(a_ometiff)) == "<class 'numpy.ndarray'>") and \
              (a_ometiff.dtype == np.float32) and \
              (a_ometiff.shape == (4, 1, 200, 300)) and\
              (a_ometiff[2].min() == 0.0) and \
              (a_ometiff[3].min() == 0.0) and \
              (a_ometiff[0].max() >= 1.0) and \
              (a_ometiff[1].max() >= 1.0) and \
              (a_ometiff[2].max() >= 1.0) and \
              (a_ometiff[3].max() >= 1.0)

    def test_mcds_make_ome_tiff_conccutoff(self, mcds=mcds):
        a_ometiff = mcds.make_ome_tiff(cell_attribute='ID', conc_cutoff={'oxygen': -1}, focus=None, file=False)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(a_ometiff)) == "<class 'numpy.ndarray'>") and \
              (a_ometiff.dtype == np.float32) and \
              (a_ometiff.shape == (4, 1, 200, 300)) and \
              (a_ometiff[2].min() == 0.0) and \
              (a_ometiff[3].min() == 0.0) and \
              (a_ometiff[0].max() >= 1.0) and \
              (a_ometiff[1].max() >= 1.0) and \
              (a_ometiff[2].max() >= 1.0) and \
              (a_ometiff[3].max() >= 1.0)

    def test_mcds_make_ome_tiff_focus(self, mcds=mcds):
        a_ometiff = mcds.make_ome_tiff(cell_attribute='ID', conc_cutoff={}, focus={'default'}, file=False)
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(a_ometiff)) == "<class 'numpy.ndarray'>") and \
              (a_ometiff.dtype == np.float32) and \
              (a_ometiff.shape == (1, 1, 200, 300)) and \
              (a_ometiff[0].min() == 0.0) and \
              (a_ometiff[0].max() >= 1.0)


class TestTimeStepNeuroglancer(object):
    ''' tests for loading a pcdl.TimeStep data set. '''
    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True)

    ## make_gif and magick ommand ##
    def test_mcds_render_neuroglancer_default(self, mcds=mcds):
        s_tiffpathfile = mcds.make_ome_tiff()
        o_viewer = mcds.render_neuroglancer(
            tiffpathfile = s_tiffpathfile,
            #timestep = 0,
            #intensity_cmap='gray',
        )
        assert(str(type(o_viewer)) == "<class 'neuroglancer.viewer.Viewer'>") and \
              (str(o_viewer).startswith('http://127.0.0.1:'))
        os.remove(s_tiffpathfile)

    def test_mcds_render_neuroglancer_timestep(self, mcds=mcds):
        s_tiffpathfile = mcds.make_ome_tiff()
        o_viewer = mcds.render_neuroglancer(
            tiffpathfile = s_tiffpathfile,
            timestep = -1,
            intensity_cmap='gray',
        )
        assert(str(type(o_viewer)) == "<class 'neuroglancer.viewer.Viewer'>") and \
              (str(o_viewer).startswith('http://127.0.0.1:'))
        os.remove(s_tiffpathfile)

    def test_mcds_render_neuroglancer_cmap(self, mcds=mcds):
        s_tiffpathfile = mcds.make_ome_tiff()
        o_viewer = mcds.render_neuroglancer(
            tiffpathfile = s_tiffpathfile,
            timestep = 0,
            intensity_cmap='magma',
        )
        assert(str(type(o_viewer)) == "<class 'neuroglancer.viewer.Viewer'>") and \
              (str(o_viewer).startswith('http://127.0.0.1:'))
        os.remove(s_tiffpathfile)


## anndata helper function ##
class TestTimeStepScaler(object):
    ''' test for pcdl.scaler function '''
    a_x = np.array([[ 1.,-1., 2., 0.],[ 2., 0., 0.,0.],[ 0., 1.,-1.,0.]])
    df_x = pd.DataFrame(a_x, columns=['a','b','c','d'])

    def test_scaler_none(self, df_x=df_x):
        df_scaled = pcdl.timestep.scaler(df_x=df_x, scale=None)
        assert(str(type(df_scaled)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (all(df_scaled == df_x))

    def test_scaler_minabs(self, df_x=df_x):
        df_scaled = pcdl.timestep.scaler(df_x=df_x, scale='maxabs')
        assert(str(type(df_scaled)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_scaled.values.sum().round(3) == 2.0) and \
              (df_scaled.values.min().round(3) == -1.0) and \
              (df_scaled.values.max().round(3) == 1.0)

    def test_scaler_minmax(self, df_x=df_x):
        df_scaled = pcdl.timestep.scaler(df_x=df_x, scale='minmax')
        assert(str(type(df_scaled)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_scaled.values.sum().round(3) == 4.333) and \
              (df_scaled.values.min().round(3) == 0.0) and \
              (df_scaled.values.max().round(3) == 1.0)

    def test_scaler_std(self, df_x=df_x):
        df_scaled = pcdl.timestep.scaler(df_x=df_x, scale='std')
        assert(str(type(df_scaled)) == "<class 'pandas.core.frame.DataFrame'>") and \
              (df_scaled.values.sum().round(3) == 0.0) and \
              (df_scaled.values.min().round(3) == -1.0) and \
              (df_scaled.values.max().round(3) == 1.091)


## anndata time step related functions ##
class TestTimeStepAnnData(object):
    ''' test for pcdl.TimeStep class. '''

    ## get_anndata command ##
    def test_mcds_get_anndata(self):
        mcds = pcdl.TimeStep(s_pathfile_2d, verbose=False)
        ann = mcds.get_anndata(values=1, drop=set(), keep=set(), scale='maxabs')
        assert(str(type(mcds)) == "<class 'pcdl.timestep.TimeStep'>") and \
              (str(type(ann)) == "<class 'anndata._core.anndata.AnnData'>") and \
              (ann.X.shape[0] > 9) and \
              (ann.X.shape[1] == 105) and \
              (ann.obs.shape[0] > 9) and \
              (ann.obs.shape[1] == 7) and \
              (ann.obsm['spatial'].shape[0] > 9) and \
              (ann.obsm['spatial'].shape[1] == 2) and \
              (len(ann.obsp) == 2) and \
              (ann.var.shape == (105, 0)) and \
              (len(ann.uns) == 1)

