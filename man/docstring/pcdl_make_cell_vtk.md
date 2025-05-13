```
usage: pcdl_make_cell_vtk [-h] [--custom_data_type [CUSTOM_DATA_TYPE ...]]
                          [--microenv MICROENV] [--physiboss PHYSIBOSS]
                          [--settingxml SETTINGXML] [-v VERBOSE]
                          [path] [attribute ...]

function that generates 3D glyph vtk file for cells. cells can have specified
attributes like cell_type, pressure, dead, etc. you can post-process this file
in other software like paraview (https://www.paraview.org/).

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .
  attribute             listing of mcds.get_cell_df dataframe column names,
                        used for cell attributes. default is a single term:
                        cell_type.

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
                        loaded into the df_cell dataframe? default is True.
  --settingxml SETTINGXML
                        the settings.xml that is loaded, from which the cell
                        type ID label mapping, is extracted, if this
                        information is not found in the output xml file. set
                        to None or False if the xml file is missing! default
                        is PhysiCell_settings.xml.
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to False for less text output, while
                        processing. default is True.

homepage: https://github.com/elmbeech/physicelldataloader
```
