```
usage: pcdl_get_cell_attribute [-h]
                               [--custom_data_type [CUSTOM_DATA_TYPE ...]]
                               [--microenv MICROENV] [--physiboss PHYSIBOSS]
                               [--settingxml SETTINGXML] [-v VERBOSE]
                               [--drop [DROP ...]] [--keep [KEEP ...]]
                               [--allvalues ALLVALUES]
                               [path] [values]

function to detect informative variables in a time series. this function
detects even variables which have less than the minimal state count in each
time step, but different values from time step to time step. the output is a
json file with an entry of all non-coordinate column names that at least in
one of the time steps or in between time steps, reach the given minimal value
count. key is the column name, mapped is a list of all values (bool, str, and,
if allvalues is True, int and float) or a list with minimum and maximum values
(int, float).

positional arguments:
  path                  path to the PhysiCell output directory. default is . .
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
  --microenv MICROENV   should the microenvironment data be loaded? setting
                        microenv to False will use less memory and speed up
                        processing. default is True.
  --physiboss PHYSIBOSS
                        if found, should physiboss state data be extracted and
                        loaded into df_cell dataframe? default is True.
  --settingxml SETTINGXML
                        the settings.xml that is loaded, from which the cell
                        type ID label mapping, is extracted, if this
                        information is not found in the output xml file. set
                        to None or False if the xml file is missing! default
                        is False.
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
  --allvalues ALLVALUES
                        for numeric data, should only the min and max values
                        or all values be returned? default is false.

homepage: https://github.com/elmbeech/physicelldataloader
```
