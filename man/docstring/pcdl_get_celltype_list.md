```
usage: pcdl_get_celltype_list [-h] [--settingxml SETTINGXML] [-v VERBOSE]
                              [path]

this function is returns a list with all celltype labels ordered by celltype
ID.

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .

options:
  -h, --help            show this help message and exit
  --settingxml SETTINGXML
                        the settings.xml that is loaded, from which the cell
                        type ID label mapping, is extracted, if this
                        information is not found in the output xml file. set
                        to None or False if the xml file is missing! default
                        is False.
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to True for more text output, while
                        processing. default is False.

homepage: https://github.com/elmbeech/physicelldataloader
```
