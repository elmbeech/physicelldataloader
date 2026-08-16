#####
# title: test_optional_dependencies.py
#
# language: python3
# author: Elmar Bucher
# date: 2026-08-14
# license: BSD 3-Clause
#
# description:
#   pytest unit test library that checks that pcdl installs and runs light
#   weight (default install: matplotlib, numpy, pandas, scipy only), and
#   that functions requiring an optional, heavyweight dependency (anndata,
#   bioio, bioio-ome-tiff, geopandas, neuroglancer, requests, scikit-image,
#   shapely, spatialdata, vtk) raise an actionable error message, pointing
#   to `pip install pcdl[full]`, or to install the missing library manually,
#   in case that dependency is not installed.
#   + https://docs.pytest.org/
#####


# load library
import os
import pathlib
import pytest
import subprocess
import sys
import pcdl
from pcdl._optional import optional_import


# const
s_path_2d = str(pathlib.Path(pcdl.__file__).parent.resolve()/'output_2d')
s_file_2d = 'output00000024.xml'


## download test dataset ##
if not os.path.exists(s_path_2d):
    pcdl.install_data()


## the module names optional_import has to reach for, per heavyweight,
## specialized pcdl function.
ls_optional_module = [
    'anndata',
    'bioio',
    'bioio.writers',
    'bioio_base',
    'geopandas',
    'neuroglancer',
    'neuroglancer.cli',
    'requests',
    'skimage.exposure',
    'skimage.util',
    'shapely',
    'spatialdata',
    'vtk',
]

## pre-warm the import cache for all optional dependencies (if installed),
## so that the missing-dependency tests below, which poison one module at
## a time via sys.modules, only ever fail on the single library they
## specifically poison, not on some sibling library that library depends
## on internally (e.g. spatialdata depends on shapely and geopandas).
for s_module in ls_optional_module:
    try:
        optional_import(s_module)
    except ModuleNotFoundError:
        pass


########################################
# pcdl._optional.optional_import tests #
########################################

class TestOptionalImport(object):
    ''' tests for the pcdl._optional.optional_import lazy import helper. '''

    def test_optional_import_module_present(self):
        o_module = optional_import('os')
        assert o_module is os

    def test_optional_import_attr_present(self):
        f_join = optional_import('os.path', s_attr='join')
        assert f_join is os.path.join

    def test_optional_import_module_missing(self):
        with pytest.raises(ModuleNotFoundError) as o_error:
            optional_import('pcdl_not_a_real_dependency_xyz')
        s_message = str(o_error.value)
        assert 'pcdl_not_a_real_dependency_xyz' in s_message
        assert 'pip install pcdl[full]' in s_message
        assert 'pip install pcdl_not_a_real_dependency_xyz' in s_message

    def test_optional_import_module_missing_custom_pip_name(self):
        with pytest.raises(ModuleNotFoundError) as o_error:
            optional_import('skimage_not_a_real_dependency', s_pip='scikit-image')
        s_message = str(o_error.value)
        assert 'scikit-image' in s_message
        assert 'pip install scikit-image' in s_message

    def test_optional_import_module_missing_caller_named(self):
        with pytest.raises(ModuleNotFoundError) as o_error:
            optional_import('pcdl_not_a_real_dependency_xyz', s_caller='TimeStep.get_anndata')
        assert 'TimeStep.get_anndata' in str(o_error.value)


###############################################
# light weight import and core function tests #
###############################################

class TestLightWeightImport(object):
    '''
    tests, run in a subprocess with a clean sys.modules, that pcdl can be
    imported, and that basic, core data loading functions work, even if
    none of the optional, heavyweight libraries are installed.
    '''

    def test_pcdl_import_and_core_functions_without_optional_libraries(self):
        s_script = f"""
import sys
for s_module in {ls_optional_module!r}:
    sys.modules[s_module] = None
import pcdl
mcds = pcdl.TimeStep(
    xmlfile={s_file_2d!r},
    output_path={s_path_2d!r},
    verbose=False,
)
df_cell = mcds.get_cell_df()
df_conc = mcds.get_conc_df()
assert df_cell.shape[0] > 0
assert df_conc.shape[0] > 0
ax = mcds.plot_scatter()
ax = mcds.plot_contour('oxygen')
print('LIGHT_IMPORT_OK')
"""
        o_result = subprocess.run([sys.executable, '-c', s_script], capture_output=True, text=True)
        assert 'LIGHT_IMPORT_OK' in o_result.stdout, o_result.stderr


