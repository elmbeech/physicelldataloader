# libarary
import io
import json
import lzma
import numpy as np
import os
import pandas as pd
from pcdl.timestep import TimeStep, graphfile_parser, pccmap, render_neuroglancer, scaler
from pcdl.timeseries import TimeSeries, make_gif, make_movie
from pcdl.VERSION import __version__
from pcdl.output_data import install_data, uninstall_data
import sys
from zipfile import ZipFile


###############
# LOAD"*",8,1 #
###############

def read(s_path, custom_data_type={}, load=True, microenv=True, graph=True, physiboss=True, settingxml=False, verbose=True):
    """
    input:
    output:
    description:
        load pcd physicell data
        https://github.com/elmbeech/mcmx/tree/main
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
    if s_pathfile.endswith('.pcdl'):
        s_path = '/'.join(s_pathfile.split('/')[:-1])
        s_path = s_path if len(s_path) > 0 else '.'
        do_pcd = {}
        for s_file in ZipFile(s_pathfile).namelist():
            # load mcds data dictionary
            if s_file.endswith('.json') or s_file.endswith('.json.xz'):
                print(f'readring: {s_file} ...')
                # json
                with ZipFile(s_pathfile, 'r').open(s_file, 'r') as f:
                    o_pcd = json.load(f) if not s_file.endswith('.xz') else json.loads(lzma.decompress(f.read()))
                    # list to set manipulation
                    for s_graph in o_pcd['cell']['dei_graph']:
                        o_pcd['cell']['dei_graph'][s_graph] = {i_key: set(li_value) for i_key, li_value in o_pcd['cell']['dei_graph'][s_graph].items()}
                    # list to array manipulation
                    o_pcd['mesh']['ijk_axis'] = [np.array(l_value) for l_value in o_pcd['mesh']['ijk_axis']]
                    o_pcd['mesh']['mnp_axis'] = [np.array(l_value) for l_value in o_pcd['mesh']['mnp_axis']]
                    o_pcd['mesh']['mnp_coordinate'] = np.array(o_pcd['mesh']['mnp_coordinate'])
                    o_pcd['mesh']['mnp_grid'] =  np.array(o_pcd['mesh']['mnp_grid'])

                # load and plug in df_substrate
                s_csv = s_file.replace('.json','_subs.csv')
                with ZipFile(s_pathfile, 'r').open(s_csv, 'r') as f:
                    df_substrate = pd.read_csv(io.BytesIO(f.read())) if not s_file.endswith('.xz') else pd.read_csv(io.BytesIO(lzma.decompress(f.read())))
                    o_pcd['substrate']['df_substrate'] = df_substrate  # plug
                # load and plug in df_substrate
                s_csv = s_file.replace('.json','_conc.csv')
                with ZipFile(s_pathfile, 'r').open(s_csv, 'r') as f:
                    df_conc = pd.read_csv(io.BytesIO(f.read())) if not s_file.endswith('.xz') else pd.read_csv(io.BytesIO(lzma.decompress(f.read())))
                    o_pcd['substrate']['df_conc'] = df_conc  # plug
                # load and plug in df_substrate
                s_csv = s_file.replace('.json','_cell.csv')
                with ZipFile(s_pathfile, 'r').open(s_csv, 'r') as f:
                    df_cell = pd.read_csv(io.BytesIO(f.read())) if not s_file.endswith('.xz') else pd.read_csv(io.BytesIO(lzma.decompress(f.read())))
                    o_pcd['cell']['df_cell'] = df_cell  # plug
                # update output
                do_pcd.update({o_pcd['metadata']['timestep'] : o_pcd})
        # transform mcds data dictionary to TimeSteps
        l_mcds = [TimeStep(o_pcd, output_path=s_path) for _, o_pcd in sorted(do_pcd.items())]
        if (len(l_mcds) == 1):
            pcd = l_mcds[0]
        # transform list of many mcds TimeSteps to TimeSeries
        elif (len(l_mcds) > 1):
            pcd = TimeSeries(l_mcds)
        # error handling
        else:
            sys.exit(f'Error @ load"*",8,1 : {s_pathfile} path pcdl files does not contain any mcds time step.')

    # output timestep
    elif s_pathfile.endswith('.xml'):
        #s_path = '/'.join(s_path.split('/')[:-1])
        pcd = TimeStep(
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
            pcd = TimeSeries(
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
