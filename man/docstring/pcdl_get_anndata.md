```
usage: pcdl_get_anndata [-h] [--custom_data_type [CUSTOM_DATA_TYPE ...]]
                        [--microenv MICROENV] [--graph GRAPH]
                        [--physiboss PHYSIBOSS] [--settingxml SETTINGXML]
                        [-v VERBOSE] [--drop [DROP ...]] [--keep [KEEP ...]]
                        [--scale SCALE] [--collapse COLLAPSE]
                        [path] [values]

function to transform mcds time steps into one or many anndata objects for
downstream analysis.

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .
  values                minimal number of values a variable has to have in any
                        of the mcds time steps to be outputted. variables that
                        have only 1 state carry no information. None is a
                        state too. default is 1.

options:
  -h, --help            show this help message and exit
  --custom_data_type [CUSTOM_DATA_TYPE ...]
                        parameter to specify custom_data variable types other
                        than float (namely: int, bool, str) like this
                        var:dtype myint:int mybool:bool mystr:str . downstream
                        float and int will be handled as numeric, bool as
                        Boolean, and str as categorical data. default is an
                        empty string.
  --microenv MICROENV   should the microenvironment be extracted and loaded
                        into the anndata object? setting microenv to False
                        will use less memory and speed up processing. default
                        is True.
  --graph GRAPH         should neighbor graph, attach graph, and attached
                        spring graph be extracted and loaded into the anndata
                        object? default is True.
  --physiboss PHYSIBOSS
                        if found, should physiboss state data be extracted and
                        loaded into the anndata object? default is True.
  --settingxml SETTINGXML
                        the settings.xml that is loaded, from which the cell
                        type ID label mapping, is extracted, if this
                        information is not found in the output xml file. set
                        to None or False if the xml file is missing! default
                        is PhysiCell_settings.xml.
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to False for less text output, while
                        processing. default is True.
  --drop [DROP ...]     set of column labels to be dropped for the dataframe.
                        don't worry: essential columns like ID, coordinates
                        and time will never be dropped. Attention: when the
                        keep parameter is given, then the drop parameter has
                        to be an empty string! default is an empty string.
  --keep [KEEP ...]     set of column labels to be kept in the dataframe. set
                        values=1 to be sure that all variables are kept. don't
                        worry: essential columns like ID, coordinates and time
                        will always be kept. default is an empty string.
  --scale SCALE         specify how the data should be scaled. possible values
                        are None, maxabs, minmax, std. None: no scaling. set
                        scale to None if you would like to have raw data or
                        entirely scale, transform, and normalize the data
                        later. maxabs: maximum absolute value distance scaler
                        will linearly map all values into a [-1, 1] interval.
                        if the original data has no negative values, the
                        result will be the same as with the minmax scaler
                        (except with attributes with only one value). if the
                        attribute has only zeros, the value will be set to 0.
                        minmax: minimum maximum distance scaler will map all
                        values linearly into a [0, 1] interval. if the
                        attribute has only one value, the value will be set to
                        0. std: standard deviation scaler will result in
                        sigmas. each attribute will be mean centered around 0.
                        ddof delta degree of freedom is set to 1 because it is
                        assumed that the values are samples out of the
                        population and not the entire population. it is
                        incomprehensible to me that the equivalent sklearn
                        method has ddof set to 0. if the attribute has only
                        one value, the value will be set to 0. default is
                        maxabs
  --collapse COLLAPSE   should all mcds time steps from the time series be
                        collapsed into one big anndata h5ad file, or a many
                        h5ad, one h5ad for each time step?, default is True.

homepage: https://github.com/elmbeech/physicelldataloader
```
