#########
# title: pyMCDSts.py
#
# language: python3
# date: 2022-08-22
# license: BSD-3-Clause
# authors: Patrick Wall, Randy Heiland, Paul Macklin, Elmar Bucher
#
# description:
#     pyMCDSts.py defines an object class, able to load and access
#     within python a time series of mcds objects loaded from a single
#     PhysiCell model output directory. pyMCDSts.py was first forked from
#     PhysiCell-Tools python-loader, where it was implemented as
#     pyMCDS_timeseries.py, then totally rewritten and further developed.
#
#     the make_image and make_movie functions are cloned from the PhysiCell
#     Makefile. note on difference image magick convert and mogrify:
#     + https://graphicsmagick-tools.narkive.com/9Sowc4HF/gm-tools-mogrify-vs-convert
#########


# load libraries
import bioio_base
from bioio.writers import OmeTiffWriter
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from pcdl.pyMCDS import pyMCDS, es_coor_cell, es_coor_conc
import platform
import sys
import xml.etree.ElementTree as etree


############
# function #
############

## MAKING MOVIES RELATED FUNCTIONS ##
def _handle_magick():
    """
    output:
        s_magick: string
            image magick command line command call.

    description:
        internal function manipulates the command line command call,
        so that the call as well works on linux systems, which all
        too often run image magick < 7.0.
    """
    s_magick = 'magick '
    if (platform.system() in {'Linux'}) and (os.system('magick --version') != 0) and (os.system('convert --version') == 0):
        s_magick = ''
    return s_magick


def make_gif(path, interface='jpeg'):
    """
    input:
        path: string
            relative or absolute path to where the images are
            from which the gif will be generated.

        interface: string; default jpeg
            this images, from which the gif will be generated
            have to exist under the given path.
            they can be generated with the plot_scatter or plot_contour
            function.

    output:
        gif file in the path directory.
            additionally, the function will return the gif's path and filename.

    description:
        this function generates a gif image from all interface image files
        found in the path directory.
        https://en.wikipedia.org/wiki/GIF
    """
    s_magick = _handle_magick()
    # handle path and file name
    path = path.replace('\\','/')
    if path.endswith('/'): path = path[:-1]
    if not os.path.isdir(path):
        sys.exit(f'Error @ make_gif : {path} path does not exist.')
    s_file = path.split('/')[-1]
    if s_file.startswith('.'): s_file = s_file[1:]
    if (len(s_file) == 0): s_file = 'movie'
    s_file += f'_{interface}.gif'
    s_opathfile = f'{path}/{s_file}'
    s_ipathfiles = f'{path}/*.{interface}'
    # genaerate gif
    s_cmd = f'{s_magick}convert {s_ipathfiles} {s_opathfile}'
    if (os.system(s_cmd) != 0):
        sys.exit("Error @ make_gif : imagemagick could not generatet the gif.")

    # output
    return s_opathfile


def make_movie(path, interface='jpeg', framerate=12):
    """
    input:
        path: string
            relative or absolute path to where the images are
            from which the movie will be generated.

        interface: string; default jpeg
            this images, from which the mp4 movie will be generated
            have to exist under the given path.
            they can be generated with the plot_scatter or plot_contour
            function.

        framerate: integer; default 12
            specifies how many images per second will be used.
            humans are capable of processing 12 images per second and
            seeing them individually. higher rates are seen as motion.

    output:
        mp4 move file in the path directory.
`           additionally, the function will return the mp4's path and filename.

    description:
        this function generates a movie from all interface image files
        found in the path directory.
        https://en.wikipedia.org/wiki/MP4_file_format
        https://en.wikipedia.org/wiki/Making_Movies
    """
    # handle path
    s_pwd = os.getcwd()
    s_path = path.replace('\\','/')
    if s_path.endswith('/'): s_path = s_path[:-1]

    # handle output filename
    s_ofile = s_path.split('/')[-1]
    if s_ofile.startswith('.'): s_ofile = s_ofile[1:]
    if (len(s_ofile) == 0): s_ofile = 'movie'
    s_ofile += f'_{interface}{framerate}.mp4'
    s_opathfile = f'{s_path}/{s_ofile}'

    # generate input file list
    os.chdir(s_path)
    ls_ifile = sorted(glob.glob(f'*.{interface}'))
    f = open('ffmpeginput.txt', 'w')
    for s_ifile in ls_ifile:
        f.write(f"file '{s_ifile}'\n")
    f.close()

    # genearete movie
    s_cmd = f'ffmpeg -y -r {framerate} -f concat -i ffmpeginput.txt -vcodec libx264 -pix_fmt yuv420p -strict -2 -tune animation -crf 15 -acodec none {s_ofile}'  # -safe 0
    if (os.system(s_cmd) != 0):
        sys.exit("Error @ make_movie : ffmpeg could not generatet the movie.")
    os.remove('ffmpeginput.txt')

    # output
    os.chdir(s_pwd)
    return s_opathfile


###########
# classes #
###########

