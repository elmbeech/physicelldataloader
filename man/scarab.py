####
# title: scarab.py
#
# language: python3
# date: 2024-03-07
# license: BSD-3-Clause
# author: Elmar Bucher
#
# description:
#     inspired by sphinx, scarabaeus is a super lightweight script,
#     that turns input: output: description: docstrings
#     and argparse command line help into markdown files,
#     for source code reference api documentation.
####


# library
import pcdl
import os


# function
def help_md(s_command, s_opath='man/docstring/'):
    """
    input:
        s_command: string
            command line command name.

        s_opath: string, default man/docstring/
            output path.

    output:
        opath/command.md file.

    description:
        function to generate a markdown file from the
        argparse help information.
    """
    print(f'processing: {s_command} ...')
    s_opathfile = f'{s_opath}{s_command}.md'
    f = open(s_opathfile, 'w')
    f.write('```\n')
    f.close()
    os.system(f'{s_command} -h >> {s_opathfile}')
    f = open(s_opathfile, 'a')
    f.write('```\n')
    f.close()


def docstring_md(s_function, ls_doc, s_header=None, s_opath='man/docstring/'):
    """
    input:
        s_function: string
            function name.

        ls_doc: list of string.
            module.function.__doc__.split('\n')

        s_header: string, default None
            default markdown text title is function().
            with this s_header argument you can set another title
            than the default one.

        s_opath: string, default man/docstring/
            output path.

    output:
        opath/command.md file.

    description:
        function to generate a markdown file from
        docstring information.
    """
    print(f'processing: {s_function} ...')
    os.makedirs(s_opath, exist_ok=True)
    s_opathfile = s_opath + f'{s_function}.md'
    f = open(s_opathfile, 'w')
    if (s_header is None):
        s_header = f'{s_function}()'
    f.write(f'# {s_header}\n\n')
    for s_doc in ls_doc:
        if (s_doc.find('input:') > -1):
            f.write(f'## {s_doc.strip()}\n```\n')
        elif (s_doc.find('output:') > -1):
            f.write(f'```\n\n## {s_doc.strip()}\n```\n')
        elif (s_doc.find('description:') > -1):
            f.write(f'```\n\n## {s_doc.strip()}\n```\n')
        else:
            f.write(f'{s_doc}\n')
    f.write('```')
    f.close()


# download test dataset
if not os.path.exists('pcdl/output_2d/') or not os.path.exists('pcdl/output_3d/'):
    pcdl.install_data()


# load data
mcds = pcdl.TimeStep(
    'pcdl/output_2d/output00000000.xml',
    #custom_data_type={'oncoprotein': str},
    verbose=False,
)

mcdsts = pcdl.TimeSeries(
    'pcdl/output_2d/',
    #custom_data_type={'oncoprotein': str},
    verbose=False,
)


# write data_timeseries function makdown files
docstring_md(
    s_function = 'pcdl.install_data',
    ls_doc = pcdl.install_data.__doc__.split('\n'),
)
docstring_md(
    s_function = 'pcdl.uninstall_data',
    ls_doc = pcdl.uninstall_data.__doc__.split('\n'),
)


# write TimeStep initialize function makdown files
docstring_md(
    s_function = 'mcds.__init__',
    ls_doc = pcdl.TimeStep.__init__.__doc__.split('\n'),
    s_header = "mcds = pcdl.TimeStep('path/to/outputnnnnnnnn.xml')"
)
docstring_md(
    s_function = 'mcds.set_verbose_false',
    ls_doc = pcdl.TimeStep.set_verbose_false.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.set_verbose_true',
    ls_doc = pcdl.TimeStep.set_verbose_true.__doc__.split('\n'),
)

# write TimeStep metadata function makdown files
docstring_md(
    s_function = 'mcds.get_multicellds_version',
    ls_doc = pcdl.TimeStep.get_multicellds_version.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_physicell_version',
    ls_doc = pcdl.TimeStep.get_physicell_version.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_timestamp',
    ls_doc = pcdl.TimeStep.get_timestamp.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_time',
    ls_doc = pcdl.TimeStep.get_time.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_runtime',
    ls_doc = pcdl.TimeStep.get_runtime.__doc__.split('\n'),
)

docstring_md(
    s_function = 'mcds.get_unit_dict',
    ls_doc = pcdl.TimeStep.get_unit_dict.__doc__.split('\n'),
)

