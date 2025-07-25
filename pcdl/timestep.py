#########
# title: timestep.py
#
# language: python3
# date: 2022-08-22
# license: BSD-3-Clause
# authors: Patrick Wall, Randy Heiland, Furkan Kurtoglu, Paul Macklin, Elmar Bucher
#
# description:
#     timestep.py definds an object class, able to load and access
#     within python a single time step from the PhysiCell model output folder.
#     timestep.py was forked from the original PhysiCell-Tools python-loader
#     implementation and further developed.
#########


# load library
import anndata as ad
import bioio_base
from bioio.writers import OmeTiffWriter
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
import neuroglancer
import numpy as np
import os
import pandas as pd
from pcdl import imagine
from pcdl import pdplt
from pcdl import neuromancer
from scipy import io
from scipy import sparse
import sys
import vtk
import warnings
import xml.etree.ElementTree as etree
from pcdl.VERSION import __version__


# const physicell codec
# implemation based on PhysiCell/core/PhysiCell_constants.h. (PhysiCell < 1.14)
# implemented based on PhysiCell/core/PhysiCell_constants.cpp (PhysiCell >= 1.14)
ds_cycle_model = {
    '0' : 'advanced_Ki67_cycle_model',
    '1' : 'basic_Ki67_cycle_model',
    '2' : 'flow_cytometry_cycle_model',
    '3' : 'live_apoptotic_cycle_model',
    '4' : 'total_cells_cycle_model',
    '5' : 'live_cells_cycle_model',
    '6' : 'flow_cytometry_separated_cycle_model',
    '7' : 'cycling_quiescent_model',
}
ds_death_model = {
    '100' : 'apoptosis_death_model',
    '101' : 'necrosis_death_model',
    '102' : 'autophagy_death_model',
    '9999' : 'custom_cycle_model',
}

ds_cycle_phase = {
    '0' : 'Ki67_positive_premitotic',
    '1' : 'Ki67_positive_postmitotic',
    '2' : 'Ki67_positive',
    '3' : 'Ki67_negative',
    '4' : 'G0G1_phase',
    '5' : 'G0_phase',
    '6' : 'G1_phase',
    '7' : 'G1a_phase',
    '8' : 'G1b_phase',
    '9' : 'G1c_phase',
    '10' : 'S_phase',
    '11' : 'G2M_phase',
    '12' : 'G2_phase',
    '13' : 'M_phase',
    '14' : 'live',
    '15' : 'G1pm_phase',
    '16' : 'G1ps_phase',
    '17' : 'cycling',
    '18' : 'quiescent',
    '9999' : 'custom_phase',
}
ds_death_phase = {
    '100' : 'apoptotic',
    '101' : 'necrotic_swelling',
    '102' : 'necrotic_lysed',
    '103' : 'necrotic',
    '104' : 'debris',
}

# const physicell variable names
es_var_subs = {  # variable size=1 (check for the s at the end of the label)
    # cycle NOP
    # death NOP
    # volumme NOP
    # mechanicis NOP
    # motility
    'chemotactic_sensitivities',
    # secretion
    'secretion_rates',
    'uptake_rates',
    'saturation_densities',
    'net_export_rates',
    'internalized_total_substrates',
    'fraction_released_at_death',
    'fraction_transferred_when_ingested',
    # interactions NOP
    # intracellular NOP
    # custom data NOP
}
es_var_cell = {  # variable size=1 (check for the s at the end of the label)
    # cycle NOP
    # death NOP
    # volumme NOP
    # mechanics
    'cell_adhesion_affinities',
    # motility NOP
    # secretion NOP
    # interactions
    'live_phagocytosis_rates',
    'attack_rates',
    'immunogenicities',
    'fusion_rates',
    'transformation_rates',
    # intracellular NOP
    # custom data NOP
}
es_var_death = {  # variable size=2 (2 clolumns)
    'death_rates',
}
es_var_spatial = {  # variable size=3 (3 columns)
    'migration_bias_direction',  # MCDS version == 1.0
    'motility_bias_direction',  # MCDS version == 0.5
    'motility_vector',
    'orientation',
    'position',
    'velocity',
}

# const physicell variable types (non-float)
# bue 20240805: var sample is just a placeholder; data type stays float.
do_var_type = {
    # integer
    'ID': int, # bue 20240805: this index is special!
    'cell_count_voxel': int,  # bue 20240805: pcdl generated column.
    'number_of_nuclei': int,
    'maximum_number_of_attachments': int,
    # boolean
    'contact_with_basement_membrane': bool,
    'dead': bool,
    'is_motile': bool,
    # categorical
    'cell_type': str,  # id mapping cell_type
    'chemotaxis_index': str,  # id mapping substarte
    'cycle_model': str,  # codec mapping
    'current_phase': str,  # codec mapping
    'current_death_model': str,  # codec mapping
}

# const coordinate variable names
es_coor_conc = {
    'ID',
    'voxel_i','voxel_j','voxel_k',
    'mesh_center_m','mesh_center_n','mesh_center_p',
    'time', 'runtime',
    'xmlfile',
}
es_coor_cell = {
    'ID',
    'voxel_i', 'voxel_j', 'voxel_k',
    'mesh_center_m', 'mesh_center_n', 'mesh_center_p',
    'position_x', 'position_y', 'position_z',
    'time', 'runtime',
    'xmlfile',
}


# functions
def render_neuroglancer(tiffpathfile, timestep=0, intensity_cmap='gray'):
    """
    input:
        tiffpathfile: string.
            path to ome tiff file.

        timestep: integer, default is 0.
            variable to specify the specific time step to render.
            useful for time series ome.tiff files.
            the default is compatible with single time step ome.tiff files.

        intensity_cmap: string; default is 'gray'.
            matlab color map label, used to display expression intensity values.
            if None, no intensity layers will be generated.
            + https://matplotlib.org/stable/users/explain/colors/colormaps.html

    output:
        viewer: local url where the loaded, neuroglancer rendered ome tiff file
            can be viewed.

    description:
        function to load a time step from an ome tiff files, generated
        with make_ome_tiff, into neuroglancer.
    """
    # start neuroglancer
    viewer = neuroglancer.Viewer()
    with viewer.txn() as state:
        # render ometiff into neuroglancer
        neuromancer.ometiff2neuro(
            o_state = state,
            s_pathfile_tiff = tiffpathfile,
            i_timestep = timestep,
            s_intensity_cmap = intensity_cmap,
        )

    # print neuroglancer viewer url
    return viewer


def graphfile_parser(s_pathfile):
    """
    input:
        s_pathfile: string
            path to and file name from graph.txt file.

    output:
        dei_graph: dictionary of sets of integers.
            object maps each cell ID to connected cell IDs.

    description:
        code parses PhysiCell's own graphs format and
        returns the content in a dictionary object.
    """
    # processing
    dei_graph = {}
    f = open(s_pathfile)
    for i, s_line in enumerate(f):
        #print('processing line:', s_line.strip())
        s_key, s_value = s_line.strip().split(':')
        ei_value = set()
        if len(s_value.strip()) :
            ei_value = set([int(s_id) for s_id in s_value.split(',')])
        dei_graph.update({int(s_key): ei_value})
    f.close()

    # output
    return dei_graph


def scaler(df_x, scale='maxabs'):
    """
    input:
        df_x: pandas dataframe
              one attribute per column, one sample per row.

        scale: string; default 'maxabs'
            None: no scaling. set scale to None if you would like to have
                raw data or scale, transform, and normalize the data later.

            maxabs: maximum absolute value distance scaler will linearly map
                all values into a [-1, 1] interval. if the original data
                has no negative values, the result will be the same as with
                the minmax scaler (except with attributes with only one value).
                if the attribute has only zeros, the value will be set to 0.

            minmax: minimum maximum distance scaler will map all values
                linearly into a [0, 1] interval.
                if the attribute has only one value, the value will be set to 0.

            std: standard deviation scaler will result in sigmas.
                each attribute will be mean centered around 0.
                ddof delta degree of freedom is set to 1 because it is assumed
                that the values are samples out of the population
                and not the entire population. it is incomprehensible to me
                that the equivalent sklearn method has ddof set to 0.
                if the attribute has only one value, the value will be set to 0.

    output:
        df_x: pandas dataframe
            scaled df_x dataframe.

    description:
        inspired by scikit-learn's preprocessing scaling method, this function
        offers a re-implementation of the linear re-scaling methods maxabs,
        minmax, and scale.

        the robust scaler methods (quantile based) found in scikit-learn are
        missing. since we deal with simulated data, we don't expect heavy
        outliers, and if they exist, then they are of interest.
        the power and quantile based transformation methods and unit circle
        based normalizer methods found there are missing too.
        if you need to apply any such methods, you can do so to an anndata object
        like this:

        from sklearn import preprocessing
        adata.obsm["X_scaled"] = preprocessing.scale(adata.X)

    + https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html
    + https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing
    + https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.maxabs_scale.html
    + https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.minmax_scale.html
    + https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.scale.html
    """
    if scale is None:
        pass
    # -1,1
    elif scale == 'maxabs':
        a_x = df_x.values
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        a_maxabs = a_x / abs(a_x).max(axis=0)
        warnings.simplefilter('default')
        a_maxabs[np.isnan(a_maxabs)] = 0  # fix if entier column is 0
        df_x = pd.DataFrame(a_maxabs, columns=df_x.columns, index=df_x.index)
    # 0,1
    elif scale == 'minmax':
        a_x = df_x.values
        warnings.simplefilter("ignore")
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        a_minmax = (a_x - a_x.min(axis=0)) / (a_x.max(axis=0) - a_x.min(axis=0))
        warnings.simplefilter('default')
        a_minmax[np.isnan(a_minmax)] = 0  # fix if entier column has same value
        df_x = pd.DataFrame(a_minmax, columns=df_x.columns, index=df_x.index)
    # sigma
    elif scale == 'std':
        a_x = df_x.values
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        a_std = (a_x - a_x.mean(axis=0)) / a_x.std(axis=0, ddof=1)
        warnings.simplefilter('default')
        a_std[np.isnan(a_std)] = 0  # fix if entier column has same value
        df_x = pd.DataFrame(a_std, columns=df_x.columns, index=df_x.index)
    else:
        raise ValueError(f"Error @ scaler : unknown scale algorithm {scale} detected. known are [None, 'maxabs', 'minmax', 'std'].")

    return df_x


def _anndextract(df_cell, scale='maxabs', graph_attached={}, graph_neighbor={}, graph_spring={}, graph_method='PhysiCell'):
    """
    input:
        df_cell:  pandas dataframe
            data frame retrieved with the mcds.get_cell_df function.

        scale: string; default maxabs
            specify how the data should be scaled.
            possible values are None, maxabs, minmax, std.
            for more input, check out: help(pcdl.scaler).

        graph_attached: dict; default {}
            attached graph dictionary, retrieved with
            with the mcds.get_attched_graph() function.

        graph_neighbor: dict; default {}
            neighbor graph dictionary, retrieved
            with the mcds.get_neighbor_graph() function.

        graph_spring: dict; default {}
            spring_attached graph dictionary, retrieved
            with the mcds.get_spring_graph_dict() function.

        graph_method: string; default PhysiCell
            method how the graphs were generated.

    output:
        df_count, df_obs, d_obsm, d_obsp, d_uns dataframes and dictionaries,
            ready to be backed into an anndata object.

    description:
        this function takes a pcdl df_cell pandas dataframe and re-formats
        it into a set of two dataframes (df_count, df_obs),
        two dictionary of numpy array (d_obsm, d_obsp),
        and one dictionary of string (d_uns),
        which downstream might be transformed into an anndata object.
    """
    # transform index to string
    df_coor = df_cell.loc[:,['position_x','position_y','position_z']].copy()
    df_cell.index = df_cell.index.astype(str)

    # build obs anndata object (annotation of observations)
    df_obs = df_cell.loc[:,['mesh_center_p','time']].copy()
    df_obs.columns = ['z_layer', 'time']

    # buil obsm anndata object spatial (multi-dimensional annotation of observations)
    if (len(set(df_cell.position_z)) == 1):
        df_obsm = df_cell.loc[:,['position_x','position_y']].copy()
    else:
        df_obsm = df_cell.loc[:,['position_x','position_y','position_z']].copy()
    d_obsm = {"spatial": df_obsm.values}

    # build obsp and uns anndata object graph (pairwise annotation of obeservation) and (unstructured data)
    ####
    # acknowledgement:
    #   this code is inspired from the tysserand add_to_AnnData impelmentation
    #   from Alexis Coullomb form the Pancaldi Lab.
    #   https://github.com/VeraPancaldiLab/tysserand/blob/main/tysserand/tysserand.py#L1546
    ####
    # extract cell_id to index mapping (i always loved perl)
    di_ididx = df_cell.reset_index().loc[:,'ID'].reset_index().astype(int).set_index('ID').squeeze().to_dict()
    # transform cell id graph dict to index matrix and pack for anndata
    d_obsp = {}  # pairwise annotation of obeservation
    d_uns = {}  # unstructured data
    for s_graph, dei_graph in [('neighbor', graph_neighbor), ('attached', graph_attached), ('spring', graph_spring)]:
        lli_edge = []
        lr_distance = []
        for i_src, ei_dst in dei_graph.items():
            for i_dst in ei_dst:
                # extract edge
                lli_edge.append([di_ididx[i_src], di_ididx[i_dst]])
                r_distance = ((df_coor.loc[i_src,:].values -  df_coor.loc[i_dst,:].values)**2).sum()**(1/2)
                lr_distance.append(r_distance)
        # if there is a graph
        if (len(lli_edge) > 0):
            # handle edge data
            ai_edge = np.array(lli_edge, dtype=np.uint)
            # handle connection data
            ai_conectivity = np.ones(ai_edge.shape[0], dtype=np.uint16)
            ai_conectivity_sparse = sparse.csr_matrix(
                (ai_conectivity, (ai_edge[:,0], ai_edge[:,1])),
                shape = (df_cell.shape[0], df_cell.shape[0]),
                dtype = np.uint
            )
            # handle distance data
            ar_distance  = np.array(lr_distance, dtype=np.float64)
            ar_distance_sparse = sparse.csr_matrix(
                (ar_distance, (ai_edge[:,0], ai_edge[:,1])),
                shape = (df_cell.shape[0], df_cell.shape[0]),
                dtype = np.float64
            )
            # pack obsp
            d_obsp.update({
                f'physicell_{s_graph}_conectivities': ai_conectivity_sparse,
                f'physicell_{s_graph}_distances': ar_distance_sparse,
            })
            # pack uns
            d_uns.update({
                s_graph : {
                    'connectivities_key': f'physicell_{s_graph}_conectivities',
                    'distances_key': f'physicell_{s_graph}_distances',
                    'params': {
                        'metric': 'euclidean',
                        'method': graph_method,
                    }
                }
            })

    # extract discrete cell data
    es_drop = set(df_cell.columns).intersection({
        'voxel_i', 'voxel_j', 'voxel_k',
        'mesh_center_m', 'mesh_center_n', 'mesh_center_p',
        'position_x', 'position_y','position_z',
        'time', 'runtime', 'xmlfile',
    })
    df_cell.drop(es_drop, axis=1, inplace=True)  # maybe obs?

    # dectect variable types
    des_type = {'float': set(), 'int': set(), 'bool': set(), 'str': set()}
    for _, se_cell in df_cell.items():
        if str(se_cell.dtype).startswith('float'):
            des_type['float'].add(se_cell.name)
        elif str(se_cell.dtype).startswith('int'):
            des_type['int'].add(se_cell.name)
        elif str(se_cell.dtype).startswith('bool'):
            des_type['bool'].add(se_cell.name)
        elif str(se_cell.dtype).startswith('object'):
            des_type['str'].add(se_cell.name)
        else:
            print(f'Error @ TimeSeries.get_anndata : column {se_cell.name} detected with unknown dtype {str(se_cell.dtype)}.')

    # build on obs and X anndata object
    df_cat = df_cell.loc[:,sorted(des_type['str'])].copy()
    df_obs = pd.merge(df_obs, df_cat, left_index=True, right_index=True)
    es_num = des_type['float'].union(des_type['int'].union(des_type['bool']))
    df_count = df_cell.loc[:,sorted(es_num)].copy()
    for s_col in des_type['bool']:
        df_count[s_col] = df_count[s_col].astype(int)
    df_count = scaler(df_count, scale=scale)

    # return
    return(df_count, df_obs, d_obsm, d_obsp, d_uns)


