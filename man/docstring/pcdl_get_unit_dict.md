```
usage: pcdl_get_unit_dict [-h] [--microenv MICROENV] [--settingxml SETTINGXML]
                          [-v VERBOSE]
                          [path]

function returns a csv that lists all tracked variables from metadata, cell,
and microenvironment and maps them to their unit.

positional arguments:
  path                  path to the PhysiCell output directory. default is . .

options:
  -h, --help            show this help message and exit
  --microenv MICROENV   should the microenvironment data be loaded? setting
                        microenv to False will use less memory and speed up
                        processing. default is True.
  --settingxml SETTINGXML
                        the settings.xml that is loaded, from which the cell
                        type ID label mapping, is extracted, if this
                        information is not found in the output xml file. set
                        to None or False if the xml file is missing! default
                        is False.
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to False for less text output, while
                        processing. default is True.

homepage: https://github.com/elmbeech/physicelldataloader
```