# write TimeStep mesh function markdown files
# range and axis
docstring_md(
    s_function = 'mcds.get_voxel_ijk_range',
    ls_doc = pcdl.TimeStep.get_voxel_ijk_range.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_mesh_mnp_range',
    ls_doc = pcdl.TimeStep.get_mesh_mnp_range.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_xyz_range',
    ls_doc = pcdl.TimeStep.get_xyz_range.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_voxel_ijk_axis',
    ls_doc = pcdl.TimeStep.get_voxel_ijk_axis.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_mesh_mnp_axis',
    ls_doc = pcdl.TimeStep.get_mesh_mnp_axis.__doc__.split('\n'),
)
# mesh
docstring_md(
    s_function = 'mcds.get_mesh',
    ls_doc = pcdl.TimeStep.get_mesh.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_mesh_2D',
    ls_doc = pcdl.TimeStep.get_mesh_2D.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_mesh_coordinate',
    ls_doc = pcdl.TimeStep.get_mesh_coordinate.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_mesh_spacing',
    ls_doc = pcdl.TimeStep.get_mesh_spacing.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.is_in_mesh',
    ls_doc = pcdl.TimeStep.is_in_mesh.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_mesh_mnp',
    ls_doc = pcdl.TimeStep.get_mesh_mnp.__doc__.split('\n'),
)
# voxel
docstring_md(
    s_function = 'mcds.get_voxel_spacing',
    ls_doc = pcdl.TimeStep.get_voxel_spacing.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_voxel_volume',
    ls_doc = pcdl.TimeStep.get_voxel_volume.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_voxel_ijk',
    ls_doc = pcdl.TimeStep.get_voxel_ijk.__doc__.split('\n'),
)

# write TimeStep microenv function markdown files
docstring_md(
    s_function = 'mcds.get_substrate_list',
    ls_doc = pcdl.TimeStep.get_substrate_list.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_substrate_dict',
    ls_doc = pcdl.TimeStep.get_substrate_dict.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_substrate_df',
    ls_doc = pcdl.TimeStep.get_substrate_df.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_conc_df',
    ls_doc = pcdl.TimeStep.get_conc_df.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.plot_contour',
    ls_doc = pcdl.TimeStep.plot_contour.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.make_conc_vtk',
    ls_doc = pcdl.TimeStep.make_conc_vtk.__doc__.split('\n'),
)

# write TimeStep cell agent function markdown files
docstring_md(
    s_function = 'mcds.get_celltype_list',
    ls_doc = pcdl.TimeStep.get_celltype_list.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_celltype_dict',
    ls_doc = pcdl.TimeStep.get_celltype_dict.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_cell_df',
    ls_doc = pcdl.TimeStep.get_cell_df.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_cell_attribute_list',
    ls_doc = pcdl.TimeStep.get_cell_attribute_list.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.plot_scatter',
    ls_doc = pcdl.TimeStep.plot_scatter.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.make_cell_vtk',
    ls_doc = pcdl.TimeStep.make_cell_vtk.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_anndata',
    ls_doc = pcdl.TimeStep.get_anndata.__doc__.split('\n'),
)

# write TimeStep graph function markdown files
docstring_md(
    s_function = 'mcds.get_attached_graph_dict',
    ls_doc = pcdl.TimeStep.get_attached_graph_dict.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_neighbor_graph_dict',
    ls_doc = pcdl.TimeStep.get_neighbor_graph_dict.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.get_spring_graph_dict',
    ls_doc = pcdl.TimeStep.get_spring_graph_dict.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcds.make_graph_gml',
    ls_doc = pcdl.TimeStep.make_graph_gml.__doc__.split('\n'),
)

# write TimeStep microenvironment and cells function markdown files
docstring_md(
    s_function = 'mcds.make_ome_tiff',
    ls_doc = pcdl.TimeStep.make_ome_tiff.__doc__.split('\n'),
)

docstring_md(
    s_function = 'pcdl.render_neuroglancer',
    ls_doc = pcdl.render_neuroglancer.__doc__.split('\n'),
    s_header = "mcds.render_neuroglancer('path/to/ome.tiff')"
)

# write TimeStep internal function makdown files
docstring_md(
    s_function = 'pcdl.scaler',
    ls_doc = pcdl.scaler.__doc__.split('\n'),
)
docstring_md(
    s_function = 'pcdl.graphfile_parser',
    ls_doc = pcdl.graphfile_parser.__doc__.split('\n'),
)


