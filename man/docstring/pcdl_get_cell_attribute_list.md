```
usage: pcdl_get_cell_attribute_list [-h] [--microenv MICROENV]
                                    [--physiboss PHYSIBOSS]
                                    [--settingxml SETTINGXML] [-v VERBOSE]
                                    [path]

this function is returns a list with all cell attribute labels, alphabetically
ordered.

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .

options:
  -h, --help            show this help message and exit
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
                        is PhysiCell_settings.xml.
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to True for more text output, while
                        processing. default is False.

homepage: https://github.com/elmbeech/physicelldataloader
```