# object classes
class TimeStep:
    def __init__(self, xmlfile, output_path='.', custom_data_type={}, microenv=True, graph=True, physiboss=True, settingxml='PhysiCell_settings.xml', verbose=True):
        """
        input:
            xmlfile: string
                name of the xml file with or without path.
                in the with path case, output_path has to be set to the default!

            output_path: string; default '.'
                relative or absolute path to the directory where
                the PhysiCell output files are stored.

            custom_dtype: dictionary; default is {}
                variable to specify custom_data variable types other than
                floats (namely: int, bool, str) like this: {var: dtype, ...}.
                downstream float and int will be handled as numeric,
                bool as Boolean, and str as categorical data.

            microenv: boole; default True
                should the microenvironment data be loaded?
                setting microenv to False will use less memory and speed up processing.

            graph: boole; default True
                should the graphs, like cell_neighbor_graph.txt, be loaded?
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
            mcds: TimeStep class instance
                all fetched content is stored at mcds.data.

        description:
            TimeStep.__init__ will generate a class instance with a
            dictionary of dictionaries data structure that contains all
            output from a single PhysiCell model time step. furthermore,
            this class, and as such it's instances, offers functions
            to access the stored data.
            the code assumes that all related output files are stored in
            the same directory. data is loaded by reading the xml file
            for a particular time step and the therein referenced files.
        """
        self.path = None
        self.xmlfile = None
        self.custom_data_type = custom_data_type
        self.microenv = microenv
        self.graph = graph
        self.physiboss = physiboss
        if type(settingxml) is str:
            settingxml = settingxml.replace('\\','/').split('/')[-1]
        self.settingxml = settingxml
        self.verbose = verbose
        self.data = self._read_xml(xmlfile, output_path)


    def set_verbose_false(self):
        """
        input:

        output:
            set verbose false.

        description:
            function to set verbosity.
        """
        self.verbose = False
        #print(f'pcdl: set mcds.verbose = False.')


    def set_verbose_true(self):
        """
        input:

        output:
            set verbose true.

        description:
            function to set verbosity.
        """
        self.verbose = True
        #print(f'pcdl: set mcds.verbose = True.')


    ## METADATA RELATED FUNCTIONS ##

    def get_multicellds_version(self):
        """
        input:

        output:
            s_version : sting
                MultiCellDS xml version which stored the data.

        description:
            function returns as a string the MultiCellDS xml version
            that was used to store this data.
        """
        return self.data['metadata']['multicellds_version']


    def get_physicell_version(self):
        """
        input:

        output:
            s_version : sting
                PhysiCell version which generated the data.

        description:
            function returns as a string the PhysiCell version
            that was used to generate this data.
        """
        return self.data['metadata']['physicell_version']


    def get_timestamp(self):
        """
        input:

        output:
            s_timestap : sting
                timestamp from when this data was generated.

        description:
            function returns as a string the timestamp from when
            this data was generated.
        """
        return self.data['metadata']['created']


    def get_time(self):
        """
        input:

        output:
            r_time : floating point number
                simulation time in [min].

        description:
            function returns as a real number
            the simulation time in minutes.
        """
        return self.data['metadata']['current_time']


    def get_runtime(self):
        """
        input:

        output:
            r_time : floating point number
                wall time in [sec].

        description:
            function returns as a real number, the wall time in seconds
            the simulation took to run up to this time step.
        """
        return self.data['metadata']['current_runtime']


    ## MODEL PARAMETER SETTING RELATED FUNCTIONS ##

    def get_unit_dict(self):
        """
        input:

        output:
            ds_unit: dictionary
                dictionary, which tracks units from cell and microenvironment
                variables.

        description:
            function returns a dictionary that stores all tracked variables
            and their units.
        """
        return self.data['metadata']['ds_unit'].copy()


    ## MESH RELATED FUNCTIONS  ##

    def get_voxel_ijk_range(self):
        """
        input:

        output:
            lti_i : list of tuple of 2 integer numbers
                i-axis, j-aixs, and k-axis voxel range.

        description:
            function returns in a list of tuples the lowest and highest
            i-axis, j-axis, and k-axis voxel value.
        """
        return self.data['mesh']['ijk_range'].copy()


    def get_mesh_mnp_range(self):
        """
        input:

        output:
            ltr_mnp : list of tuple of 2 floating point numbers
                m-axis, n-axis, and p-axis  mesh center range.

        description:
            function returns in a list of tuples the lowest and highest
            m-axis, n-axis, and p-axis mesh center value.
        """
        return self.data['mesh']['mnp_range'].copy()


    def get_xyz_range(self):
        """
        input:

        output:
            ltr_xyz : list of tuple of 2 floating point numbers
                x-axis, y-axis, and z-axis position range.

        description:
            function returns in a list of tuples the lowest and highest
            x-axis, y-axis, and z-axis position value.
        """
        return self.data['mesh']['xyz_range'].copy()


    def get_voxel_ijk_axis(self):
        """
        input:

        output:
            lai_ijk : list of 3 numpy arrays of integer numbers
                i-axis, j-axis, and k-axis voxel coordinates axis.

        description:
            function returns a list of voxel coordinate vectors,
            one for the i-axis, j-axis, and k-axis.
        """
        return self.data['mesh']['ijk_axis'].copy()


    def get_mesh_mnp_axis(self):
        """
        input:

        output:
            lar_mnp : list of 3 numpy arrays of floating point numbers
                m-axis, n-axis, and p-axis mesh center axis coordinates.

        description:
            function returns a list of mesh center vectors,
            one for the m-axis, n-axis, and p-axis.
        """
        return self.data['mesh']['mnp_axis'].copy()


    def get_mesh(self, flat=False):
        """
        input:
            flat : bool; default False
                if flat is True, only the m-axis mesh center
                and n-axis mesh center meshgrids will be returned.
                else the m, n, and p mesh center meshgrids will be returned.

        output:
            aar_meshgrid : 4-way (3D) or 3-way (2D) numpy arrays tensor of floating point numbers
                meshgrid shaped object, with the mesh center
                coordinate values from the m, n, p-axis or m, n-axis.

        description:
            function returns a numpy array of meshgrids each of which stores
            the mesh center coordinate values from one particular axis.
            the function can either return meshgrids for the full
            m, n, p 3D cube, or only the 2D planes along the p-axis.
        """
        if flat:
            ar_m = self.data['mesh']['mnp_grid'][0][:, :, 0]
            ar_n = self.data['mesh']['mnp_grid'][1][:, :, 0]
            return np.array([ar_m, ar_n]).copy()

        else:
            return self.data['mesh']['mnp_grid'].copy()


    def get_mesh_2D(self):
        """
        input:

        output:
            aar_meshgrid : 3-way numpy arrays tensor of floating point numbers
                meshgrid shaped objects, with the mesh center
                coordinate values from the m and n-axis.

        description:
            function is identical to the self.get_mesh(self, flat=True)
            function call.
        """
        return self.get_mesh(flat=True)


    def get_mesh_coordinate(self):
        """
        input:

        output:
            aar_meshaxis : numpy array of 3 one dimensional numpy floating point number arrays
                n, m, and p-axis mesh center coordinate vectors.

        description:
            function returns three vectors with mesh center coordinate values,
            one for each axis.
        """
        return self.data['mesh']['mnp_coordinate'].copy()


    def get_mesh_spacing(self):
        """
        input:

        output:
            lr_mnp_spacing: list of 3 floating point numbers
                mesh spacing in m, n, and p direction.

        description:
            function returns the distance in between mesh centers,
            in the spacial unit defined in the PhysiCell_settings.xml file.
        """
        return self.data['mesh']['mnp_spacing'].copy()


    def is_in_mesh(self, x, y, z, halt=False):
        """
        input:
            x: floating point number
                position x-coordinate.

            y: floating point number
                position y-coordinate.

            z: floating point number
                position z-coordinate.

            halt: boolean; default is False
                should program execution break or just spit out a warning,
                if position is not in mesh?

        output:
            b_isinmesh: boolean
                declares if the given coordinate is inside the mesh.

        description:
            function evaluates if the given position coordinate
            is inside the boundaries. if the coordinate is outside the
            mesh, a warning will be printed. if additionally
            halt is set to True, program execution will halt.
        """
        b_isinmesh = True

        # check against boundary box
        tr_x, tr_y, tr_z = self.get_xyz_range()

        if (x < tr_x[0]) or (x > tr_x[1]):
            if self.verbose:
                print(f'Warning @ TimeStep.is_in_mesh : x = {x} out of bounds: x-range is {tr_x}.')
            b_isinmesh = False
        elif (y < tr_y[0]) or (y > tr_y[1]):
            if self.verbose:
                print(f'Warning @ TimeStep.is_in_mesh : y = {y} out of bounds: y-range is {tr_y}.')
            b_isinmesh = False
        elif (z < tr_z[0]) or (z > tr_z[1]):
            if self.verbose:
                print(f'Warning @ TimeStep.is_in_mesh : z = {z} out of bounds: z-range is {tr_z}.')
            b_isinmesh = False

        # output
        if halt and not b_isinmesh:
            sys.exit('Processing stopped!')
        return b_isinmesh


    def get_mesh_mnp(self, x, y, z, is_in_mesh=True):
        """
        input:
            x: floating point number
                position x-coordinate.

            y: floating point number
                position y-coordinate.

            z: floating point number
                position z-coordinate.

            is_in_mesh: boolean; default is True
                should function check, if the given coordinate is in the mesh,
                and only calculate ijk values if is so?

        output:
            lr_mnp : list of 3 floats
                m, n, p indices for the mesh center,
                for the mesh cell containing the x, y, z position.

        description:
            function returns the meshgrid indices m, n, p
            for the given position x, y, z.
        """
        lr_mnp = None
        b_calc = True

        if is_in_mesh:
            b_calc = self.is_in_mesh(x=x, y=y, z=z, halt=False)

        if b_calc:
            ar_m_axis, ar_n_axis, ar_p_axis = self.get_mesh_mnp_axis()
            r_m = ar_m_axis[abs(ar_m_axis - x).argmin()]
            r_n = ar_n_axis[abs(ar_n_axis - y).argmin()]
            r_p = ar_p_axis[abs(ar_p_axis - z).argmin()]
            lr_mnp = [r_m, r_n, r_p]

        return lr_mnp


    def get_voxel_spacing(self):
        """
        input:

        output:
            lr_ijk_spacing: list of 3 floating point numbers
                voxel spacing in i, j, and k directions.

        description:
            function returns the voxel width, height, depth measurement,
            in the spacial unit defined in the PhysiCell_settings.xml file.
        """
        return self.data['mesh']['mnp_spacing'].copy()


    def get_voxel_volume(self):
        """
        input:

        output:
            r_volume: floating point number
                voxel volume value related to the spacial unit
                defined in the PhysiCell_settings.xml file.

        description:
            function returns the volume value for a single voxel, related
            to the spacial unit defined in the PhysiCell_settings.xml file.
        """
        return self.data['mesh']['volume']


    def get_voxel_ijk(self, x, y, z, is_in_mesh=True):
        """
        input:
            x: floating point number
                position x-coordinate.

            y: floating point number
                position y-coordinate.

            z: floating point number
                position z-coordinate.

            is_in_mesh: boolean; default is True
                should function check, if the given coordinate is in the mesh,
                and only calculate ijk values if is so?

        output:
            li_ijk : list of 3 integers
                i, j, k indices for the voxel
                containing the x, y, z position.

        description:
            function returns the meshgrid indices i, j, k
            for the given position x, y, z.
        """
        li_ijk = None
        b_calc = True

        if is_in_mesh:
            b_calc = self.is_in_mesh(x=x, y=y, z=z, halt=False)

        if b_calc:
            tr_m, tr_n, tr_p = self.get_mesh_mnp_range()
            dm, dn, dp = self.get_voxel_spacing()

            i = int(np.round((x - tr_m[0]) / dm))
            j = int(np.round((y - tr_n[0]) / dn))
            k = int(np.round((z - tr_p[0]) / dp))

            li_ijk = [i, j, k]

        return li_ijk


    ## MICROENVIRONMENT RELATED FUNCTIONS ##

    def get_substrate_list(self):
        """
        input:

        output:
            ls_substrate: list of stings
                by ID ordered list of all tracked substrates.

        description:
            function returns all chemical species names, modeled
            in the microenvironment, ordered by chemical species ID.
        """
        return self.data['substrate']['ls_substarte'].copy()


    def get_substrate_dict(self):
        """
        input:

        output:
            ds_substrate: dictionary of stings
                dictionary that maps substrate IDs to labels.

        description:
            function returns a dictionary that maps ID and name from all
            microenvironment_setup variables,
            specified in the PhysiCell_settings.xml file.
        """
        return self.data['substrate']['ds_substrate'].copy()


    def get_substrate_df(self):
        """
        input:

        output:
            df_substrae: pandas dataframe
                one substrate per row and decay_rate and difusion_coefficient
                factors as columns.

        description:
            function returns a dataframe with each substrate's
            decay_rate and difusion_coefficient.
        """
        return self.data['substrate']['df_substarte'].copy()


    def get_conc_df(self, z_slice=None, halt=False, values=1, drop=set(), keep=set()):
        """
        input:
            z_slice: floating point number; default is None
                z-axis position to slice a 2D xy-plain out of the
                3D substrate concentration mesh. if None the
                whole 3D mesh will be returned.

            halt: boolean; default is False
                should program execution break or just spit out a warning,
                if z_slice position is not an exact mesh center coordinate?
                if False, z_slice will be adjusted to the nearest
                mesh center value, the smaller one, if the coordinate
                lies on a saddle point.

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
                don't worry: essential columns like ID, coordinates
                and time will always be kept.

        output:
            df_conc : pandas dataframe
                dataframe stores all substrate concentrations in each voxel.

        description:
            function returns a dataframe with concentration values
            for all chemical species in all voxels. additionally, this
            dataframe lists voxel and mesh center coordinates.
        """
        # check keep and drop
        if (len(keep) > 0) and (len(drop) > 0):
            sys.exit(f"Error @ TimeStep.get_conc_df : when keep is given {keep}, then drop has to be an empty set {drop}!")

        # check if z_slice is a mesh center or None
        if not (z_slice is None):
            _, _, ar_p_axis = self.get_mesh_mnp_axis()
            if not (z_slice in ar_p_axis):
                if self.verbose:
                    print(f'Warning @ TimeStep.get_conc_df : specified z_slice {z_slice} is not an element of the z-axis mesh centers set {ar_p_axis}.')
                if halt:
                    sys.exit('Processing stopped!')
                else:
                    z_slice = ar_p_axis[abs(ar_p_axis - z_slice).argmin()]
                    print(f'z_slice set to {z_slice}.')

        # fetch dataframe
        df_conc = self.data['substrate']['df_conc'].copy()

        # filter z_slice
        if not (z_slice is None):
           df_conc = df_conc.loc[df_conc.mesh_center_p == z_slice, :]

        # filter
        es_attribute = set(df_conc.columns).difference(es_coor_conc)
        if (len(keep) > 0):
            es_delete = es_attribute.difference(keep)
        else:
            es_delete = es_attribute.intersection(drop)

        if (values > 1):
            for s_column in set(df_conc.columns).difference(es_coor_conc):
                if len(set(df_conc.loc[:,s_column])) < values:
                    es_delete.add(s_column)
        if self.verbose and (len(es_delete) > 0):
            print('es_delete:', es_delete)
        df_conc.drop(es_delete, axis=1, inplace=True)

        # output
        df_conc.sort_values(['voxel_i', 'voxel_j', 'voxel_k', 'time'], axis=0, inplace=True)
        df_conc.reset_index(drop=True, inplace=True)
        df_conc.index.name = 'index'
        return df_conc


    def plot_contour(self, focus, z_slice=0.0, vmin=None, vmax=None, alpha=1, fill=True, cmap='viridis', title=None, grid=True, xlim=None, ylim=None, xyequal=True, ax=None, figsizepx=None, ext=None, figbgcolor=None, **kwargs):
        """
        input:
            focus: string
                column name within conc dataframe, for example substrate name.

            z_slice: floating point number; default is 0.0
                z-axis position to slice a 2D xy-plain out of the
                3D substrate concentration mesh. if z_slice position
                is not an exact mesh center coordinate, then z_slice
                will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.

            vmin: floating point number; default is None
                color scale min value.
                None will take the min value found in the data.

            vmax: floating point number; default is None
                color scale max value.
                None will take the max value found in the data.

            alpha: floating point number; default is 1
                alpha channel transparency value
                between 1 (not transparent at all) and 0 (totally transparent).

            fill: boolean; default is True
                True generates a matplotlib contourf plot.
                False generates a matplotlib contour plot.

            cmap: string; default is viridis
                matplotlib color map color label.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html

            title: string; default None
                possible plot title string.

            grid: boolean; default True
                should be plotted on  a grid or on a blank page?
                True will plot on a grid.

            xlim: tuple of two floating point numbers; default is None
                to specify min and max x axis value.
                None will extract agreeable values from the data.

            ylim: tuple of two floating point numbers; default is None
                to specify min and max y axis value.
                None will extract agreeable values from the data.

            xyequal: boolean; default True
                to specify equal axis spacing for x and y axis.

            ax: matplotlib axis object; default setting is None
                the ax object, which will be used as a canvas for plotting.
                None will generate a figure and ax object from scratch.

            figsizepx: list of two integers; default is None
                size of the figure in pixels, (x, y).
                the given x and y will be rounded to the nearest even number,
                to be able to generate movies from the images.
                None tries to take the values from the initial.svg file.
                fall back setting is [640, 480].

            ext: string; default is None
                output image format. possible formats are jpeg, png, and tiff.
                None will return the matplotlib fig object.

            figbgcolor: string; default is None which is transparent (png)
                or white (jpeg, tiff).
                figure background color.

            **kwargs: possible additional keyword arguments input,
                handled by the matplotlib contour and contourf function.
                + https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html
                + https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contourf.html

        output:
            fig: matplotlib figure, depending on ext, either as object or as file.
                the figure containing the contour plot and color bar.

        description:
            function returns a matplotlib contour (or contourf) plot,
            inclusive color bar, for the focus specified, either
            as matplotlib fig object or as jpeg, png, or tiff file.
        """
        # handle initial.svg for s and figsizepx
        if (figsizepx is None):
            s_pathfile = self.path + '/initial.svg'
            try:
                x_tree = etree.parse(s_pathfile)
                x_root = x_tree.getroot()
                i_width = int(np.ceil(float(x_root.get('width')))) # px
                i_height = int(np.ceil(float(x_root.get('height'))))  # px
                figsizepx = [i_width, i_height]
            except FileNotFoundError:
                if self.verbose:
                    print(f'Warning @ TimeStep.plot_contour : could not load {s_pathfile} to auto detect figsizepx. take default.')
                figsizepx = [640, 480]

        # handle figure size
        figsizepx[0] = figsizepx[0] - (figsizepx[0] % 2)  # enforce even pixel number
        figsizepx[1] = figsizepx[1] - (figsizepx[1] % 2)
        r_px = 1 / plt.rcParams['figure.dpi']  # translate px to inch
        figsize = [None, None]
        figsize[0] = figsizepx[0] * r_px
        figsize[1] = figsizepx[1] * r_px
        if self.verbose:
            print(f'px figure size set to {figsizepx}.')

        # handle z_slice input
        _, _, ar_p_axis = self.get_mesh_mnp_axis()
        if not (z_slice in ar_p_axis):
            z_slice = ar_p_axis[abs(ar_p_axis - z_slice).argmin()]
            if self.verbose:
                print(f'z_slice set to {z_slice}.')

        # get data z slice
        df_conc = self.get_conc_df(values=1, drop=set(), keep=set())
        df_conc = df_conc.loc[(df_conc.mesh_center_p == z_slice),:]
        # extend to x y domain border
        df_mmin = df_conc.loc[(df_conc.mesh_center_m == df_conc.mesh_center_m.min()), :].copy()
        df_mmin.mesh_center_m = self.get_xyz_range()[0][0]
        df_mmax = df_conc.loc[(df_conc.mesh_center_m == df_conc.mesh_center_m.max()), :].copy()
        df_mmax.mesh_center_m = self.get_xyz_range()[0][1]
        df_conc = pd.concat([df_conc, df_mmin, df_mmax], axis=0)
        df_nmin = df_conc.loc[(df_conc.mesh_center_n == df_conc.mesh_center_n.min()), :].copy()
        df_nmin.mesh_center_n =self.get_xyz_range()[1][0]
        df_nmax = df_conc.loc[(df_conc.mesh_center_n == df_conc.mesh_center_n.max()), :].copy()
        df_nmax.mesh_center_n = self.get_xyz_range()[1][1]
        df_conc = pd.concat([df_conc, df_nmin, df_nmax], axis=0)
        # sort dataframe
        df_conc.sort_values(['mesh_center_m', 'mesh_center_n', 'mesh_center_p'], inplace=True)

        # meshgrid shape
        df_mesh = df_conc.pivot(index='mesh_center_n', columns='mesh_center_m', values=focus)

        # handle vmin and vmax input
        if (vmin is None):
            vmin = np.floor(df_mesh.min().min())
        if (vmax is None):
            vmax = np.ceil(df_mesh.max().max())

        # get figure and axis orbject
        if (ax is None):
            # handle figsize
            if (figsize is None):
                figsize = (6.4, 4.8)
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = plt.gcf()

        # set equal axis spacing
        if xyequal:
            ax.axis('equal')

        # get contour plot
        if fill:
            ax.contourf(df_mesh.columns, df_mesh.index, df_mesh.values, vmin=vmin, vmax=vmax, alpha=alpha, cmap=cmap, **kwargs)
        else:
            ax.contour(df_mesh.columns, df_mesh.index, df_mesh.values, vmin=vmin, vmax=vmax, alpha=alpha, cmap=cmap, **kwargs)

        # set title
        if not (title is None):
            ax.set_title(title)

        # set grid
        ax.grid(visible=grid)

        # set axis lim
        if not (xlim is None):
            ax.set_xlim(xlim[0], xlim[1])
        if not (ylim is None):
            ax.set_ylim(ylim[0], ylim[1])

        # add colorbar to fig
        fig.colorbar(
            mappable=cm.ScalarMappable(norm=colors.Normalize(vmin=vmin, vmax=vmax), cmap=cmap),
            label=focus,
            ax=ax
        )

        # finalize
        if (ext is None):
            # output
            return fig

        else:
            # handle output path and filename
            s_path = self.path + f"/conc_{focus.replace(' ','_')}_z{round(z_slice,9)}/"
            os.makedirs(s_path, exist_ok=True)
            s_file = self.xmlfile.replace('.xml', f"_{focus.replace(' ','_')}.{ext}")
            s_pathfile = f'{s_path}{s_file}'
            # handle figure background color
            if figbgcolor is None:
                figbgcolor = 'auto'
            # plotting
            plt.tight_layout()
            fig.savefig(s_pathfile, facecolor=figbgcolor)
            plt.close(fig)
            # output
            return s_pathfile


    def make_conc_vtk(self):
        """
        input:

        output:
            s_vtkpathfile: vtk rectilinear grid file that contains
                3D distributions of all substrates over the microenvironment.

        description:
            function generates a vtk rectilinear grid file that contains
            distribution of all substrates over microenvironment.
            you can post-process this file in other software like paraview.

            https://www.paraview.org/
        """
        # off we go.
        s_vtkfile = self.xmlfile.replace('.xml','_conc.vtr')
        if self.verbose:
            print(f'processing: {s_vtkfile} ...')

        # get microenviornment data frame
        df_conc = self.get_conc_df()

        # define dimensions of the grid
        ti_dim = (
            self.get_voxel_ijk_range()[0][1] + 1,
            self.get_voxel_ijk_range()[1][1] + 1,
            self.get_voxel_ijk_range()[2][1] + 1,
        )

        # generate a rectilinear grid
        vrg_data = vtk.vtkRectilinearGrid()

        # generate and populate coordinates for the grid
        vfa_x = vtk.vtkFloatArray()
        vfa_y = vtk.vtkFloatArray()
        vfa_z = vtk.vtkFloatArray()
        vfa_x.SetNumberOfTuples(ti_dim[0])
        vfa_y.SetNumberOfTuples(ti_dim[1])
        vfa_z.SetNumberOfTuples(ti_dim[2])

        for i, m in enumerate(self.get_mesh_mnp_axis()[0]):
            vfa_x.SetValue(i, m)

        for j, n in enumerate(self.get_mesh_mnp_axis()[1]):
            vfa_y.SetValue(j, n)

        for k, p in enumerate(self.get_mesh_mnp_axis()[2]):
            vfa_z.SetValue(k, p)

        # generate and populate grid dimensions
        vrg_data.SetDimensions(ti_dim)
        vrg_data.SetXCoordinates(vfa_x)
        vrg_data.SetYCoordinates(vfa_y)
        vrg_data.SetZCoordinates(vfa_z)

        # loop over substartes to populate rectilinear grid
        b_first = True
        for s_substrate in self.get_substrate_list():
            vfa_value = vtk.vtkFloatArray()
            vfa_value.SetNumberOfComponents(1)
            vfa_value.SetNumberOfTuples(ti_dim[0] * ti_dim[1] * ti_dim[2])
            vfa_value.SetName(s_substrate)

            # populate the substrate values
            for k in range(ti_dim[2]):
                for j in range(ti_dim[1]):
                    for i in range(ti_dim[0]):
                        i_index = i + ti_dim[0] * (j + ti_dim[1] * k)
                        r_conc = df_conc.loc[
                            (df_conc.loc[:,'voxel_k'] == k) & (df_conc.loc[:,'voxel_j'] == j) & (df_conc.loc[:,'voxel_i'] == i),
                            s_substrate
                        ].values[0]
                        vfa_value.SetValue(i_index, r_conc)
            if b_first:
                vrg_data.GetPointData().SetScalars(vfa_value)
                b_first = False
            else:
                vrg_data.GetPointData().AddArray(vfa_value)

        # save vtk file
        s_vtkpathfile = self.path + '/' + s_vtkfile
        vw_writer = vtk.vtkXMLRectilinearGridWriter()
        vw_writer.SetFileName(s_vtkpathfile)
        vw_writer.SetInputData(vrg_data)
        vw_writer.Write()

        return s_vtkpathfile


    ## CELL AGENT RELATED FUNCTIONS ##

    def get_celltype_list(self):
        """
        input:

        output:
            ls_celltype: list of strings
                by ID ordered list of all tracked celltype labels.

        description:
            function returns a list with all celltype labels,
            ordered by cell_type ID.
        """
        return self.data['cell']['ls_celltype'].copy()


    def get_celltype_dict(self):
        """
        input:

        output:
            ds_celltype: dictionary of stings
                dictionary that maps cell_type IDs to labels.

        description:
            function returns a dictionary that maps ID and name from all
            cell_definitions, specified in the PhysiCell_settings.xml file.
        """
        return self.data['cell']['ds_celltype'].copy()


    def get_cell_df(self, values=1, drop=set(), keep=set()):
        """
        input:
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

        output:
            df_cell: pandas dataframe
                dataframe lists, one cell per row, all tracked variables
                values related to this cell. the variables are cell_position,
                mesh_center, and voxel coordinates, all cell_variables,
                all substrate rates and concentrations, and additional
                the surrounding cell density.

        description:
            function returns a dataframe with a cell centric view
            of the simulation.
        """
        # check keep and drop
        if (len(keep) > 0) and (len(drop) > 0):
            sys.exit(f"Error @ TimeStep.get_cell_df : when keep is given {keep}, then drop has to be an empty set {drop}!")

        # fetch data frame
        df_cell = self.data['cell']['df_cell'].copy()

        # filter
        es_attribute = set(df_cell.columns).difference(es_coor_cell)
        if (len(keep) > 0):
            es_delete = es_attribute.difference(keep)
        else:
            es_delete = es_attribute.intersection(drop)

        if (values > 1):  # by minimal number of states
            for s_column in set(df_cell.columns).difference(es_coor_cell):
                if len(set(df_cell.loc[:,s_column])) < values:
                    es_delete.add(s_column)
        if self.verbose and (len(es_delete) > 0):
            print('es_delete:', es_delete)
        df_cell.drop(es_delete, axis=1, inplace=True)

        # output
        df_cell = df_cell.loc[:,sorted(df_cell.columns)]
        df_cell.sort_values('ID', axis=0, inplace=True)
        return df_cell


    def get_cell_attribute_list(self):
        """
        input:

        output:
            ls_cellattr: list of strings
                alphabetically ordered list of all tracked cell attributes.

        description:
            function returns a list with all cell attribute labels,
            alphabetically ordered.
        """
        return self.data['cell']['ls_cellattr'].copy()


    def plot_scatter(self, focus='cell_type', z_slice=0.0, z_axis=None, alpha=1, cmap='viridis', title=None, grid=True, legend_loc='lower left', xlim=None, ylim=None, xyequal=True, s=1.0, ax=None, figsizepx=None, ext=None, figbgcolor=None, **kwargs):
        """
        input:
            focus: string; default is 'cell_type'
                column name within cell dataframe.

            z_slice: floating point number; default is 0.0
                z-axis position to slice a 2D xy-plain out of the
                3D substrate concentration mesh. if z_slice position
                is not an exact mesh center coordinate, then z_slice
                will be adjusted to the nearest mesh center value,
                the smaller one, if the coordinate lies on a saddle point.

            z_axis: for a categorical focus: set of labels;
               for a numeric focus: tuple of two floats; default is None
               depending on the focus column variable dtype, default extracts
               labels or min and max values from data.

            alpha: floating point number; default is 1.0
                alpha channel transparency value
                between 1 (not transparent at all) and 0 (totally transparent).

            cmap: dictionary of strings or string; default viridis.
                dictionary that maps labels to colors strings.
                matplotlib colormap string.
                https://matplotlib.org/stable/tutorials/colors/colormaps.html

            title: string; default None
                possible plot title string.

            grid: boolean default True.
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

            s: floating point number; default is 1.0
                scatter plot dot size scale factor.
                with figsizepx extracted from initial.svg, scale factor 1.0
                should be ok. adjust if necessary.

            ax: matplotlib axis object; default setting is None
                the ax object, which will be used as a canvas for plotting.
                None will generate a figure and ax object from scratch.

            figsizepx: list of two integers; default is None
                size of the figure in pixels, (x, y).
                the given x and y will be rounded to the nearest even number,
                to be able to generate movies from the images.
                None tries to take the values from the initial.svg file.
                fall back setting is [640, 480].

            ext: string; default is None
                output image format. possible formats are jpeg, png, and tiff.
                None will return the matplotlib fig object.

            figbgcolor: string; default is None which is transparent (png)
                or white (jpeg, tiff).
                figure background color.

            **kwargs: possible additional keyword arguments input,
                handled by the pandas dataframe plot function.
                + https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html

        output:
            fig: matplotlib figure, depending on ext, either as object or as file.
                the figure contains the scatter plot and color bar (numerical data)
                or color legend (categorical data).

        description:
            function returns a (pandas) matplotlib scatter plot,
            inclusive color bar or color legend, for the focus specified,
            either as matplotlib fig object or as jpeg, png, or tiff file.

            jpeg is by definition a lossy compressed image format.
            png is by definition a lossless compressed image format.
            tiff can by definition be a lossy or lossless compressed format.
            https://en.wikipedia.org/wiki/JPEG
            https://en.wikipedia.org/wiki/Portable_Network_Graphics
            https://en.wikipedia.org/wiki/TIFF
        """
        # handle initial.svg for figsizepx
        if (figsizepx is None):
            s_pathfile = self.path + '/initial.svg'
            try:
                x_tree = etree.parse(s_pathfile)
                x_root = x_tree.getroot()
                i_width = int(np.ceil(float(x_root.get('width')) * 2))  # px
                i_height = int(np.ceil(float(x_root.get('height')) * 2))  # px
                figsizepx = [i_width, i_height]
            except FileNotFoundError:
                if self.verbose:
                    print(f'Warning @ TimeStepts.plot_scatter : could not load {s_pathfile}.')
                figsizepx = [640, 480]

        # handle figure size
        figsizepx[0] = figsizepx[0] - (figsizepx[0] % 2)  # enforce even pixel number
        figsizepx[1] = figsizepx[1] - (figsizepx[1] % 2)
        r_px = 1 / plt.rcParams['figure.dpi']  # translate px to inch
        figsize = [None, None]
        figsize[0] = figsizepx[0] * r_px
        figsize[1] = figsizepx[1] * r_px
        if self.verbose:
            print(f'px figure size set to {figsizepx}.')

        # handle z_slice
        _, _, ar_p_axis = self.get_mesh_mnp_axis()
        if not (z_slice in ar_p_axis):
            z_slice = ar_p_axis[abs(ar_p_axis - z_slice).argmin()]
            if self.verbose:
                print(f'z_slice set to {z_slice}.')

        # get data z slice
        df_cell = self.get_cell_df(values=1, drop=set(), keep=set())
        df_cell = df_cell.loc[(df_cell.mesh_center_p == z_slice),:]

        # calculate marker size
        df_cell.loc[:,'s'] = ((6 * df_cell.total_volume) / np.pi)**(2/3)  # diamter of a sphere and plt.rcParams['lines.markersize']**2.

        # handle z_axis categorical cases
        if (str(df_cell.loc[:,focus].dtype) in {'bool', 'object'}):
            lr_extrema = [None, None]
            if (z_axis is None):
                # extract set of labels from data
                es_category = set(df_cell.loc[:,focus])
                if (str(df_cell.loc[:,focus].dtype) in {'bool'}):
                    es_category = es_category.union({True, False})
            else:
                es_category = z_axis

        # handle z_axis numerical cases
        else:  # df_cell.loc[:,focus].dtype is numeric
            es_category = None
            if (z_axis is None):
                # extract min and max values from data
                r_zmin = df_cell.loc[:,focus].min()
                r_zmax = df_cell.loc[:,focus].max()
                lr_extrema = [r_zmin, r_zmax]
            else:
                lr_extrema = z_axis

        # handle z_axis summary
        if self.verbose:
            print(f'categories found: {es_category}.')
            print(f'min max extrema set to: {lr_extrema}.')

        # handle xlim and ylim
        if (xlim is None):
            xlim = self.get_xyz_range()[0]
            if self.verbose:
                print(f'xlim set to: {xlim}.')
        if (ylim is None):
            ylim = self.get_xyz_range()[1]
            if self.verbose:
                print(f'ylim set to: {ylim}.')

        # get figure and axis orbject
        if (ax is None):
            # handle figsize
            if (figsize is None):
                figsize = (6.4, 4.8)
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = plt.gcf()

        # layout the canvas
        if xyequal:
            ax.axis('equal')

        # handle categorical variable
        if not (es_category is None):
            s_focus_color = focus + '_color'
            # use specified category color dictionary
            if type(cmap) is dict:
                ds_color = cmap
                df_cell[s_focus_color] = 'gray'
                for s_category, s_color in ds_color.items():
                    df_cell.loc[(df_cell.loc[:,focus] == s_category), s_focus_color] = s_color
            # generate category color dictionary
            else:
                ds_color = pdplt.df_label_to_color(
                    df_abc = df_cell,
                    s_focus = focus,
                    es_label = es_category,
                    s_nolabel = 'gray',
                    s_cmap = cmap,
                    b_shuffle = False,
                )
            # generate color list
            c = list(df_cell.loc[:, s_focus_color].values)
            s_cmap = None

        # handle numeric variable
        else:
            c = focus
            s_cmap = cmap

        # plot scatter
        df_cell.plot(
            kind = 'scatter',
            x = 'position_x',
            y = 'position_y',
            c = c,
            vmin = lr_extrema[0],
            vmax = lr_extrema[1],
            alpha = alpha,
            cmap = s_cmap,
            title = title,
            xlim = xlim,
            ylim = ylim,
            s = 's',
            grid = grid,
            ax = ax,
            **kwargs,
        )

        # plot categorical data legen
        if not (es_category is None):
            pdplt.ax_colorlegend(
                ax = ax,
                ds_color = ds_color,
                s_loc = legend_loc,
                s_fontsize = 'small',
            )

        # finalize
        if (ext is None):
            # output
            return fig

        else:
            # handle output path and filename
            s_path = self.path + f"/cell_{focus.replace(' ','_')}_z{round(z_slice,9)}/"
            os.makedirs(s_path, exist_ok=True)
            s_file = self.xmlfile.replace('.xml', f"_{focus.replace(' ','_')}.{ext}")
            s_pathfile = f'{s_path}{s_file}'
            # handle figure background color
            if figbgcolor is None:
                figbgcolor = 'auto'
            # plotting
            plt.tight_layout()
            fig.savefig(s_pathfile, facecolor=figbgcolor)
            plt.close(fig)
            # output
            return s_pathfile

        # output
        return fig


    def make_cell_vtk(self, attribute=['cell_type']):
        """
        input:
            attribute: list of strings; default is ['cell_type']
                column name within cell dataframe.

        output:
            s_vtkpathfile: vtk 3D glyph polynomial data file that contains cells.

        description:
            function that generates vtk 3D glyph polynomial data file for cells.
            cells can have specified attributes like cell_type,
            pressure, dead, etc.
            you can post-process this file in other software like paraview.

            https://www.paraview.org/
        """
        # off we go.
        s_vtkfile = self.xmlfile.replace('.xml','_cell.vtp')
        if self.verbose:
            print(f'processing: {s_vtkfile} ...')

        # get cell data frame
        df_cell = self.get_cell_df(values=1, drop=set(), keep=set())
        df_cell = df_cell.reset_index()

        # generate VTK instances to fill for positions and radii
        vp_points = vtk.vtkPoints()
        vfa_radii = vtk.vtkFloatArray()
        vfa_radii.SetName('radius')

        # fill VTK instance with positions and radii
        for i in df_cell.index:
            vp_points.InsertNextPoint(
                df_cell.loc[i, 'position_x'],
                df_cell.loc[i, 'position_y'],
                df_cell.loc[i, 'position_z']
            )
            vfa_radii.InsertNextValue(df_cell.loc[i, 'radius'])

        # generate data instances
        vfa_data = vtk.vtkFloatArray()
        vfa_data.SetNumberOfComponents(2)
        vfa_data.SetNumberOfTuples(df_cell.shape[0])
        vfa_data.CopyComponent(0, vfa_radii, 0)
        vfa_data.SetName('positions_and_radii')

        # generate unstructred grid for data
        vug_data = vtk.vtkUnstructuredGrid()
        vug_data.SetPoints(vp_points)
        vug_data.GetPointData().AddArray(vfa_data)
        vug_data.GetPointData().SetActiveScalars('positions_and_radii')

        # fill this grid with given attributes
        for s_attribute in attribute:
            b_bool = False
            if pd.api.types.is_bool_dtype(df_cell.loc[:, s_attribute].dtype):
                b_bool = True
                voa_data = vtk.vtkStringArray()
                print(f'boole: {s_attribute}')
            elif pd.api.types.is_string_dtype(df_cell.loc[:, s_attribute].dtype):
                voa_data = vtk.vtkStringArray()
                print(f'string: {s_attribute}')
            elif  pd.api.types.is_integer_dtype(df_cell.loc[:, s_attribute].dtype) or pd.api.types.is_float_dtype(df_cell.loc[:, s_attribute].dtype):
                voa_data = vtk.vtkFloatArray()
                print(f'numeric: {s_attribute}')
            else:
                sys.exit(f'Error @ TimeStep.make_cell_vtk : {s_attribute} {df_cell.loc[:, s_attribute].dtype} unknown df_cell column data type.')

            voa_data.SetName(s_attribute)
            for i in df_cell.index:
                if b_bool:
                    if (df_cell.loc[i, s_attribute]):
                        voa_data.InsertNextValue('True')
                    else:
                        voa_data.InsertNextValue('False')
                else:
                    voa_data.InsertNextValue(df_cell.loc[i, s_attribute])

            vug_data.GetPointData().AddArray(voa_data)

        # generate sphere source
        vss_data = vtk.vtkSphereSource()
        vss_data.SetRadius(1.0)
        vss_data.SetPhiResolution(16)
        vss_data.SetThetaResolution(32)

        # generate Glyph to save
        vg_data = vtk.vtkGlyph3D()
        vg_data.SetInputData(vug_data)
        vg_data.SetSourceConnection(vss_data.GetOutputPort())

        # define important preferences for VTK
        vg_data.ClampingOff()
        vg_data.SetScaleModeToScaleByScalar()
        vg_data.SetScaleFactor(1.0)
        vg_data.SetColorModeToColorByScalar()
        vg_data.Update()

        # write VTK
        s_vtkpathfile = self.path + '/' + s_vtkfile
        vw_writer = vtk.vtkXMLPolyDataWriter()
        vw_writer.SetFileName(s_vtkpathfile)
        vw_writer.SetInputData(vg_data.GetOutput())
        vw_writer.Write()

        return s_vtkpathfile


    ## MICROENVIRONMENT AND CELL AGENT RELATED FUNCTIONS ##

    def make_ome_tiff(self, cell_attribute='ID', conc_cutoff={}, focus=None, file=True):
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
                than zero (shifted to integer 1), another cutoff value can be
                specified here.

            focus: set of strings; default is a None
                set of substrate and cell_type names to specify what will be
                translated into ome tiff format.
                if None, all substrates and cell types will be processed.

            file: boolean; default True
                if True, an ome tiff file is the output.
                if False, a numpy array with shape czyx is the output.

        output:
            a_tczyx_img: numpy array or ome tiff file.

        description:
            function to transform chosen mcds output into an 1[um] spaced
            czyx (channel, z-axis, y-axis, x-axis) ome tiff file or numpy array,
            one substrate or cell_type per channel.
            an ome tiff file is more or less:
            a numpy array, containing the image information
            and a xml, containing the microscopy metadata information,
            like the channel labels.
            the ome tiff file format can for example be read by the napari
            or fiji (imagej) software.

            https://napari.org/stable/
            https://fiji.sc/
        """
        # handle channels
        ls_substrate = self.get_substrate_list()
        ls_celltype = self.get_celltype_list()

        if not (focus is None):
            ls_substrate = [s_substrate for s_substrate in ls_substrate if s_substrate in set(focus)]
            ls_celltype = [s_celltype for s_celltype in ls_celltype if s_celltype in set(focus)]
            if (set(focus) != set(ls_substrate).union(set(ls_celltype))):
                sys.exit(f'Error : {focus} not found in {ls_substrate} {ls_celltype}')

        # const
        ls_coor_mnp = ['mesh_center_m', 'mesh_center_n', 'mesh_center_p'] # xyz
        ls_coor_xyz = ['position_x', 'position_y', 'position_z'] # xyz
        ls_coor = ['voxel_x', 'voxel_y', 'voxel_z']

        # time step tensor
        i_time = int(self.get_time())

        # get xy coordinate dataframe
        lr_axis_z  = list(self.get_mesh_mnp_axis()[2] - self.get_voxel_spacing()[2] / 2)
        lr_axis_z.append(self.get_mesh_mnp_axis()[2][-1] + self.get_voxel_spacing()[2] / 2)
        lll_coor = []
        for i_x in range(int(round(self.get_voxel_ijk_range()[0][1] * self.get_voxel_spacing()[0]))):
            for i_y in range(int(round(self.get_voxel_ijk_range()[1][1] * self.get_voxel_spacing()[1]))):
                lll_coor.append([i_x, i_y])
        df_coor = pd.DataFrame(lll_coor, columns=ls_coor[:2])
        lr_axis_z[-1] += 1

        # extract voxel radius
        di_grow = {}
        for s_substarte in ls_substrate:
            di_grow.update({
                s_substarte : int(np.round(np.mean(self.get_voxel_spacing()[:2])) - 1)
            })

        # get and shift substrate xy data
        df_conc = self.get_conc_df()
        df_conc = df_conc.loc[:, ls_coor_mnp + ls_substrate]
        df_conc.loc[:, 'mesh_center_m'] = (df_conc.loc[:, 'mesh_center_m'] - self.get_xyz_range()[0][0]).round()
        df_conc.loc[:, 'mesh_center_n'] = (df_conc.loc[:, 'mesh_center_n'] - self.get_xyz_range()[1][0]).round()
        df_conc.rename({'mesh_center_m':'voxel_x', 'mesh_center_n':'voxel_y', 'mesh_center_p':'voxel_z'}, axis=1, inplace=True)
        df_conc = df_conc.astype({'voxel_x': int, 'voxel_y': int, 'voxel_z': float})
        # level the cake
        for s_channel in conc_cutoff.keys():
            try:
                df_conc.loc[:, s_channel] = df_conc.loc[:, s_channel] - conc_cutoff[s_channel]  + 1  # positive values starting at > 0
                df_conc.loc[(df_conc.loc[:, s_channel] <= conc_cutoff[s_channel]), s_channel] = 0
            except KeyError:
                pass


        # get cell data
        df_cell = self.get_cell_df().reset_index()

        # extract cell radius
        for s_celltype in ls_celltype:
            try:
                i_cell_grow = int(round(df_cell.loc[(df_cell.cell_type == s_celltype), 'radius'].mean()) - 1)
            except:
                i_cell_grow = 0
            di_grow.update({s_celltype : i_cell_grow})

        # filter and shift
        df_cell = df_cell.loc[:, ls_coor_xyz + ['cell_type', cell_attribute]]
        if (cell_attribute == 'cell_type'):
            sys.exit(f'Error @ TimeStep.make_ome_tiff : cell_attribute cannot be cell_type.')
        elif (df_cell.loc[:, cell_attribute].dtype == str) or (df_cell.loc[:, cell_attribute].dtype == np.object_):  # in {str, np.str_, np.object_}):
            sys.exit(f'Error @ TimeStep.make_ome_tiff : {cell_attribute} {df_cell.loc[:, cell_attribute].dtype} cell_attribute cannot be string or object. cell_attribute has to be boolean, integer, or float.')
        elif (df_cell.loc[:, cell_attribute].dtype == bool): # in {bool, np.bool_, np.bool}):
            df_cell = df_cell.astype({cell_attribute: int})
        df_cell.loc[:, 'position_x'] = (df_cell.loc[:, 'position_x'] - self.get_xyz_range()[0][0]).round()
        df_cell.loc[:, 'position_y'] = (df_cell.loc[:, 'position_y'] - self.get_xyz_range()[1][0]).round()
        df_cell.rename({'position_x':'voxel_x', 'position_y':'voxel_y', 'position_z':'voxel_z'}, axis=1, inplace=True)
        df_cell = df_cell.astype({'voxel_x': int, 'voxel_y': int, 'voxel_z': float})
        # level the cake
        df_cell.loc[:, cell_attribute] = df_cell.loc[:, cell_attribute] -  df_cell.loc[:, cell_attribute].min()  + 1  # positive values starting at > 0

        # check for duplicates: two cell at exactelly the same xyz position.
        #if self.verbose and df_cell.loc[:,['voxel_x', 'voxel_y', 'voxel_z']].duplicated().any():
        #    df_duplicate = df_cell.loc[(df_cell.loc[:, ['voxel_x', 'voxel_y', 'voxel_z']].duplicated()), :]
        #    sys.exit(f"Error @ TimeStep.make_ome_tiff : {df_duplicate} cells at exactely the same xyz voxel position detected. cannot pivot!")

        # pivot cell_type
        df_cell = df_cell.pivot_table(index=ls_coor, columns='cell_type', values=cell_attribute, aggfunc='sum').reset_index()  # fill_value is na
        for s_celltype in ls_celltype:
            if not s_celltype in set(df_cell.columns):
               df_cell[s_celltype] = 0

        # each C channel - time step tensors
        la_czyx_img = []
        ls_channel = ls_substrate + ls_celltype
        for s_channel in ls_channel:

            # get channel dataframe
            if s_channel in set(ls_substrate):
                df_channel = df_conc.loc[:, ls_coor + [s_channel]]
            elif s_channel in set(ls_celltype):
                df_channel = df_cell.loc[:, ls_coor + [s_channel]]
            else:
                sys.exit(f'Error @ TimeStep.make_ome_tiff : {s_channel} unknown channel detected. not in substrate and cell type list {ls_substrate} {ls_celltype}!')

            # each z axis
            la_zyx_img = []
            for i_zaxis in range(len(lr_axis_z)):
                if (i_zaxis < (len(lr_axis_z) - 1)):
                    print(f'processing: {i_time} [min]  {s_channel} [channel]  {i_zaxis} [z_axis] ...')
                    # extract z layer
                    df_yxchannel = df_channel.loc[
                        ((df_channel.loc[:, ls_coor[2]] >= lr_axis_z[i_zaxis]) & (df_channel.loc[:, ls_coor[2]] < lr_axis_z[i_zaxis + 1])),
                        ls_coor[:2] + [s_channel]
                    ]

                    # drop row with na and duplicate entries
                    df_yxchannel = df_yxchannel.dropna(axis=0)
                    df_yxchannel = df_yxchannel.drop_duplicates()

                    # merge with coooridnates and get image
                    # bue 20240811: df_coor left side merge will cut off reset cell that are out of the xyz domain range, which is what we want.
                    df_yxchannel = pd.merge(df_coor, df_yxchannel, on=ls_coor[:2], how='left').replace({np.nan: 0})
                    try:
                        df_yxchannel = df_yxchannel.pivot(columns=ls_coor[0], index=ls_coor[1], values=s_channel)
                    except ValueError:  # two cells from the same cell type very close to each other detetced.
                        if self.verbose:
                            df_duplicate = df_cell.loc[(df_yxchannel.loc[:, ['voxel_x', 'voxel_y']].duplicated()), :]
                            print(f'Warning: {s_channel} {df_duplicate} cells within 1[um] distance form each detected. cannot pivot. erase cell type from this timestep.')
                        df_yxchannel.loc[:,s_channel] = 0  # erase cells
                        df_yxchannel = df_yxchannel.drop_duplicates()
                        df_yxchannel = df_yxchannel.pivot(columns=ls_coor[0], index=ls_coor[1], values=s_channel)
                    a_yx_img = df_yxchannel.values

                    # grow
                    a_yx_img = imagine.grow_seed(a_yx_img, i_step=di_grow[s_channel], b_verbose=False)

                    # update output
                    la_zyx_img.append(a_yx_img)
            a_zyx_img = np.array(la_zyx_img, np.float32)
            la_czyx_img.append(np.array(a_zyx_img, np.float32))

        # output
        a_czyx_img = np.array(la_czyx_img, dtype=np.float32)

        # numpy array
        if not file:
            return a_czyx_img

        # write to file
        else:
            if self.verbose:
                print('a_czyx_img shape:', a_czyx_img.shape)
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
            s_tifffile = self.xmlfile.replace('.xml', f'{s_channel}.ome.tiff')
            s_tifffile = s_tifffile.replace(' ','_')
            if (len(s_tifffile) > 255):
                print(f"Warning: filename {len(s_tifffile)} > 255 character.")
                s_tifffile = self.xmlfile.replace('.xml', f'_channels.ome.tiff')
                print(f"file name adjusted to {s_tifffile}.")
            s_tiffpathfile = self.path + '/' + s_tifffile

            # save to file
            OmeTiffWriter.save(
                a_czyx_img,
                s_tiffpathfile,
                dim_order = 'CZYX',
                #ome_xml=x_img,
                channel_names = ls_channel,
                image_names = [s_tifffile.replace('.ome.tiff','')],
                physical_pixel_sizes = bioio_base.types.PhysicalPixelSizes(self.get_voxel_spacing()[2], 1.0, 1.0),  # z,y,x [um]
                #channel_colors=,
                #fs_kwargs={},
            )
            return s_tiffpathfile


    def render_neuroglancer(self, tiffpathfile, timestep=0, intensity_cmap='gray'):
        """
        help(pcdl.render_neuroglancer)
        try: mcds.render_neuroglancer(mcds.make_ome_tiff())
        """
        o_viewer = render_neuroglancer(
            tiffpathfile = tiffpathfile,
            timestep = timestep,
            intensity_cmap = intensity_cmap,
        )
        return o_viewer


    ## GRAPH RELATED FUNCTIONS ##

    def get_attached_graph_dict(self):
        """
        input:

        output:
            dei_graph: dictionary of sets of integers
                maps each cell ID to the attached connected cell IDs.

        description:
            function returns the attached cell graph as a dictionary object.
        """
        return self.data['cell']['dei_graph']['attached_cells'].copy()


    def get_neighbor_graph_dict(self):
        """
        input:

        output:
            dei_graph: dictionary of sets of integers
                maps each cell ID to the connected neighbor cell IDs.

        description:
            function returns the cell neighbor graph as a dictionary object.
        """
        return self.data['cell']['dei_graph']['neighbor_cells'].copy()


    def get_spring_graph_dict(self):
        """
        input:

        output:
            dei_graph: dictionary of sets of integers
                maps each cell ID to the attached connected cell IDs.

        description:
            function returns the attached spring cell graph as a dictionary object.
        """
        return self.data['cell']['dei_graph']['spring_attached_cells'].copy()


    def make_graph_gml(self, graph_type, edge_attribute=True, node_attribute=[]):
        """
        input:
            graph_type: string
                to specify which physicell output data should be processed.
                neighbor, touch: processes mcds.get_neighbor_graph_dict dictionary.
                attached: processes mcds.get_attached_graph_dict dictionary.
                spring: processes mcds.get_spring_graph_dict dictionary.

            edge_attribute: boolean; default True
                specifies if the spatial Euclidean distance is used for
                edge attribute, to generate a weighted graph.

            node_attribute: list of strings; default is empty list
                list of mcds.get_cell_df dataframe columns, used for
                node attributes.

        output:
            gml file, generated under the returned path.

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
        # load dataframe for celltype information
        df_cell = self.get_cell_df()
        ds_unit = self.get_unit_dict()
        s_unit_simtime = ds_unit["time"]
        r_simtime = self.get_time()
        if (graph_type in {'attached'}):
            dei_graph = self.get_attached_graph_dict()
        elif (graph_type in {'neighbor', 'touch'}):
            dei_graph = self.get_neighbor_graph_dict()
        elif (graph_type in {'spring'}):
            dei_graph = self.get_spring_graph_dict()
        #elif (graph_type in {'evo','devo','lineage'}):
        #    dei_graph = self.get_lineage_graph_dict()
        else:
            sys.exit(f'Erro @ make_graph_gml : unknown graph_type {graph_type}. known are attached, neighbor, spring, and touch.')

        # generate filename
        s_gmlpathfile = self.path + '/' + self.xmlfile.replace('.xml',f'_{graph_type}.gml')

        # open result gml file
        f = open(s_gmlpathfile, 'w')
        f.write(f'Creator "pcdl_v{__version__}"\ngraph [\n')
        f.write(f'  id {int(r_simtime)}\n  comment "time_{s_unit_simtime}"\n  label "{graph_type}_graph"\n  directed 0\n')
        for i_src, ei_dst in dei_graph.items():
            #print(f'{i_src} {sorted(ei_dst)}')
            # node
            f.write(f'  node [\n    id {i_src}\n    label "node_{i_src}"\n')
            # node attributes
            for s_attribute in node_attribute:
                o_attribute = df_cell.loc[i_src, s_attribute]
                if (type(o_attribute) == str) or (o_attribute.dtype == np.object_):  #in {str, np.str_, np.object_}):
                    f.write(f'    {s_attribute} "{o_attribute}"\n')
                elif (o_attribute.dtype == bool) or (o_attribute.dtype == int):  #in {bool, np.bool_, np.bool, int, np.int_, np.int8, np.int16, np.int32, np.int64}):
                    f.write(f'    {s_attribute} {int(o_attribute)}\n')
                elif (o_attribute.dtype == float):  #in {float, np.float16, np.float32, np.float64, np.float128}):
                    f.write(f'    {s_attribute} {o_attribute}\n')
                else:
                    sys.exit(f'Error @ TimeStep.make_graph_gml : attribute {o_attribute}; type {o_attribute.dtype}; type seems not to be bool, int, float, or string.')
            f.write(f'  ]\n')
            # edge
            for i_dst in ei_dst:
                if (i_src < i_dst):
                    f.write(f'  edge [\n    source {i_src}\n    target {i_dst}\n    label "edge_{i_src}_{i_dst}"\n')
                    if (edge_attribute):
                        # edge distance attribute
                        x = df_cell.loc[i_src, 'position_x'] - df_cell.loc[i_dst, 'position_x']
                        y = df_cell.loc[i_src, 'position_y'] - df_cell.loc[i_dst, 'position_y']
                        z = df_cell.loc[i_src, 'position_z'] - df_cell.loc[i_dst, 'position_z']
                        r_distance = (x**2 + y**2 + z**2)**(1/2)
                        f.write(f'    distance_{ds_unit["position_y"]} {round(r_distance)}\n')
                    f.write(f'  ]\n')
            # development
            #if (i_src > 16):
            #    break
        # close result gml file
        f.write(']\n')
        f.close()

        # output
        return s_gmlpathfile


    ## ANNDATA RELATED FUNCTIONS ##

    def get_anndata(self, values=1, drop=set(), keep=set(), scale='maxabs'):
        """
        input:
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
                don't worry: essential columns like ID, coordinates
                and time will always be kept.

            scale: string; default 'maxabs'
                specify how the data should be scaled.
                possible values are None, maxabs, minmax, std.
                for more input, check out: help(pcdl.scaler)

        output:
            annmcds: anndata object
                for this one time step.

        description:
            function to transform a mcds time step into an anndata object
            for downstream analysis.
        """
        # processing
        if self.verbose:
            print(f'processing: 1/1 {round(self.get_time(),9)}[min] mcds into anndata obj.')
        df_cell = self.get_cell_df(values=values, drop=drop, keep=keep)
        df_count, df_obs, d_obsm, d_obsp, d_uns = _anndextract(
            df_cell = df_cell,
            scale = scale,
            graph_attached = self.get_attached_graph_dict(),
            graph_neighbor = self.get_neighbor_graph_dict(),
            graph_method = self.get_physicell_version(),
        )
        annmcds = ad.AnnData(
            X = df_count,
            obs = df_obs,
            obsm = d_obsm,
            obsp = d_obsp,
            uns = d_uns
        )
        # output
        return annmcds


    ## LOAD DATA  ##

    def _read_xml(self, xmlfile, output_path='.'):
        """
        input:
            self: TimeStep class instance.

            xmlfile: string
                name of the xml file with or without path
                in the with path case, output_path has to be set to the default!

            output_path: string; default '.'
                relative or absolute path to the directory where
                the PhysiCell output files are stored.

        output:
            self: TimeStep class instance with loaded data.

        description:
            internal function to load the data from the PhysiCell output files
            into the TimeStep instance.
        """
        #####################
        # path and filename #
        #####################

        # file and path manipulation
        s_xmlfile = xmlfile.replace('\\','/')
        if (xmlfile.find('/') > -1) and (output_path == '.'):
            ls_xmlfile = xmlfile.split('/')
            s_xmlfile = ls_xmlfile.pop(-1)
            output_path = '/'.join(ls_xmlfile)
        while (output_path.find('//') > -1):
            output_path = output_path.replace('//','/')
        if (output_path.endswith('/')) and (len(output_path) > 1):
            output_path = output_path[:-1]
        self.path = output_path
        self.xmlfile = s_xmlfile

        # set flag
        b_celltype = False

        # generate output dictionary
        d_mcds = {
           'metadata': {},
           'mesh': {},
           'substrate': {
               'ds_substrate': {},
           },
           'metadata': {},
           'cell': {
               'ds_celltype': {},
           },
           'raw_substrate': {},
           'raw_cell': {
               'units': {},
           },
        }

        ###############################
        # read PhysiCell_settings.xml #
        ###############################
        ## get celltype dict
        # bue: used for cell_type label:id mapping for data generated with physicell versions < 3.15.

        if not ((self.settingxml is None) or (self.settingxml is False)):
            # load Physicell_settings xml file
            s_settingxmlpathfile = self.path + '/' + self.settingxml
            x_tree = etree.parse(s_settingxmlpathfile)
            if self.verbose:
                print(f'reading: {s_settingxmlpathfile}')
            self.x_settingxml = x_tree.getroot()

            # metadata cell_type label:id mapping detection (silver quality)
            for x_celltype in self.x_settingxml.find('cell_definitions').findall('cell_definition'):
                # <cell_definition>
                s_id = str(x_celltype.get('ID'))
                # I don't like spaces in cell type names!
                s_celltype = x_celltype.get('name') #.replace(' ','_') # ROH
                d_mcds['cell']['ds_celltype'].update({s_id : s_celltype})
            b_celltype = True

        #######################################
        # read physicell output xml path/file #
        #######################################

        s_xmlpathfile = self.path + '/' + self.xmlfile
        x_tree = etree.parse(s_xmlpathfile)
        if self.verbose:
            print(f'reading: {s_xmlpathfile}')
        x_root = x_tree.getroot()


        ###################
        # handle metadata #
        ###################

        if self.verbose:
            print('working on metadata ...')

        ### find the metadata node ###
        x_metadata = x_root.find('metadata')

        ## get multicellds xml version
        d_mcds['metadata']['multicellds_version'] = f"MultiCellDS_{x_root.get('version')}"

        ## get physicell software version
        x_software = x_metadata.find('software')
        x_physicelln = x_software.find('name')
        x_physicellv = x_software.find('version')
        d_mcds['metadata']['physicell_version'] = f'{x_physicelln.text}_{x_physicellv.text}'

        ## get timestamp
        x_time = x_metadata.find('created')
        d_mcds['metadata']['created'] = x_time.text

        ## get current simulated time
        x_time = x_metadata.find('current_time')
        d_mcds['metadata']['current_time'] = float(x_time.text)
        d_mcds['metadata']['time_units'] = x_time.get('units')

        ## get current runtime
        x_time = x_metadata.find('current_runtime')
        d_mcds['metadata']['current_runtime'] = float(x_time.text)
        d_mcds['metadata']['runtime_units'] = x_time.get('units')


        ####################
        # handle mesh data #
        ####################

        if self.verbose:
            print('working on mesh data ...')

        ### find the mesh node ###
        x_microenv = x_root.find('microenvironment').find('domain')  # find the microenvironment node
        x_mesh = x_microenv.find('mesh')
        d_mcds['metadata']['spatial_unit'] = x_mesh.get('units')

        # while we're at it, find the mesh
        s_x_coor = x_mesh.find('x_coordinates').text
        s_delim = x_mesh.find('x_coordinates').get('delimiter')
        ar_x_coor = np.array(s_x_coor.split(s_delim), dtype=np.float64)

        s_y_coor = x_mesh.find('y_coordinates').text
        s_delim = x_mesh.find('y_coordinates').get('delimiter')
        ar_y_coor = np.array(s_y_coor.split(s_delim), dtype=np.float64)

        s_z_coor = x_mesh.find('z_coordinates').text
        s_delim = x_mesh.find('z_coordinates').get('delimiter')
        ar_z_coor = np.array(s_z_coor.split(s_delim), dtype=np.float64)

        ## get mesh grid
        d_mcds['mesh']['mnp_grid'] = np.array(np.meshgrid(ar_x_coor, ar_y_coor, ar_z_coor, indexing='xy'))

        ## get mesh center axis
        d_mcds['mesh']['mnp_axis'] = [
            np.unique(ar_x_coor),
            np.unique(ar_y_coor),
            np.unique(ar_z_coor),
        ]

        ## get mesh center range
        d_mcds['mesh']['mnp_range'] = [
           (d_mcds['mesh']['mnp_axis'][0].min(), d_mcds['mesh']['mnp_axis'][0].max()),
           (d_mcds['mesh']['mnp_axis'][1].min(), d_mcds['mesh']['mnp_axis'][1].max()),
           (d_mcds['mesh']['mnp_axis'][2].min(), d_mcds['mesh']['mnp_axis'][2].max()),
        ]

        ## get voxel range
        d_mcds['mesh']['ijk_range'] = [
            (0, len(d_mcds['mesh']['mnp_axis'][0]) - 1),
            (0, len(d_mcds['mesh']['mnp_axis'][1]) - 1),
            (0, len(d_mcds['mesh']['mnp_axis'][2]) - 1),
        ]

        ## get voxel axis
        d_mcds['mesh']['ijk_axis'] = [
            np.array(range(d_mcds['mesh']['ijk_range'][0][1] + 1)),
            np.array(range(d_mcds['mesh']['ijk_range'][1][1] + 1)),
            np.array(range(d_mcds['mesh']['ijk_range'][2][1] + 1)),
        ]

        ## get mesh bounding box range [xmin, ymin, zmin, xmax, ymax, zmax]
        s_bboxcoor = x_mesh.find('bounding_box').text
        s_delim = x_mesh.find('bounding_box').get('delimiter')
        ar_bboxcoor = np.array(s_bboxcoor.split(s_delim), dtype=np.float64)

        d_mcds['mesh']['xyz_range'] = [
            (ar_bboxcoor[0], ar_bboxcoor[3]),
            (ar_bboxcoor[1], ar_bboxcoor[4]),
            (ar_bboxcoor[2], ar_bboxcoor[5]),
        ]

        # voxel data must be loaded from .mat file
        s_voxelpathfile = self.path + '/' + x_mesh.find('voxels').find('filename').text
        ar_mesh_initial = io.loadmat(s_voxelpathfile)['mesh']
        if self.verbose:
            print(f'reading: {s_voxelpathfile}')

        ## get voxle coordinates
        # center of voxel specified by first three rows [ x, y, z ]
        d_mcds['mesh']['mnp_coordinate'] = ar_mesh_initial[:3, :]

        ## get voxel volume
        # volume specified by fourth row
        ar_volume = ar_mesh_initial[3, :]
        if (len(set(ar_volume)) != 1):
            sys.exit(f'Error @ TimeStep._read_xml : mesh is not built out of a unique voxel volume {ar_volume}.')
        d_mcds['mesh']['volume'] = ar_volume[0]

        ## get mesh voxel spacing
        tr_m_range, tr_n_range, tr_p_range = d_mcds['mesh']['mnp_range']
        ar_m_axis, ar_n_axis, ar_p_axis = d_mcds['mesh']['mnp_axis']

        if (len(set(tr_m_range)) == 1):  # m axis
            dm = np.float64(1.0)
        else:
            dm = (tr_m_range[1] - tr_m_range[0]) / (ar_m_axis.shape[0] - 1)

        if (len(set(tr_n_range)) == 1):  # n axis
            dn = np.float64(1.0)
        else:
            dn = (tr_n_range[1] - tr_n_range[0]) / (ar_n_axis.shape[0] - 1)

        dp  = d_mcds['mesh']['volume'] / (dm * dn)  # p axis

        d_mcds['mesh']['mnp_spacing'] = [dm, dn, dp]


        ################################
        # handle microenvironment data #
        ################################

        if self.microenv:
            if self.verbose:
                print('working on microenvironment data ...')

            # micro environment data is shape [4+n, len(voxels)] where n is the number
            # of species being tracked. the first 3 rows represent (x, y, z) of voxel
            # centers. The fourth row contains the voxel volume. The 5th row and up will
            # contain values for that species in that voxel.
            s_microenvpathfile = self.path + '/' +  x_microenv.find('data').find('filename').text
            ar_microenv = io.loadmat(s_microenvpathfile)['multiscale_microenvironment']
            if self.verbose:
                print(f'reading: {s_microenvpathfile}')

            # raw_substrate, unlike in the matlab version the individual chemical
            # species will be primarily accessed through their names e.g.
            # d_mcds['raw_substrate']['oxygen']['units']
            # d_mcds['raw_substrate']['glucose']['data']

            # substrate loop
            for i_s, x_substrate in enumerate(x_microenv.find('variables').findall('variable')):
                # i don't like spaces in species names!
                s_substrate = x_substrate.get('name') #.replace(' ','_') # ROH

                d_mcds['raw_substrate'][s_substrate] = {}
                d_mcds['raw_substrate'][s_substrate]['units'] = x_substrate.get('units')

                if self.verbose:
                    print(f'parsing: {s_substrate} data')

                # update metadata substrate ID label dictionary
                d_mcds['substrate']['ds_substrate'].update({str(i_s) : s_substrate})

                # initialize meshgrid shaped array for concentration data
                d_mcds['raw_substrate'][s_substrate]['data'] = np.zeros(d_mcds['mesh']['mnp_grid'][0].shape)

                # diffusion data for each species
                d_mcds['raw_substrate'][s_substrate]['diffusion_coefficient'] = {}
                d_mcds['raw_substrate'][s_substrate]['diffusion_coefficient']['value'] = float(x_substrate.find('physical_parameter_set').find('diffusion_coefficient').text)
                d_mcds['raw_substrate'][s_substrate]['diffusion_coefficient']['units'] = x_substrate.find('physical_parameter_set').find('diffusion_coefficient').get('units')

                # decay data for each species
                d_mcds['raw_substrate'][s_substrate]['decay_rate'] = {}
                d_mcds['raw_substrate'][s_substrate]['decay_rate']['value']  = float(x_substrate.find('physical_parameter_set').find('decay_rate').text)
                d_mcds['raw_substrate'][s_substrate]['decay_rate']['units']  = x_substrate.find('physical_parameter_set').find('decay_rate').get('units')

                # store data from microenvironment file as numpy array
                # iterate over each voxel
                # bue: i have a hunch this could be faster reimplemented.
                for i_voxel in range(d_mcds['mesh']['mnp_coordinate'].shape[1]):

                    # find the voxel coordinate
                    ar_center = d_mcds['mesh']['mnp_coordinate'][:, i_voxel]
                    i = np.where(np.abs(ar_center[0] - d_mcds['mesh']['mnp_axis'][0]) < 1e-10)[0][0]
                    j = np.where(np.abs(ar_center[1] - d_mcds['mesh']['mnp_axis'][1]) < 1e-10)[0][0]
                    k = np.where(np.abs(ar_center[2] - d_mcds['mesh']['mnp_axis'][2]) < 1e-10)[0][0]

                    # store value
                    d_mcds['raw_substrate'][s_substrate]['data'][j, i, k] = ar_microenv[4+i_s, i_voxel]

        ## get substrate listing
        ds_substrate =  d_mcds['substrate']['ds_substrate']
        ls_substrate = [ds_substrate[s_key] for s_key in sorted(ds_substrate, key=int)]
        # store values
        d_mcds['substrate']['ls_substarte'] = ls_substrate

        ## get substrate df
        # extract data
        ls_column = ['substrate','decay_rate','diffusion_coefficient']
        ll_sub = []
        for s_substrate in d_mcds['substrate']['ls_substarte']:
            s_decay_value = d_mcds['raw_substrate'][s_substrate]['decay_rate']['value']
            s_diffusion_value = d_mcds['raw_substrate'][s_substrate]['diffusion_coefficient']['value']
            ll_sub.append([s_substrate, s_decay_value, s_diffusion_value])
        # generate dataframe
        df_substrate = pd.DataFrame(ll_sub, columns=ls_column)
        df_substrate.set_index('substrate', inplace=True)
        df_substrate.columns.name = 'attribute'
        # store values
        d_mcds['substrate']['df_substarte'] = df_substrate

        ## get conc df
        # flatten mesh coordnates
        ar_m, ar_n, ar_p = d_mcds['mesh']['mnp_grid']
        ar_m = ar_m.flatten(order='C')
        ar_n = ar_n.flatten(order='C')
        ar_p = ar_p.flatten(order='C')
        # get mesh spacing
        dm, dn, dp = d_mcds['mesh']['mnp_spacing']
        # get voxel coordinates
        ai_i = ((ar_m - ar_m.min()) / dm)
        ai_j = ((ar_n - ar_n.min()) / dn)
        ai_k = ((ar_p - ar_p.min()) / dp)
        # handle coordinates
        ls_column = [
            'voxel_i','voxel_j','voxel_k',
            'mesh_center_m','mesh_center_n','mesh_center_p'
        ]
        la_data = [ai_i, ai_j, ai_k, ar_m, ar_n, ar_p]
        # handle concentrations
        for s_substrate in d_mcds['substrate']['ls_substarte']:
            ls_column.append(s_substrate)
            ar_conc = d_mcds['raw_substrate'][s_substrate]['data'].copy()
            la_data.append(ar_conc.flatten(order='C'))
        # generate dataframe
        aa_data  = np.array(la_data)
        df_conc = pd.DataFrame(aa_data.T, columns=ls_column)
        df_conc['time'] = d_mcds['metadata']['current_time']
        df_conc['runtime'] = d_mcds['metadata']['current_runtime'] / 60  # in min
        df_conc['xmlfile'] = self.xmlfile
        d_dtype = {'voxel_i': int, 'voxel_j': int, 'voxel_k': int}
        df_conc = df_conc.astype(d_dtype)
        # store values
        df_conc.sort_values(['voxel_i', 'voxel_j', 'voxel_k', 'time'], axis=0, inplace=True)
        df_conc.reset_index(drop=True, inplace=True)
        df_conc.index.name = 'index'
        d_mcds['substrate']['df_conc'] = df_conc


        ####################
        # handle cell data #
        ####################
        if self.verbose:
            print('working on discrete cell data ...')

        # in order to get to the good stuff, we have to pass through a few different hierarchical levels
        x_cell = x_root.find('cellular_information').find('cell_populations').find('cell_population').find('custom')

        # we want the PhysiCell data, there is more of it
        for x_simplified_data in x_cell.findall('simplified_data'):
            if x_simplified_data.get('source') == 'PhysiCell':
                x_celldata = x_simplified_data
                break

        # update cell_type ID label dictionar
        # metadata cell_type label:id mapping detection ~ physicell version >= 3.15 (gold quality)
        try:
            for x_celltype in x_celldata.find('cell_types').findall('type'):
                s_id = str(x_celltype.get('ID'))
                # I don't like spaces in cell type names!
                s_celltype = x_celltype.text #.replace(' ','_')  # ROH
                d_mcds['cell']['ds_celltype'].update({s_id : s_celltype})
            b_celltype = True
        except AttributeError:
            pass

        # metadata cell_type label:id mapping detection ~ label information lost (silver quality)
        if not b_celltype:
            for x_label in x_celldata.find('labels').findall('label'):
                # I don't like spaces in cell type names!
                s_variable = x_label.tex #.replace(' ','_')  # ROH
                if s_variable in es_var_cell:
                    for i_id in range(int(x_label.get('size'))):
                        s_id = str(i_id)
                        d_mcds['cell']['ds_celltype'].update({s_id : s_id})
                    b_celltype = True

        # iterate over labels which are children of labels these will be used to label data arrays
        ls_variable = []
        for x_label in x_celldata.find('labels').findall('label'):
            # I don't like spaces in my dictionary keys!
            s_variable = x_label.text #.replace(' ','_')  # ROH
            i_variable = int(x_label.get('size'))
            s_unit = x_label.get('units')

            # variable unique for each celltype substrate combination
            if s_variable in es_var_subs:
                if (len(d_mcds['substrate']['ds_substrate']) > 0):
                    # continuum_variable id label sorting (becaus this is an id label mapping dict)
                    ls_substrate = [d_mcds['substrate']['ds_substrate'][o_key] for o_key in sorted(d_mcds['substrate']['ds_substrate'].keys(), key=int)]
                    for s_substrate in ls_substrate:
                        s_variable_subs = s_substrate + '_' + s_variable
                        ls_variable.append(s_variable_subs)
                        d_mcds['raw_cell']['units'].update({s_variable_subs : s_unit})
                else:
                    ls_substrate = [str(i_substrate) for i_substrate in range(i_variable)]
                    for s_substrate in ls_substrate:
                        s_variable_subs = s_variable + '_' + s_substrate
                        ls_variable.append(s_variable_subs)
                        d_mcds['raw_cell']['units'].update({s_variable_subs : s_unit})

            # variable unique for each celltype celltype combination
            elif s_variable in es_var_cell:
                if (len(d_mcds['cell']['ds_celltype']) > 0):
                    # raw_cell id label sorting (becaus this is an id label mapping dict)
                    ls_celltype = [d_mcds['cell']['ds_celltype'][o_key] for o_key in sorted(d_mcds['cell']['ds_celltype'].keys(), key=int)]
                    for s_celltype in ls_celltype:
                        s_variable_celltype = s_celltype + '_' + s_variable
                        ls_variable.append(s_variable_celltype)
                        d_mcds['raw_cell']['units'].update({s_variable_celltype : s_unit})
                else:
                    ls_celltype = [str(i_celltype) for i_celltype in range(i_variable)]
                    for s_celltype in ls_celltype:
                        s_variable_celltype = s_variable + '_' + s_celltype
                        ls_variable.append(s_variable_celltype)
                        d_mcds['raw_cell']['units'].update({s_variable_celltype : s_unit})

            # variable unique for each dead model
            elif s_variable in es_var_death:
                for i_deathrate in range(i_variable):
                    s_variable_deathrate = s_variable + '_' + str(i_deathrate)
                    ls_variable.append(s_variable_deathrate)
                    d_mcds['raw_cell']['units'].update({s_variable_deathrate : s_unit})

            # spatial variable
            elif s_variable in es_var_spatial:
                for s_axis in ['_x','_y','_z']:
                    s_variable_spatial = s_variable + s_axis
                    ls_variable.append(s_variable_spatial)
                    d_mcds['raw_cell']['units'].update({s_variable_spatial: s_unit})

            # simple variable and vectors
            else:
                if (i_variable > 1):
                    for i_n in range(i_variable):
                        ls_variable.append(f'{s_variable}_{str(i_n).zfill(3)}')
                else:
                    ls_variable.append(s_variable)
                d_mcds['raw_cell']['units'].update({s_variable : s_unit})

        # load the file
        s_cellpathfile = self.path + '/' + x_celldata.find('filename').text
        try:
            ar_cell = io.loadmat(s_cellpathfile)['cells']
            if self.verbose:
                print(f'reading: {s_cellpathfile}')
        except ValueError:  # hack: some old PhysiCell versions generates a corrupt cells.mat file, if there are zero cells.
            if self.verbose:
                print(f'Warning @ TimeStep._read_xml : corrupt {s_cellpathfile} detected!\nassuming time step with zero cells because of a known bug in PhysiCell MultiCellDS version 0.5 output.')
            ar_cell = np.empty([len(ls_variable),0])

        # check for column label mapping error (as good as it gets)
        if (ar_cell.shape[0] != len(ls_variable)):
            sys.exit(f'Error @ TimeStep._read_xml : extracted column label list leng {len(ls_variable)} and data array shape {ar_cell.shape} are incompatible!')

        # metadata cell_type label:id mapping detection ~ label information lost (bronze quality)
        if not b_celltype:
            for r_celltype in set(ar_cell[ls_variable.index('cell_type'),:]):
                s_celltype = str(int(r_celltype))
                d_mcds['cell']['ds_celltype'].update({s_celltype : s_celltype})
            b_celltype = True

        # store data
        d_mcds['raw_cell']['data'] = {}
        for i_col in range(len(ls_variable)):
            d_mcds['raw_cell']['data'].update({ls_variable[i_col]: ar_cell[i_col,:]})


        ## get celltype list
        ds_celltype = d_mcds['cell']['ds_celltype']
        ls_celltype = [ds_celltype[s_key] for s_key in sorted(ds_celltype, key=int)]
        # store values
        d_mcds['cell']['ls_celltype'] = ls_celltype


        ## get cell df
        # get cell position and more
        df_cell = pd.DataFrame(d_mcds['raw_cell']['data'])
        df_cell['time'] = d_mcds['metadata']['current_time']
        df_cell['runtime'] = d_mcds['metadata']['current_runtime'] / 60  # in min
        df_cell['xmlfile'] = self.xmlfile
        df_voxel = df_cell.loc[:,['position_x','position_y','position_z']].copy()

        # get mesh spacing
        dm, dn, dp = d_mcds['mesh']['mnp_spacing']

        # get mesh and voxel min max values
        tr_m_range, tr_n_range, tr_p_range = d_mcds['mesh']['mnp_range']
        tr_i_range, tr_j_range, tr_k_range = d_mcds['mesh']['ijk_range']

        # get voxel for each cell
        df_voxel.loc[:,'voxel_i'] = np.round((df_voxel.loc[:,'position_x'] - tr_m_range[0]) / dm).astype(int)
        df_voxel.loc[:,'voxel_j'] = np.round((df_voxel.loc[:,'position_y'] - tr_n_range[0]) / dn).astype(int)
        df_voxel.loc[:,'voxel_k'] = np.round((df_voxel.loc[:,'position_z'] - tr_p_range[0]) / dp).astype(int)
        df_voxel.loc[(df_voxel.voxel_i > tr_i_range[1]), 'voxel_i'] = tr_i_range[1]  # i_max
        df_voxel.loc[(df_voxel.voxel_i < tr_i_range[0]), 'voxel_i'] = tr_i_range[0]  # i_min
        df_voxel.loc[(df_voxel.voxel_j > tr_j_range[1]), 'voxel_j'] = tr_j_range[1]  # j_max
        df_voxel.loc[(df_voxel.voxel_j < tr_j_range[0]), 'voxel_j'] = tr_j_range[0]  # j_min
        df_voxel.loc[(df_voxel.voxel_k > tr_k_range[1]), 'voxel_k'] = tr_k_range[1]  # k_max
        df_voxel.loc[(df_voxel.voxel_k < tr_k_range[0]), 'voxel_k'] = tr_k_range[0]  # k_min

        # merge voxel (inner join)
        df_cell = pd.merge(df_cell, df_voxel, on=['position_x', 'position_y', 'position_z'])

        # merge cell_density (left join)
        df_cellcount = df_cell.loc[:,['voxel_i','voxel_j','voxel_k','ID']].groupby(['voxel_i','voxel_j','voxel_k']).count().reset_index()
        ls_column = list(df_cellcount.columns)
        ls_column[-1] = 'cell_count_voxel'
        df_cellcount.columns = ls_column
        s_density = f"cell_density_{d_mcds['metadata']['spatial_unit']}3"
        df_cellcount[s_density] = df_cellcount.loc[:,'cell_count_voxel'] / d_mcds['mesh']['volume']
        df_cell = pd.merge(
            df_cell,
            df_cellcount,
            on = ['voxel_i', 'voxel_j', 'voxel_k'],
            how = 'left',
        )

        # get column label set
        es_column = set(df_cell.columns)

        # get vector length
        for s_var_spatial in es_var_spatial:
            es_vector = es_column.intersection({f'{s_var_spatial}_x',f'{s_var_spatial}_y',f'{s_var_spatial}_z'})
            if len(es_vector) > 0:
                # linear algebra
                #a_vector = df_cell.loc[:,ls_vector].values
                #a_length = np.sqrt(np.diag(np.dot(a_vector, a_vector.T)))
                # pythoagoras
                a_length = None
                for s_vector in es_vector:
                    a_vectorsq = df_cell.loc[:,s_vector].values**2
                    if (a_length is None):
                        a_length = a_vectorsq
                    else:
                        a_length += a_vectorsq
                a_length = a_length**(1/2)
                # result
                df_cell[f'{s_var_spatial}_vectorlength'] = a_length

        # physiboss
        if self.physiboss:
            if self.verbose:
                print('working on physiboss data ...')

            # intracellular file (hack because this is not yet in output.xml)
            df_physiboss = None
            s_intracellpathfile = self.path + f'/states_{self.xmlfile.replace("output","").replace(".xml",".csv")}'
            if os.path.exists(s_intracellpathfile):
                if self.verbose:
                    print(f'reading: {s_intracellpathfile}')

                # load state
                df_physiboss = pd.read_csv(s_intracellpathfile, index_col=0)

                # add nodes
                df_physiboss[f'state_nil'] = df_physiboss.state.str.find('<nil>') > -1
                es_node = set()
                for s_state in df_physiboss.state.unique():
                    es_node = es_node.union(set(s_state.split(' -- ')))
                es_node.discard('<nil>')
                for s_node in sorted(es_node):
                    df_physiboss[f'node_{s_node}'] = df_physiboss.state.str.find(s_node) > -1

                # store data
                df_cell = pd.merge(
                    df_cell,
                    df_physiboss,
                    left_index = True,
                    right_index = True,
                    how = 'left',
                )

            elif self.verbose:
                print(f'Warning @ TimeStep._read_xml : physiboss file missing {s_intracellpathfile}.')

            else:
                pass


        # microenvironment
        if self.microenv:
            # merge substrate (left join)
            df_sub = d_mcds['substrate']['df_substarte']
            for s_sub in df_sub.index:
                 for s_rate in df_sub.columns:
                     s_var = f'{s_sub}_{s_rate}'
                     df_cell[s_var] = df_sub.loc[s_sub,s_rate]

        # merge concentration (left join)
        df_conc = d_mcds['substrate']['df_conc'].copy()  # voxel and mesh coordinates
        df_conc.drop({'time', 'runtime','xmlfile'}, axis=1, inplace=True)
        df_cell = pd.merge(
            df_cell,
            df_conc,
            on = ['voxel_i', 'voxel_j', 'voxel_k'],
            how = 'left',
        )

        # variable typing
        do_type = {}
        [do_type.update({k:v}) for k,v in do_var_type.items() if k in es_column]
        do_type.update(self.custom_data_type)
        do_int = do_type.copy()
        [do_int.update({k:int}) for k in do_int.keys()]
        ls_int = sorted(do_int.keys())
        df_cell.loc[:,ls_int] = df_cell.loc[:,ls_int].round()
        df_cell = df_cell.astype(do_int)
        df_cell = df_cell.astype(do_type)

        # categorical translation
        try:  # bue 20240805: missing in MCDS version <= 0.5 (November 2021)
            df_cell.loc[:,'current_death_model'] = df_cell.loc[:,'current_death_model'].replace(ds_death_model)  # bue 20230614: this column looks like an artefact to me
        except KeyError:
            pass
        df_cell.loc[:,'cycle_model'] = df_cell.loc[:,'cycle_model'].replace(ds_cycle_model)
        df_cell.loc[:,'cycle_model'] = df_cell.loc[:,'cycle_model'].replace(ds_death_model)
        df_cell.loc[:,'current_phase'] = df_cell.loc[:,'current_phase'].replace(ds_cycle_phase)
        df_cell.loc[:,'current_phase'] = df_cell.loc[:,'current_phase'].replace(ds_death_phase)
        df_cell.loc[:,'cell_type'] = df_cell.loc[:,'cell_type'].replace(d_mcds['cell']['ds_celltype'])
        df_cell.loc[:,'chemotaxis_index'] = df_cell.loc[:,'chemotaxis_index'].replace(d_mcds['substrate']['ds_substrate'])

        # store
        df_cell = df_cell.loc[:,sorted(df_cell.columns)]
        df_cell.sort_values('ID', axis=0, inplace=True)
        df_cell.set_index('ID', inplace=True)
        d_mcds['cell']['df_cell'] = df_cell.copy()

        ## get cell attribute list
        d_mcds['cell']['ls_cellattr'] = sorted(set(d_mcds['cell']['df_cell'].columns).difference(es_coor_cell))


        ####################
        # handle unit data #
        ####################

        if self.verbose:
            print('working on unit data ...')

        # extract data
        ds_unit = {}

        # units for metadata parameters
        ds_unit.update({'time': d_mcds['metadata']['time_units']})
        ds_unit.update({'runtime': d_mcds['metadata']['runtime_units']})
        ds_unit.update({'spatial_unit': d_mcds['metadata']['spatial_unit']})

        # microenvironment
        if self.microenv:
            for s_substrate in d_mcds['substrate']['ls_substarte']:
                # unit from substrate parameters
                s_unit = d_mcds['raw_substrate'][s_substrate]['units']
                ds_unit.update({s_substrate: s_unit})

                # units from microenvironment parameters
                s_diffusion_key = f'{s_substrate}_diffusion_coefficient'
                s_diffusion_unit = d_mcds['raw_substrate'][s_substrate]['diffusion_coefficient']['units']
                ds_unit.update({s_diffusion_key: s_diffusion_unit})

                s_decay_key = f'{s_substrate}_decay_rate'
                s_decay_unit = d_mcds['raw_substrate'][s_substrate]['decay_rate']['units']
                ds_unit.update({s_decay_key: s_decay_unit})

        # units from cell parameters
        ds_unit.update(d_mcds['raw_cell']['units'])

        # output
        del ds_unit['ID']
        d_mcds['metadata']['ds_unit'] = ds_unit


        #####################
        # handle graph data #
        #####################

        d_mcds['cell']['dei_graph'] = {}
        d_mcds['cell']['dei_graph'].update({'neighbor_cells': {}})
        d_mcds['cell']['dei_graph'].update({'attached_cells': {}})
        d_mcds['cell']['dei_graph'].update({'spring_attached_cells': {}})

        if self.graph:
            if self.verbose:
                print('working on graph data ...')

            # neighborhood cell graph
            s_cellpathfile = self.path + '/' + x_cell.find('neighbor_graph').find('filename').text
            dei_graph = graphfile_parser(s_pathfile=s_cellpathfile)
            if self.verbose:
                print(f'reading: {s_cellpathfile}')

            # store data
            d_mcds['cell']['dei_graph'].update({'neighbor_cells': dei_graph})

            # attached cell graph
            s_cellpathfile = self.path + '/' + x_cell.find('attached_cells_graph').find('filename').text
            dei_graph = graphfile_parser(s_pathfile=s_cellpathfile)
            if self.verbose:
                print(f'reading: {s_cellpathfile}')

            # store data
            d_mcds['cell']['dei_graph'].update({'attached_cells': dei_graph})

            # spring attached cell graph
            try:
                s_cellpathfile = self.path + '/' + x_cell.find('spring_attached_cells_graph').find('filename').text
                dei_graph = graphfile_parser(s_pathfile=s_cellpathfile)
                if self.verbose:
                    print(f'reading: {s_cellpathfile}')

                # store data
                d_mcds['cell']['dei_graph'].update({'spring_attached_cells': dei_graph})
            except AttributeError:
                pass


        ##########
        # output #
        ##########

        if self.verbose:
            print('done!')
        return d_mcds
