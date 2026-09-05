import os
from pcdl.timestep import TimeStep, graphfile_parser, pccmap, render_neuroglancer, scaler
from pcdl.timeseries import TimeSeries, make_gif, make_movie
from pcdl.VERSION import __version__
from pcdl.output_data import install_data, uninstall_data
import sys


###############
# LOAD"*",8,1 #
###############

def read(s_path, custom_data_type={}, load=True, microenv=True, graph=True, physiboss=True, settingxml=False, verbose=True):
    """
    input:
    output:
    description:
        load pcd physicell data
    """
    # windows to unix
    s_path = s_path.replace('\\','/')
    while (s_path.find('//') > -1):
        s_path = s_path.replace('//','/')
    # pathfile can be path to directory or file
    if (s_path.endswith('/')) and (len(s_path) > 1):
        s_path = s_path[:-1]  # handle directory
    s_pathfile = s_path

    # pcd timeseries or timestep file
    if s_pathfile.endswith('.pcd'):
        #s_path = '/'.join(s_path.split('/')[:-1])
        pcd = None

    # output timestep
    elif s_pathfile.endswith('.xml'):
        #s_path = '/'.join(s_path.split('/')[:-1])
        pcd = timestep.TimeStep(
            xmlfile = s_pathfile,
            output_path = '.',
            custom_data_type = custom_data_type,
            microenv = microenv,
            graph = graph,
            physiboss = physiboss,
            settingxml = settingxml,
            verbose = verbose,
        )

    # output timeseries
    else:
        s_pathfile = s_pathfile + '/initial.xml'
        if os.path.exists(s_pathfile):
            pcd = timeseries.TimeSeries(
                output_path = s_path,
                custom_data_type = custom_data_type,
                load = load,
                microenv = microenv,
                graph = graph,
                physiboss = physiboss,
                settingxml = settingxml,
                verbose = verbose,
            )

        # error
        else:
            sys.exit(f'Error @ load"*",8,1 : {s_pathfile} path does not look like a outputnnnnnnnn.xml file or physicell output directory ({s_path}/initial.xml is missing).')

    # output
    return pcd