#######################################################
# optional dependency function error message tests #
#######################################################

class TestOptionalDependencyErrors(object):
    ''' tests that heavyweight-dependency functions fail informatively if the dependency is missing. '''

    mcds = pcdl.TimeStep(xmlfile=s_file_2d, output_path=s_path_2d, verbose=False)

    def test_make_conc_vtk_missing_vtk(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'vtk', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.make_conc_vtk()
        s_message = str(o_error.value)
        assert 'vtk' in s_message
        assert 'pcdl[full]' in s_message

    def test_make_cell_vtk_missing_vtk(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'vtk', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.make_cell_vtk()
        assert 'vtk' in str(o_error.value)

    def test_get_anndata_missing_anndata(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'anndata', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.get_anndata()
        s_message = str(o_error.value)
        assert 'anndata' in s_message
        assert 'pcdl[full]' in s_message

    def test_get_spatialdata_missing_anndata(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'anndata', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.get_spatialdata(images=set(), points={'cell'}, shapes=set())
        assert 'anndata' in str(o_error.value)

    def test_get_spatialdata_missing_spatialdata(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'spatialdata', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.get_spatialdata(images=set(), points={'cell'}, shapes=set())
        assert 'spatialdata' in str(o_error.value)

    def test_get_spatialdata_missing_shapely(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'shapely', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.get_spatialdata(images=set(), points=set(), shapes={'cell'})
        assert 'shapely' in str(o_error.value)

    def test_get_spatialdata_missing_geopandas(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'geopandas', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.get_spatialdata(images=set(), points=set(), shapes={'cell'})
        assert 'geopandas' in str(o_error.value)

    def test_get_spatialdata_does_not_need_bioio(self, monkeypatch, mcds=mcds):
        # get_spatialdata renders its own images (file=False), so it must
        # not require the bioio ome tiff writer stack.
        monkeypatch.setitem(sys.modules, 'bioio', None)
        monkeypatch.setitem(sys.modules, 'bioio.writers', None)
        monkeypatch.setitem(sys.modules, 'bioio_base', None)
        sdata = mcds.get_spatialdata(images={'subs'}, points={'subs'}, shapes={'cell'})
        assert str(type(sdata)).startswith("<class 'spatialdata")

    def test_make_ome_tiff_file_missing_bioio(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'bioio.writers', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            mcds.make_ome_tiff(file=True)
        s_message = str(o_error.value)
        assert 'bioio' in s_message
        assert 'pcdl[full]' in s_message

    def test_make_ome_tiff_array_does_not_need_bioio(self, monkeypatch, mcds=mcds):
        monkeypatch.setitem(sys.modules, 'bioio', None)
        monkeypatch.setitem(sys.modules, 'bioio.writers', None)
        monkeypatch.setitem(sys.modules, 'bioio_base', None)
        a_img = mcds.make_ome_tiff(file=False)
        assert a_img.shape[0] > 0

    def test_render_neuroglancer_missing_neuroglancer(self, monkeypatch, mcds=mcds):
        monkeypatch.delitem(sys.modules, 'pcdl.neuromancer', raising=False)
        monkeypatch.setitem(sys.modules, 'neuroglancer', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            pcdl.render_neuroglancer('not_a_real_file.ome.tiff')
        s_message = str(o_error.value)
        assert 'neuroglancer' in s_message
        assert 'pcdl[full]' in s_message

    def test_render_neuroglancer_missing_bioio(self, monkeypatch, mcds=mcds):
        monkeypatch.delitem(sys.modules, 'pcdl.neuromancer', raising=False)
        monkeypatch.setitem(sys.modules, 'bioio', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            pcdl.render_neuroglancer('not_a_real_file.ome.tiff')
        assert 'bioio' in str(o_error.value)

    def test_install_data_missing_requests(self, monkeypatch):
        monkeypatch.setitem(sys.modules, 'requests', None)
        with pytest.raises(ModuleNotFoundError) as o_error:
            pcdl.install_data()
        s_message = str(o_error.value)
        assert 'requests' in s_message
        assert 'pcdl[full]' in s_message