class pyMCDSts:
    def __init__(self, output_path='.', custom_data_type={}, load=True, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True):
        """
        input:
            output_path: string, default '.'
                relative or absolute path to the directory where
                the PhysiCell output files are stored.

            custom_data_type: dictionary; default is {}
                variable to specify custom_data variable types
                other than float (int, bool, str) like this: {var: dtype, ...}.
                downstream float and int will be handled as numeric,
                bool as Boolean, and str as categorical data.

            load: boole; default True
                should the whole time series data, all time steps, straight at
                object initialization be read and stored to mcdsts.l_mcds?

            microenv: boole; default True
                should the microenvironment data be loaded?
                setting microenv to False will use less memory and speed up
                processing, similar to the original pyMCDS_cells.py script.

            graph: boole; default True
                should the graphs be loaded?
                setting graph to False will use less memory and speed up processing.

            physiboss: boole; default True
                should physiboss state data be loaded, if found?
                setting physiboss to False will use less memory and speed up processing.

            settingxml: string; default PhysiCell_settings.xml
                the settings.xml that is loaded, from which the cell type ID
                label mapping, is extracted, if this information is not found
                in the output xml file.
                set to None or False if the xml file is missing!

            verbose: boole; default True
                setting verbose to False for less text output, while processing.

        output:
            mcdsts: pyMCDSts class instance
                this instance offers functions to process all stored time steps
                from a simulation.

        description:
            pyMCDSts.__init__ generates a class instance the instance offers
            functions to process all time steps in the output_path directory.
        """
        output_path = output_path.replace('\\','/')
        while (output_path.find('//') > -1):
            output_path = output_path.replace('//','/')
        if (output_path.endswith('/')) and (len(output_path) > 1):
            output_path = output_path[:-1]
        if not os.path.isdir(output_path):
            print(f'Error @ pyMCDSts.__init__ : this is not a path! could not load {output_path}.')
        self.path = output_path
        self.ls_xmlfile = [s_pathfile.replace('\\','/').split('/')[-1] for s_pathfile in sorted(glob.glob(self.path + f'/output*.xml'))]  # bue 2022-10-22: is output*.xml always the correct pattern?
        self.custom_data_type = custom_data_type
        self.microenv = microenv
        self.graph = graph
        self.physiboss = physiboss
        self.settingxml = settingxml
        self.verbose = verbose
        if load:
            self.read_mcds()
        else:
            self.l_mcds = None


    def set_verbose_false(self):
        """
        input:

        output:
            set verbose false.

        description:
            function to set verbosity.
        """
        self.verbose = False


    def set_verbose_true(self):
        """
        input:

        output:
            set verbose true.

        description:
            function to set verbosity.
        """
        self.verbose = True


    def make_gif(self, path, interface='jpeg'):
        """
        help(pcdl.make_gif)
        """
        s_opathfile = make_gif(path=path, interface=interface)
        return s_opathfile


    def make_movie(self, path, interface='jpeg', framerate=12):
        """
        help(pcdl.make_movie)
        """
        s_opathfile = make_movie(path=path, interface=interface, framerate=framerate)
        return s_opathfile


    ## LOAD DATA ##

    def get_xmlfile_list(self):
        """
        input:
            self: pyMCDSts class instance.

        output:
            xmlfile_list: list of strings
                alphanumerical sorted list of output*.xml strings.

        description:
            function returns an alphanumerical (and as such chronological)
            ordered list of physicell xml path and output file names. the
            list can be manipulated and used as input for the
            mcdsts.read_mcds function.
        """
        return self.ls_xmlfile.copy()


    def read_mcds(self, xmlfile_list=None):
        """
        input:
            self: pyMCDSts class instance.

            xmlfile_list: list of strings; default None
                list of physicell output*.xml strings.

        output:
            self.l_mcds: list of mcds objects

        description:
            the function returns a list of mcds objects loaded by
            pyMCDS calls.
        """
        # handle input
        if (xmlfile_list is None):
            xmlfile_list = self.get_xmlfile_list()
        ls_xmlfile = sorted([s_xmlfile.replace('\\','/').split('/')[-1]  for s_xmlfile in xmlfile_list])
        ls_xmlpathfile = [self.path + f'/{s_xmlfile}' for s_xmlfile in ls_xmlfile]

        # load mcds objects into list
        l_mcds = []
        for s_xmlpathfile in ls_xmlpathfile:
            mcds = pyMCDS(
                xmlfile = s_xmlpathfile,
                custom_data_type = self.custom_data_type,
                microenv = self.microenv,
                graph = self.graph,
                physiboss = self.physiboss,
                settingxml = self.settingxml,
                verbose = self.verbose
            )
            l_mcds.append(mcds)
            if self.verbose:
                print() # carriage return

        # output
        self.l_mcds = l_mcds
        self.ls_xmlfile = ls_xmlfile
        return l_mcds


    def get_mcds_list(self):
        """
        input:
            self: pyMCDSts class instance.

        output:
            self.l_mcds: list of chronologically ordered mcds objects.
                watch out, this is a pointer to the
                self.l_mcds list of mcds objects, not a copy of self.l_mcds!

        description:
            function returns a pointer to the self.l_mcds list of mcds objects.
        """
        return self.l_mcds


    ## MICROENVIRONMENT RELATED FUNCTIONS ##

    def get_conc_df(self, values=1, drop=set(), keep=set(), collapse=True):
        """
        input:
            self: pyMCDSts class instance.

            values: integer; default is 1
                minimal number of values a variable has to have to be outputted.
                variables that have only 1 state carry no information.
                None is a state too.

            drop: set of strings; default is an empty set
                set of column labels to be dropped for the dataframe.
                don't worry: essential columns like ID, coordinates
                and time will never be dropped.
                Attention: when the keep parameter is given, then
                the drop parameter has to be an empty set!

            keep: set of strings; default is an empty set
                set of column labels to be kept in the dataframe.
                set values=1 to be sure that all variables are kept.
                don't worry: essential columns like ID, coordinates,
                time and runtime (wall time) will always be kept.

            collapse: boole; default True
                should all mcds time steps from the time series be collapsed
                into one pandas dataframe object, or a list of dataframe objects
                for each time step?

        output:
            df_conc or ldf_conc: pandas dataframe or list of dataframe
                dataframe stores all substrate concentrations in each voxel.

        description:
            function returns for the whole time series in one or many dataframes
            with concentration values for all chemical species in all voxels.
            additionally, this dataframe lists voxel and mesh center coordinates.
        """
        # set output variables
        ldf_concts = []
        df_concts = None

        # load data
        for i, mcds in enumerate(self.get_mcds_list()):
            # pack collapsed
            if collapse:
                df_conc = mcds.get_conc_df(
                    values = 1,
                    drop = drop,
                    keep = keep,
                )
                if df_concts is None:
                    df_concts = df_conc
                else:
                    df_concts = pd.concat([df_concts, df_conc], axis=0, ignore_index=True, join='outer')
            # pack not collapsed
            else:
                df_conc = mcds.get_conc_df(
                    values = values,
                    drop = drop,
                    keep = keep,
                )
                ldf_concts.append(df_conc)

        # output
        if collapse:
            # filter
            es_attribute = set(df_concts.columns).difference(es_coor_conc)
            if (len(keep) > 0):
                es_delete = es_attribute.difference(keep)
            else:
                es_delete = es_attribute.intersection(drop)

            if (values > 1):  # by minimal number of states
                for s_column in set(df_concts.columns).difference(es_coor_conc):
                    if len(set(df_concts.loc[:,s_column])) < values:
                        es_delete.add(s_column)
            df_concts.drop(es_delete, axis=1, inplace=True)
            df_concts.index.name = 'index'
            return df_concts

        else:
            # output not collapsed
            return ldf_concts


    def get_conc_attribute(self, values=1, drop=set(), keep=set(), allvalues=False):
        """
        input:
            self: pyMCDSts class instance.

            values: integer; default is 1
                minimal number of values a variable has to have
                in any of the mcds time steps to be outputted.
                variables that have only 1 state carry no information.
                None is a state too.

            drop: set of strings; default is an empty set
                set of column labels to be dropped for the dataframe.
                don't worry: essential columns like ID, coordinates
                and time will never be dropped.
                Attention: when the keep parameter is given, then
                the drop parameter has to be an empty set!

            keep: set of strings; default is an empty set
                set of column labels to be kept in the dataframe.
                set values=1 to be sure that all variables are kept.
                don't worry: essential columns like ID, coordinates
                and time will always be kept.

            allvalues: boolean; default is False
                should only the min and max values or all values be returned?

        output:
            dl_variable: dictionary of list
                dictionary with an entry of all non-coordinate column names
                that at least in one of the time steps or in between time
                steps, reach the given minimal state count.
                key is the column name, mapped is a list of all values
                (bool, str, and, if allvalues is True, int and float)
                or a list with minimum and maximum values (int, float).

        description:
            function to detect informative substrate concentration variables
            in a time series. this function detects even variables which have
            less than the minimal state count in each time step, but
            different values from time step to time step.
        """
        # gather data
        der_variable_state = {}
        for mcds in self.get_mcds_list():
            df_conc = mcds.get_conc_df(drop=drop, keep=keep)
            for s_column in df_conc.columns:
                if not (s_column in es_coor_conc):
                    er_state = set(df_conc.loc[:,s_column])
                    try:
                        der_variable_state[s_column] = der_variable_state[s_column].union(er_state)
                    except KeyError:
                        der_variable_state.update({s_column: er_state})
        # extract
        dlr_variable_range = dict()
        for s_column, er_state in der_variable_state.items():
            if len(er_state) >= values:
                if allvalues:
                    lr_range = sorted(er_state)
                else:
                    lr_range = [min(er_state), max(er_state)]
                dlr_variable_range.update({s_column : lr_range})
        # output
        return dlr_variable_range


    def plot_contour(self, focus, z_slice=0.0, extrema=None, alpha=1, fill=True, cmap='viridis', title='', grid=True, xlim=None, ylim=None, xyequal=True, figsizepx=None, ext='jpeg', figbgcolor=None):
        """
        input:
            self: pyMCDSts class instance

            focus: string
                column name within conc dataframe, for example.

            z_slice: floating point number; default is 0.0
                z-axis position to slice a 2D xy-plain out of the
                3D substrate concentration mesh. if z_slice position
                is not an exact mesh center coordinate, then z_slice
                will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.

            extrema: tuple of two floats; default is None
                default takes min and max from data, from the whole time series.

            alpha: floating point number; default is 1
                alpha channel transparency value
                between 1 (not transparent at all) and 0 (totally transparent).

            fill: boolean; default True
                True generates a matplotlib contourf plot.
                False generates a matplotlib contour plot.

            title: string; default is ''
                title prefix.

            cmap: string; default viridis.
                matplotlib colormap.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html

            grid: boolean; default True.
                plot axis grid lines.

            xlim: tuple of two floats; default is None
                x axis min and max value.
                default takes min and max from mesh x axis range.

            ylim: tuple of two floats; default is None
                y axis min and max value.
                default takes min and max from mesh y axis range.

            xyequal: boolean; default True
                to specify equal axis spacing for x and y axis.

            figsizepx: list of two integers; default is None
                size of the figure in pixels, (x, y).
                the given x and y will be rounded to the nearest even number,
                to be able to generate movies from the images.
                None tries to take the values from the initial.svg file.
                fall back setting is [640, 480].

            ext: string; default is jpeg
                output image format. possible formats are jpeg, png, and tiff.
                None will return the matplotlib fig object.

            figbgcolor: string; default is None which is transparent (png)
                or white (jpeg, tiff).
                figure background color.

        output:
            fig: matplotlib figures, depending on ext, either as files or as
                objects. the figures contains the contour plot and color bar.

        description:
            this function generates a matplotlib contour (or contourf) plot
            time series.

            jpeg is by definition a lossy compressed image format.
            png is by definition a lossless compressed image format.
            tiff can by definition be a lossy or lossless compressed format.
            https://en.wikipedia.org/wiki/JPEG
            https://en.wikipedia.org/wiki/Portable_Network_Graphics
            https://en.wikipedia.org/wiki/TIFF
        """
        # handle z_slice
        z_slice = float(z_slice)
        _, _, ar_p_axis = self.get_mcds_list()[0].get_mesh_mnp_axis()
        if not (z_slice in ar_p_axis):
            z_slice = ar_p_axis[abs(ar_p_axis - z_slice).argmin()]
            if self.verbose:
                print(f'z_slice set to {z_slice}.')

        # handle extrema
        if extrema == None:
            extrema = [None, None]
            for mcds in self.get_mcds_list():
                df_conc = mcds.get_conc_df()
                r_min = df_conc.loc[:,focus].min()
                r_max = df_conc.loc[:,focus].max()
                if (extrema[0] is None) or (extrema[0] > r_min):
                    extrema[0] = np.floor(r_min)
                if (extrema[1] is None) or (extrema[1] < r_max):
                    extrema[1] = np.ceil(r_max)
            if self.verbose:
                print(f'min max extrema set to {extrema}.')

        # handle xlim and ylim
        if (xlim is None):
            xlim = self.get_mcds_list()[0].get_xyz_range()[0]
            if self.verbose:
                print(f'xlim set to {xlim}.')
        if (ylim is None):
            ylim = self.get_mcds_list()[0].get_xyz_range()[1]
            if self.verbose:
                print(f'ylim set to {ylim}.')

        # handle output path
        s_path = self.path + f'/conc_{focus}_z{round(z_slice,9)}/'

        # plotting
        lo_output = []
        for i, mcds in enumerate(self.get_mcds_list()):
            o_output = mcds.plot_contour(
                focus = focus,
                z_slice = z_slice,
                vmin = extrema[0],
                vmax = extrema[1],
                alpha = alpha,
                fill = fill,
                cmap = cmap,
                title = f'{title}{focus} z{round(z_slice,9)}\n{round(mcds.get_time(),9)}[min]',
                grid = grid,
                xlim = xlim,
                ylim = ylim,
                xyequal = xyequal,
                ax = None,
                figsizepx = figsizepx,
                ext = ext,
                figbgcolor = figbgcolor,
            )
            lo_output.append(o_output)

        # output
        return lo_output


    def make_conc_vtk(self, visualize=True):
        """
        input:
            visualize: boolean; default is False
                additionally, visualize cells using vtk renderer.

        output:
            ls_vtkpathfile: one vtk file per mcds time step that contains
               3D distributions of all substrates over the microenvironment
               with corresponding time stamp.

        description:
            function generates rectilinear grid vtk files, one file
            per mcds time step that contains distribution of substrates
            over microenvironment.
            you can post-process this file in other software like paraview.

            https://www.paraview.org/
        """
        # processing
        ls_vtkpathfile = []
        for mcds in self.get_mcds_list():
            s_vtkpathfile = mcds.make_conc_vtk(visualize=visualize)
            ls_vtkpathfile.append(s_vtkpathfile)

        # output
        return ls_vtkpathfile


    ## CELL RELATED FUNCTIONS ##

    def get_cell_df(self, values=1, drop=set(), keep=set(), collapse=True):
        """
        input:
            self: pyMCDSts class instance.

            values: integer; default is 1
                minimal number of values a variable has to have to be outputted.
                variables that have only 1 state carry no information.
                None is a state too.

            drop: set of strings; default is an empty set
                set of column labels to be dropped for the dataframe.
                don't worry: essential columns like ID, coordinates
                and time will never be dropped.
                Attention: when the keep parameter is given, then
                the drop parameter has to be an empty set!

            keep: set of strings; default is an empty set
                set of column labels to be kept in the dataframe.
                set values=1 to be sure that all variables are kept.
                don't worry: essential columns like ID, coordinates,
                time and runtime (wall time) will always be kept.

            collapse: boole; default True
                should all mcds time steps from the time series be collapsed
                into one pandas dataframe object, or a list of dataframe objects
                for each time step?

        output:
            df_cell or ldf_cell: pandas dataframe or list of dataframe
                dataframe stores one cell per row, all tracked variables
                values related to this cell. the variables are cell_position,
                mesh_center, and voxel coordinates, all cell_variables,
                all substrate rates and concentrations, and additional
                the surrounding cell density.

        description:
            function returns for the whole time series one or many dataframes
            with a cell centric view of the simulation.
        """
        # set output variables
        ldf_cellts = []
        df_cellts = None

        # load data
        for i, mcds in enumerate(self.get_mcds_list()):
            # pack collapsed
            if collapse:
                df_cell = mcds.get_cell_df(
                    values = 1,
                    drop = drop,
                    keep = keep,
                )
                if df_cellts is None:
                    df_cellts = df_cell
                else:
                    df_cellts = pd.concat([df_cellts, df_cell], axis=0, ignore_index=False, join='outer')
            # pack not collapsed
            else:
                df_cell = mcds.get_cell_df(
                    values = values,
                    drop = drop,
                    keep = keep,
                )
                ldf_cellts.append(df_cell)

        # output collapsed
        if collapse:
            # filter
            es_attribute = set(df_cellts.columns).difference(es_coor_cell)
            if (len(keep) > 0):
                es_delete = es_attribute.difference(keep)
            else:
                es_delete = es_attribute.intersection(drop)

            if (values > 1):  # by minimal number of states
                for s_column in set(df_cellts.columns).difference(es_coor_cell):
                    if len(set(df_cellts.loc[:,s_column])) < values:
                        es_delete.add(s_column)
            df_cellts.drop(es_delete, axis=1, inplace=True)
            df_cellts.reset_index(inplace=True)
            df_cellts.index.name = 'index'
            return df_cellts
        # output not collapsed
        else:
            return ldf_cellts


    def get_cell_attribute(self, values=1, drop=set(), keep=set(), allvalues=False):
        """
        input:
            self: pyMCDSts class instance.

            values: integer; default is 1
                minimal number of values a variable has to have
                in any of the mcds time steps to be outputted.
                variables that have only 1 state carry no information.
                None is a state too.

            drop: set of strings; default is an empty set
                set of column labels to be dropped for the dataframe.
                don't worry: essential columns like ID, coordinates
                and time will never be dropped.
                Attention: when the keep parameter is given, then
                the drop parameter has to be an empty set!

            keep: set of strings; default is an empty set
                set of column labels to be kept in the dataframe.
                set values=1 to be sure that all variables are kept.
                don't worry: essential columns like ID, coordinates
                and time will always be kept.

            allvalues: boolean; default is False
                for numeric data, should only the min and max values or
                all values be returned?

        output:
            dl_variable: dictionary of list
                dictionary with an entry of all non-coordinate column names
                that at least in one of the time steps or in between
                time steps, reach the given minimal value count.
                key is the column name, mapped is a list of all values
                (bool, str, and, if allvalues is True, int and float) or
                a list with minimum and maximum values (int, float).

        description:
            function to detect informative variables in a time series.
            this function detects even variables which have less than the
            minimal state count in each time step, but different values
            from time step to time step.
        """
        # gather data
        de_variable_state = {}
        for mcds in self.get_mcds_list():
            df_cell = mcds.get_cell_df(drop=drop, keep=keep)
            for s_column in df_cell.columns:
                if not (s_column in es_coor_cell):
                    e_state = set(df_cell.loc[:,s_column])
                    try:
                        de_variable_state[s_column] = de_variable_state[s_column].union(e_state)
                    except KeyError:
                        de_variable_state.update({s_column: e_state})
        # extract
        dl_variable_range = dict()
        for s_column, e_state in de_variable_state.items():
            if len(e_state) >= values:
                o_state = list(e_state)[0]
                if (type(o_state) in {float, int}) and not(allvalues):  # min max values (numeric)
                    l_range = [min(e_state), max(e_state)]
                else:  # bool, str, and all values (numeric)
                    l_range = sorted(e_state)
                dl_variable_range.update({s_column : l_range})
        # output
        return dl_variable_range


    def plot_scatter(self, focus='cell_type', z_slice=0.0, z_axis=None, alpha=1, cmap='viridis', title='', grid=True, legend_loc='lower left', xlim=None, ylim=None, xyequal=True, s=None, figsizepx=None, ext='jpeg', figbgcolor=None):
        """
        input:
            self: pyMCDSts class instance

            focus: string; default is 'cell_type'
                column name within cell dataframe.

            z_slice: floating point number; default is 0.0
                z-axis position to slice a 2D xy-plain out of the 3D mesh.
                if z_slice position is not an exact mesh center coordinate,
                then z_slice will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.

            z_axis: for a categorical focus: set of labels;
               for a numeric focus: tuple of two floats; default is None
               depending on the focus column variable dtype, default extracts
               labels or min and max values from data.

            alpha: floating point number; default is 1
                alpha channel transparency value
                between 1 (not transparent at all) and 0 (totally transparent).

            cmap: dictionary of strings or string; default viridis.
                dictionary that maps labels to colors strings.
                matplotlib colormap string.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html

            title: string; default is ''
                title prefix.

            grid: boolean; default is True.
                plot axis grid lines.

            legend_loc: string; default is 'lower left'.
                the location of the categorical legend, if applicable.
                possible strings are: best,
                upper right, upper center, upper left, center left,
                lower left, lower center, lower right, center right,
                center.

            xlim: tuple of two floats; default is None
                x axis min and max value.
                default takes min and max from mesh x axis range.

            ylim: tuple of two floats; default is None
                y axis min and max value.
                default takes min and max from mesh y axis range.

            xyequal: boolean; default True
                to specify equal axis spacing for x and y axis.

            s: integer; default is None
                scatter plot dot size in pixel.
                typographic points are 1/72 inch.
                the marker size s is specified in points**2.
                plt.rcParams['lines.markersize']**2 is in my case 36.
                None tries to take the value from the initial.svg file.
                fall back setting is 36.

            figsizepx: list of two integers; default is None
                size of the figure in pixels, (x, y).
                the given x and y will be rounded to the nearest even number,
                to be able to generate movies from the images.
                None tries to take the values from the initial.svg file.
                fall back setting is [640, 480].

            ext: string; default is jpeg
                output image format. possible formats are jpeg, png, and tiff.
                None will return the matplotlib fig object.

            figbgcolor: string; default is None which is transparent (png)
                or white (jpeg, tiff).
                figure background color.

        output:
            fig: matplotlib figures, depending on ext, either as files or
                as objects. the figures contains the scatter plot and
                color bar (numerical data) or color legend (categorical data).

        description:
            function returns a (pandas) matplotlib scatter plotts,
            inclusive color bar or color legend, for the whole time series,
            for the focus specified, either as matplotlib fig object
            or as jpeg, png, or tiff file.

            jpeg is by definition a lossy compressed image format.
            png is by definition a lossless compressed image format.
            tiff can by definition be a lossy or lossless compressed format.
            https://en.wikipedia.org/wiki/JPEG
            https://en.wikipedia.org/wiki/Portable_Network_Graphics
            https://en.wikipedia.org/wiki/TIFF
        """
        # plotting
        lo_output = []
        for i, mcds in enumerate(self.get_mcds_list()):
            df_cell = mcds.get_cell_df()
            o_output = mcds.plot_scatter(
                focus = focus,
                z_slice = z_slice,
                z_axis = z_axis,
                alpha = alpha,
                cmap = cmap,
                title = f'{title}{focus} z{round(z_slice,9)}\n{df_cell.shape[0]}[agent] {round(mcds.get_time(),9)}[min]',
                grid = grid,
                legend_loc = legend_loc,
                xlim = xlim,
                ylim = ylim,
                xyequal = xyequal,
                s = s,
                ax = None,
                figsizepx = figsizepx,
                ext = ext,
                figbgcolor = figbgcolor,
            )
            lo_output.append(o_output)

        # output
        return lo_output


    def make_cell_vtk(self, attribute=['cell_type'], visualize=False):
        """
        input:
            attribute: list of strings; default is ['cell_type']
                column name within cell dataframe.

            visualize: boolean; default is False
                additionally, visualize cells using vtk renderer.

        output:
            ls_vtkpathfile: one 3D glyph vtk file per mcds time step
                that contains cells.

        description:
            function that generates 3D glyph vtk files for cells.
            one file per mcds time step. cells can have specified attributes
            like cell_type, pressure, dead, etc.
            you can post-process this file in other software like paraview.

            https://www.paraview.org/
        """
        # processing
        ls_vtkpathfile = []
        for mcds in self.get_mcds_list():
            s_vtkpathfile = mcds.make_cell_vtk(
                attribute = attribute,
                visualize = visualize,
            )
            ls_vtkpathfile.append(s_vtkpathfile)

        # output
        return ls_vtkpathfile


    ## OME TIFF RELATED FUNCTIONS ##

    def make_ome_tiff(self, cell_attribute='ID', conc_cutoff={}, focus=None, file=True, collapse=True):
        """
        input:
            cell_attribute: strings; default is 'ID', which will result in a
                cell segmentation mask.
                column name within the cell dataframe.
                the column data type has to be numeric (bool, int, float)
                and cannot be string.
                the result will be stored as 32 bit float.

            conc_cutoff: dictionary string to real; default is an empty dictionary.
                if a contour from a substrate not should be cut by greater
                than zero (shifted to integer 1), another cutoff value can be specified here.

            focus: set of strings; default is a None
                set of substrate and cell_type names to specify what will be
                translated into ome tiff format.
                if None, all substrates and cell types will be processed.

            file: boolean; default True
                if True, an ome tiff file is the output.
                if False, a numpy array with shape tczyx is the output.

            collapse: boole; default True
                should all mcds time steps from the time series be collapsed
                into one ome tiff file (numpy array),
                or an ome tiff file (numpy array) for each time step?

        output:
            a_tczyx_img: numpy array or ome tiff file.


        description:
            function to transform chosen mcdsts output into an 1[um] spaced
            tczyx (time, channel, z-axis, y-axis, x-axis) ome tiff file or numpy array,
            one substrate or cell_type per channel.
            a ome tiff file is more or less:
            a numpy array, containing the image information
            and a xml, containing the microscopy metadata information,
            like the channel labels.
            the ome tiff file format can for example be read by the napari
            or fiji (imagej) software.

            https://napari.org/stable/
            https://fiji.sc/
        """
        # for each T time step
        l_tczyx_img = []
        for i, mcds in enumerate(self.get_mcds_list()):
            # processing
            b_file = True # 10
            if (not file and not collapse) or (not file and collapse) or (file and collapse):  # 00, 01, 11
                b_file = False
            o_tczyx_img = mcds.make_ome_tiff(
                cell_attribute = cell_attribute,
                conc_cutoff = conc_cutoff,
                focus = focus,
                file = b_file
            )
            l_tczyx_img.append(o_tczyx_img)

        # handle channels
        ls_substrate = mcds.get_substrate_list()
        ls_celltype = mcds.get_celltype_list()

        if not (focus is None):
            ls_substrate = [s_substrate for s_substrate in ls_substrate if s_substrate in set(focus)]
            ls_celltype = [s_celltype for s_celltype in ls_celltype if s_celltype in set(focus)]
            if (set(focus) != set(ls_substrate).union(set(ls_celltype))):
                sys.exit(f'Error : {focus} not found in {ls_substrate} {ls_celltype}')

        # output 00 list of numpy arrays
        if (not file and not collapse):  # 00
            if self.verbose:
                print(f'la_tczyx_img shape: {len(l_tczyx_img)} * {l_tczyx_img[0].shape}')
            return l_tczyx_img

        # output 01 numpy array
        elif (not file and collapse):  # 01
            # numpy array
            a_tczyx_img = np.array(l_tczyx_img)
            if self.verbose:
                print('a_tczyx_img shape:', a_tczyx_img.shape)
            return a_tczyx_img

        # output 10 list of pathfile strings
        elif (file and not collapse):  # 10
            return l_tczyx_img

        # output 11 ometiff file
        elif (file and collapse):  # 11
            a_tczyx_img = np.array(l_tczyx_img)
            if self.verbose:
                print('a_tczyx_img shape:', a_tczyx_img.shape)

            # generate filename
            s_channel = ''
            for s_substrate in ls_substrate:
                try:
                    r_value = conc_cutoff[s_substrate]
                    s_channel += f'_{s_substrate}{r_value}'
                except KeyError:
                    s_channel += f'_{s_substrate}'
            for s_celltype in ls_celltype:
                s_channel += f'_{s_celltype}'
            if len(ls_celltype) > 0:
                s_channel += f'_{cell_attribute}'
            s_tifffile = f'timeseries{s_channel}.ome.tiff'
            if (len(s_tifffile) > 255):
                print(f"Warning: filename {len(s_tifffile)} > 255 character.")
                s_tifffile = 'timeseries_channels.ome.tiff'
                print(f"file name adjusted to {s_tifffile}.")
            s_tiffpathfile = self.path + '/' + s_tifffile

            # save to file
            OmeTiffWriter.save(
                a_tczyx_img,
                s_tiffpathfile,
                dim_order = 'TCZYX',
                #ome_xml=x_img,
                channel_names = ls_substrate + ls_celltype,
                image_names = [f'timeseries_{cell_attribute}'],
                physical_pixel_sizes = bioio_base.types.PhysicalPixelSizes(mcds.get_voxel_spacing()[2], 1.0, 1.0),  # z,y,x [um]
                #channel_colors=,
                #fs_kwargs={},
            )
            return s_tiffpathfile

        # error case
        else:
            sys.exit(f'Error @ make_ome_tiff : {file} {collapse} strange file collapse combination.')


    ## TIME SERIES RELATED FUNCTIONS ##

    def plot_timeseries(self, focus_cat=None, focus_num=None, aggregate_num=np.nanmean, frame='cell', z_slice=None, logy=False, ylim=None, secondary_y=None, subplots=False, sharex=False, sharey=False, linestyle='-', linewidth=None, cmap=None, color=None, grid=True, legend=True, yunit=None, title=None, ax=None, figsizepx=[640, 480], ext=None, figbgcolor=None):
        """
        input:
            self: pyMCDSts class instance

            focus_cat: string; default is None
                categorical or boolean data column within dataframe specified under frame.
                default is None, which is total, which is all agents or voxels, no categories.

            focus_num: string; default is None
                numerical data column within dataframe specified under frame.
                default is None, which is count, agent or voxel count.

            aggregate_num: function; default np.nanmean
                aggregation function for focus_num data.

            frame: string; default is cell_df
                to specifies the data dataframe.
                cell: dataframe will be retrieved through the mcds.get_cell_df function.
                conc: dataframe will be retrieved through the mcds.get_conc_df function.

            z_slice: floating point number; default is None
                z-axis position to slice a 2D xy-plain out of the 3D mesh.
                if z_slice position numeric but not an exact mesh center coordinate,
                then z_slice will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.
                if set to None, the whole domain is taken.

            logy: bool; default False
                if True, then y axis is natural log scaled.

            ylim: tuple of two floats; default is None
                y axis min and max value.
                default is None, which automatically detects min and max value.

            secondary_y: bool or list of strings; default False
                whether to plot on the secondary y-axis.
                if a list, which columns to plot on the secondary y-axis.

            subplots: bool or sequence of iterable, default False
                whether to group columns into subplots.
                a sequence of iterable of column labels
                will create a subplot for each group of columns.

            sharex: bool, default False
                in case subplots is True, share x-axis by
                setting some x-axis labels to invisible.

            sharey: bool, default False
                in case subplots is True, share y-axis range and possibly
                setting some y-axis labels to invisible.

            linestyle: string or list of strings, default '-'
                matplotlib line style {'-', '--', '-.', ':', ''},
                over all or per column.

            linewidth: float or list of float, default None
                line width in points.

            cmap: string; default None
                matplotlib colormap string.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html
                achtung: if cmap is given, color will be disregarded.

            color: string or list of string or dictionary; default None
                color string referred to by name, RGB or RGBA code.
                achtung: if cmap is given, color will be disregarded.

            grid: boolean; default True
                plot axis grid lines.

            legend: bool or 'reverse'; default True
                if True or reverse, place legend on axis subplots.

            yunit: string; default None
                string to specify y-axis unit.
                None will not print a unit on the y-axis.

            title: string or list; default None
                title to use for the plot or subplots.
                None will print no title.

            ax: matplotlib axis object; default setting is None
                the ax object, which will be used as a canvas for plotting.
                None will generate a figure and ax object from scratch.

            figsizepx: list of two integers, default is [640, 480]
                size of the figure in pixels, (x, y).
                the given x and y will be rounded to the nearest even number,
                to be able to generate movies from the images.

            ext: string; default is None
                output image format. possible formats are None, jpeg, png, and tiff.
                if None then the matplotlib figure is returned by the function
                and not written to file.

            figbgcolor: string; default is None which is transparent (png)
                or white (jpeg, tiff).
                figure background color.
                only relevant if ext not is None.

        output:
            if ext is None: a fig matplotlib figure, containing the ax axis object, is returned.
            else: an image file is generated under the returned path.

        description:
            this function to generate a timeseries plot and either returns a
            matplotlib figure or an image file (jpeg, png, tiff).

            jpeg is by definition a lossy compressed image format.
            png is by definition a lossless compressed image format.
            tiff can by definition be a lossy or lossless compressed format.
            https://en.wikipedia.org/wiki/JPEG
            https://en.wikipedia.org/wiki/Portable_Network_Graphics
            https://en.wikipedia.org/wiki/TIFF
        """
        # handle focus
        if focus_cat is None:
            focus_cat  = 'total'
        if focus_num is None:
            focus_num = 'count'
            aggregate_num = len

        # handle z_slice
        if not (z_slice is None):
            _, _, ar_p_axis = self.get_mcds_list()[0].get_mesh_mnp_axis()
            if not (z_slice in ar_p_axis):
                z_slice = ar_p_axis[abs(ar_p_axis - z_slice).argmin()]
                if self.verbose:
                    print(f'z_slice set to {z_slice}.')

        # generate series dataframe
        df_series = None
        for mcds in self.get_mcds_list():
            # fetch cell timestep dataframe
            if frame in {'cell', 'df_cell', 'cell_df', 'get_cell_df'}:
                mcds.set_verbose_false()
                if (focus_cat == 'total') and (focus_num == 'count'):
                    df_frame = mcds.get_cell_df(values=1, keep={'time'})
                    df_frame['total'] = 'total'
                    df_frame['count'] = 1
                elif (focus_cat == 'total'):
                    df_frame = mcds.get_cell_df(values=1, keep={focus_num})
                    df_frame['total'] = 'total'
                elif (focus_num == 'count'):
                    df_frame = mcds.get_cell_df(values=1, keep={focus_cat})
                    df_frame['count'] = 1
                else:
                    df_frame = mcds.get_cell_df(values=1, keep={focus_cat,focus_num})
                mcds.set_verbose_true()
            # fetch conc timestep dataframe
            elif frame in {'conc', 'df_conc', 'conc_df', 'get_conc_df'}:
                mcds.set_verbose_false()
                if (focus_cat == 'total') and (focus_num == 'count'):
                    df_frame = mcds.get_conc_df(values=1, keep={'time'})
                    df_frame['total'] = 'total'
                    df_frame['count'] = 1
                elif (focus_cat == 'total'):
                    df_frame = mcds.get_conc_df(values=1, keep={focus_num})
                    df_frame['total'] = 'total'
                elif (focus_num == 'count'):
                    df_frame = mcds.get_conc_df(values=1, keep={focus_cat})
                    df_frame['count'] = 1
                else:
                    df_frame = mcds.get_conc_df(values=1, keep={focus_cat,focus_num})
                mcds.set_verbose_true()
            # error
            else:
                sys.exit(f"Error @ pyMCDSts.plot_timeseries : unknown frame {frame}. known are cell_df and conc_df.")
            # handle z_slize
            if not (z_slice is None):
                df_frame = df_frame.loc[(df_frame.mesh_center_p == z_slice),:]
            # calculate focus_num aggregate per focus_cat
            r_time = mcds.get_time()
            df_frame = df_frame.loc[:,[focus_cat, focus_num]]
            o_aggregate = df_frame.groupby(focus_cat).apply(aggregate_num, include_groups=False)
            if (type(o_aggregate) is pd.Series):
                o_aggregate.name = r_time
                df_aggregate = o_aggregate.to_frame()
            elif (type(o_aggregate) is pd.DataFrame):
                df_aggregate = o_aggregate.loc[:,[focus_num]]
                df_aggregate.columns = [r_time]
            else:
                sys.exit(f'Error @ pyMCDSts.plot_timeseries : {aggregate_num} calculation returns unexpected variable type {type(o_aggregate)}.\nthe expected type is a pandas Series or DataFrame.')
            # store result
            if (df_series is None):
                df_series = df_aggregate
            else:
                df_series = pd.merge(
                    df_series,
                    df_aggregate,
                    left_index=True,
                    right_index=True,
                    how='outer'
                )
        # transpose dataframe
        df_series = df_series.T

        # handle ylabel
        if (focus_num == 'count') and (yunit is None):
            ylabel = focus_num
        elif (focus_num == 'count'):
            ylabel = f'focus_num [{yunit}]'
        elif (yunit is None):
            ylabel = f"{aggregate_num.__name__.replace('np.nan','')} {focus_num}"
        else:
            ylabel = f"{aggregate_num.__name__.replace('np.nan','')} {focus_num} [{yunit}]"

        # generate series line plot
        if (ax is None):
            # handle figure size
            figsizepx[0] = figsizepx[0] - (figsizepx[0] % 2)  # enforce even pixel number
            figsizepx[1] = figsizepx[1] - (figsizepx[1] % 2)
            r_px = 1 / plt.rcParams['figure.dpi']  # translate px to inch
            figsize = [None, None]
            figsize[0] = figsizepx[0] * r_px
            figsize[1] = figsizepx[1] * r_px
            if self.verbose:
                print(f'inch figure size set to {figsize}.')
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = plt.gcf()
        if not (cmap is None):
            # if cmap
            df_series.plot(
                kind = 'line',
                logy = logy,
                ylim = ylim,
                secondary_y = secondary_y,
                subplots = subplots,
                sharex = sharex,
                sharey = sharey,
                linestyle = linestyle,
                linewidth = linewidth,
                cmap = cmap,
                grid = grid,
                legend = legend,
                ylabel = ylabel,
                xlabel = f"time [{mcds.get_unit_dict()['time']}]",
                title = title,
                ax = ax
            )
        else:
            # if color
            df_series.plot(
                kind = 'line',
                logy = logy,
                ylim = ylim,
                secondary_y = secondary_y,
                subplots = subplots,
                sharex = sharex,
                sharey = sharey,
                linestyle = linestyle,
                linewidth = linewidth,
                color = color,
                grid = grid,
                legend = legend,
                ylabel = ylabel,
                xlabel = f"time [{mcds.get_unit_dict()['time']}]",
                title = title,
                ax = ax
            )

        # output
        if (ext is None):
            return fig
        else:
            if (focus_num == 'count'):
                s_pathfile = self.path + f'/timeseries_{frame}_{focus_cat}_{focus_num}.{ext}'
            else:
                s_pathfile = self.path + f"/timeseries_{frame}_{focus_cat}_{focus_num}_{aggregate_num.__name__.replace('np.nan','')}.{ext}"
            if figbgcolor is None:
                figbgcolor = 'auto'
            plt.tight_layout()
            fig.savefig(s_pathfile, facecolor=figbgcolor)
            plt.close(fig)
            return s_pathfile


    ## GRAPH RELATED FUNCTIONS ##

    def make_graph_gml(self, graph_type, edge_attribute=True, node_attribute=[]):
        """
        input:
            self: pyMCDS class instance.

            graph_type: string
                to specify which physicell output data should be processed.
                attached, touch: processes mcds.get_attached_graph_dict dictionary.
                neighbor: processes mcds.get_neighbor_graph_dict dictionary.
                spring: processes mcds.get_spring_graph_dict dictionary.

            edge_attribute: boolean; default True
                specifies if the spatial Euclidean distance is used for
                edge attribute, to generate a weighted graph.

            node_attribute: list of strings; default is empty list
                list of mcds.get_cell_df dataframe columns, used for
                node attributes.

        output:
            gml file for each time step.
                path and filenames are printed to the standard output.

        description:
            function to generate graph files in the gml graph modelling language
            standard format.

            gml was the outcome of an initiative that started at
            the international symposium on graph drawing 1995 in Passau
            and ended at Graph Drawing 1996 in Berkeley. the networkx python
            and igraph C and python libraries for graph analysis are
            gml compatible and can as such read and write this file format.

            https://en.wikipedia.org/wiki/Graph_Modelling_Language
            https://github.com/elmbeech/physicelldataloader/blob/master/man/publication/himsolt1996gml_a_portable_graph_file_format.pdf
            https://networkx.org/
            https://igraph.org/
        """
        # processing
        ls_pathfile = []
        for mcds in self.get_mcds_list():
            s_pathfile = mcds.make_graph_gml(
                graph_type = graph_type,
                edge_attribute = edge_attribute,
                node_attribute = node_attribute,
            )
            ls_pathfile.append(s_pathfile)

        # outout
        return ls_pathfile
