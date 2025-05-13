#########
# title: data_timeseries.py
#
# language: python3
# date: 2023-06-11
# license: BSD-3-Clause
# authors: Patrick Wall, Randy Heiland, Paul Macklin, Elmar Bucher
#
# description:
#     code to download the output.tar.gz files
#     from the source code repository, and extract them to where
#     the pcdl library is installed, and code to remove the installed
#     output folders.
#     the extracted output_2d and output_3d folder contains
#     example PhysiCell output, necessary to run the pytest unit tests
#     and useful to run through the tutorial.
#########

# bue 20240822: in future:
# maybe physiboss output?

# library
import os
import pathlib
import pcdl
import requests
import shutil
import tarfile


# object classes
class install_data:
    """
    input:

    output:
        PhysiCell output folder (2D and 3D time series).

    description:
        function to install a 2D and 3D PhysiCell output test dataset.
    """
    def __init__(self):
        # get pcdl library installation path
        s_path = str(pathlib.Path(pcdl.__file__).parent).replace('\\','/') + '/'

        # for each timeseries
        for s_url in [
                'https://raw.githubusercontent.com/elmbeech/physicelldataloader/master/output_2d.tar.gz',
                'https://raw.githubusercontent.com/elmbeech/physicelldataloader/master/output_3d.tar.gz',
            ]:
            # get path and filename
            s_file = s_url.split('/')[-1]
            s_pathfile = s_path + s_file

            # download tar.gz file
            print(f'download: {s_url}')
            o_response = requests.get(s_url)

            print(f'extract: {s_pathfile}\n')
            # save tar.gz file
            f = open(s_pathfile, 'wb')
            f.write(o_response.content)
            f.close()
            # extract tar.gz file
            f = tarfile.open(s_pathfile, 'r')
            f.extractall(s_path)
            # bue 20240314: for the future 3.12 .. 3.14.
            # at this moment filter breaks some currently supported python versions.
            #f.extractall(s_path, filter='data' or 'fully_trusted')


class uninstall_data:
    """
    input:

    output:
        remove PhysiCell test dataset output folders.

    description:
        function to uninstall the 2D and 3D PhysiCell output test datasets,
        and all other files stored within its folders.
    """
    def __init__(self):
        # get pcdl library installation path
        s_path = str(pathlib.Path(pcdl.__file__).parent) + '/'

        # for each obsolet timeserie
        for s_file in sorted(os.listdir(s_path)):
            if s_file.startswith('output_2d') or s_file.startswith('output_3d'):

               # get path and filename
               s_pathfile = s_path + s_file

               # delete timeseries
               print(f'remove: {s_pathfile}')
               if os.path.isfile(s_pathfile):
                   os.remove(s_pathfile)
               else:
                   shutil.rmtree(s_pathfile)