# write TimeSeries initialize function makdown files
docstring_md(
    s_function = 'mcdsts.__init__',
    ls_doc = pcdl.TimeSeries.__init__.__doc__.split('\n'),
    s_header = "mcdsts = pcdl.TimeSeries('path/to/output')"
)
docstring_md(
    s_function = 'mcdsts.get_xmlfile_list',
    ls_doc = pcdl.TimeSeries.get_xmlfile_list.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.read_mcds',
    ls_doc = pcdl.TimeSeries.read_mcds.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.get_mcds_list',
    ls_doc = pcdl.TimeSeries.get_mcds_list.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.get_annmcds_list',
    ls_doc = pcdl.TimeSeries.get_annmcds_list.__doc__.split('\n'),
)

docstring_md(
    s_function = 'mcdsts.set_verbose_false',
    ls_doc = pcdl.TimeSeries.set_verbose_false.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.set_verbose_true',
    ls_doc = pcdl.TimeSeries.set_verbose_true.__doc__.split('\n'),
)

# write TimeSeries microenv function makdown files
docstring_md(
    s_function = 'mcdsts.get_conc_df',
    ls_doc = pcdl.TimeSeries.get_conc_df.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.get_conc_attribute',
    ls_doc = pcdl.TimeSeries.get_conc_attribute.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.plot_contour',
    ls_doc = pcdl.TimeSeries.plot_contour.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.make_conc_vtk',
    ls_doc = pcdl.TimeSeries.make_conc_vtk.__doc__.split('\n'),
)

# write TimeSeries cell agent function makdown files
docstring_md(
    s_function = 'mcdsts.get_cell_df',
    ls_doc = pcdl.TimeSeries.get_cell_df.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.get_cell_attribute',
    ls_doc = pcdl.TimeSeries.get_cell_attribute.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.plot_scatter',
    ls_doc = pcdl.TimeSeries.plot_scatter.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.make_cell_vtk',
    ls_doc = pcdl.TimeSeries.make_cell_vtk.__doc__.split('\n'),
)
docstring_md(
    s_function = 'mcdsts.get_anndata',
    ls_doc = pcdl.TimeSeries.get_anndata.__doc__.split('\n'),
)

# write TimeSeries graph function makdown files
docstring_md(
    s_function = 'mcdsts.make_graph_gml',
    ls_doc = pcdl.TimeSeries.make_graph_gml.__doc__.split('\n'),
)

# write TimeSeries microenvironment and cells function makdown files
docstring_md(
    s_function = 'mcdsts.make_ome_tiff',
    ls_doc = pcdl.TimeSeries.make_ome_tiff.__doc__.split('\n'),
)
docstring_md(
    s_function = 'pcdl.render_neuroglancer',
    ls_doc = pcdl.render_neuroglancer.__doc__.split('\n'),
    s_header = "mcdsts.render_neuroglancer('path/to/ome.tiff')"
)
docstring_md(
    s_function = 'mcdsts.plot_timeseries',
    ls_doc = pcdl.TimeSeries.plot_timeseries.__doc__.split('\n'),
)

# write TimeSeries making movies function markdown files
docstring_md(
    s_function = 'pcdl.make_gif',
    ls_doc = pcdl.make_gif.__doc__.split('\n'),
    s_header = "mcdsts.make_gif('path/to/plots')"
)
docstring_md(
    s_function = 'pcdl.make_movie',
    ls_doc = pcdl.make_movie.__doc__.split('\n'),
    s_header = "mcdsts.make_movie('path/to/plots')"
)


# wite cli function markdown files
# metadata
help_md(s_command='pcdl_get_version')
help_md(s_command='pcdl_get_unit_dict')
# substrate
help_md(s_command='pcdl_get_substrate_list')
help_md(s_command='pcdl_get_conc_attribute')
help_md(s_command='pcdl_get_conc_df')
help_md(s_command='pcdl_plot_contour')
help_md(s_command='pcdl_make_conc_vtk')
# cell agent
help_md(s_command='pcdl_get_celltype_list')
help_md(s_command='pcdl_get_cell_attribute_list')
help_md(s_command='pcdl_get_cell_attribute')
help_md(s_command='pcdl_get_cell_df')
help_md(s_command='pcdl_get_anndata')
help_md(s_command='pcdl_make_graph_gml')
help_md(s_command='pcdl_plot_scatter')
help_md(s_command='pcdl_make_cell_vtk')
# substrate and cell agent
help_md(s_command='pcdl_plot_timeseries')
help_md(s_command='pcdl_make_ome_tiff')
help_md(s_command='pcdl_render_neuroglancer')
# making movies
help_md(s_command='pcdl_make_gif')
help_md(s_command='pcdl_make_movie')

