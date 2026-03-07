```
usage: pcdl_get_cell_df [-h] [--microenv MICROENV] [--physiboss PHYSIBOSS]
                        [--settingxml SETTINGXML] [-v VERBOSE]
                        [--drop [DROP ...]] [--keep [KEEP ...]]
                        [--collapse COLLAPSE]
                        [path] [values]

this function extracts dataframes with a cell centric view of the simulation
and saves them as csv files.

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .
  values                minimal number of values a variable has to have in any
                        of the mcds time steps to be outputted. variables that
                        have only 1 state carry no information. None is a
                        state too. default is 1.

options:
  -h, --help            show this help message and exit
  --microenv MICROENV   should the microenvironment data be loaded? setting
                        microenv to False will use less memory and speed up
                        processing. default is True.
  --physiboss PHYSIBOSS
                        if found, should physiboss state data be extracted and
                        loaded into the df_cell dataframe? default is True.
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
  --collapse COLLAPSE   should all mcds time steps from the time series be
                        collapsed into one big csv, or a many csv, one csv for
                        each time step?, default is True.

homepage: https://github.com/elmbeech/physicelldataloader
```
