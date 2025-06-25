# PhysiCell Data Loader How To Manual

Below you will find information about how to install, load, update, uninstall, and troubleshooting pcdl.


## How to install pcdl?

```bash
pip3 install pcdl
```


## How to load the pcdl library?

```python3
import pcdl
```


## How to check for the current installed pcdl version?

```python3
import pcdl
pcdl.__version__
```


## How to update to the latest pcdl version?

```bash
pip3 install -U pcdl
```


## How to uninstall pcdl?

Note: For the pcdl library, this is a two-step procedure.
First, possibly installed test data and tutorial output will be removed.
Then, the software will be uninstalled.\
Keep in mind that pcdl library dependencies (like anndata, matplotlib, numpy, pandas, and scipy) will never be uninstalled automatically.

```bash
python3 -c "import pcdl; pcdl.uninstall_data()"
pip3 uninstall pcdl
```


## How to test if the command line interface pcdl functions work?

Execute the following command on the command line.\
Note: depending on your operating system and command line shell, tab completion might or might not work.
```bash
pcdl_get_version path/to/PhysiCell/output
```
If you get an error like: `pcdl_get_version: command not found`, please, follow the troubleshooting guide below.


## How to troubleshoot the command line interface pcdl functions?

Run the following commands:
```bash
pip3 install pip -U --force-reinstall
pip3 install pcdl --verbose -U --force-reinstall
```

### Windows:

Somewhere towards the bottom of the output, there should be a warning:
```bash
Installing collected packages: pcdl
  WARNING: The scripts pcdl_*.exe, pcdl_*.exe, pcdl_*.exe are installed in 'C:\path\to\Python\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```
Please follow these instructions to add the mentioned path to the PATH variable.
+ https://www.computerhope.com/issues/ch000549.htm

### Apple:

Somewhere towards the bottom of the output, there should be a warning:
```bash
Installing collected packages: pcdl
  WARNING: The scripts pcdl_*, pcdl_*, pcdl_* are installed in 'path/to/python/scripts/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```
To add the mentioned path to the PATH variable, use a plain text editor to
edit `~/.bash_profile` (bash is the default shell in MacOS > 9 and < 10.15 )
or `~/.zprofile` or `~/.zshenv` (zsh is the default shell in MacOS >= 10.15).

For example, this can be achieved with the following line:
```bash
PATH="path/to/python/scripts/bin:$PATH"
```
Then, depending on what file you have edited, reload:
```bash
source ~/.bash_profile
or
source ~/.zprofile
or
source ~/.zshenv
```

### Linux:

Somewhere towards the bottom of the output, there should be a warning:
```bash
Installing collected packages: pcdl
  WARNING: The scripts pcdl_*, pcdl_*, pcdl_* are installed in 'path/to/python/scripts/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```
To add the mentioned path to the PATH variable, use your favorite text editor to
edit your `~/.profile` or `~/.bash_profile` (depending on your distro and how you run linux).

For example, this can be achieved with the following line:
```bash
PATH="path/to/python/scripts/bin:$PATH"
```
Then, depending on what file you have edited, reload:
```bash
source ~/.profile
or
source ~/.bash_profile
```


## How to load data with pyMCDS.py like in the early days?

In the very early days, PhysiCell output was with the help of a MATLAB script loaded into MATLAB for analysis.

In 2019, a similar loader script was written for phython3.
The name of this script file, defining the pyMCDS class, was pyMCDS.py.
This pyMCDS.py script is in branch version 1, 2 and 3 still the core of the pcdl library.

To load data the old school way:

1. Copy the latest branch 3 [pyMCDS.py](https://raw.githubusercontent.com/elmbeech/physicelldataloader/v3/pcdl/pyMCDS.py) file into the PhysiCell or PhysiCell/output folder.
2. In the same directory, fire up a python3 shell (core [python](https://docs.python.org/3/tutorial/interpreter.html#interactive-mode), [ipython](https://en.wikipedia.org/wiki/IPython), or a [jupyter](https://en.wikipedia.org/wiki/Project_Jupyter) notebook that is running an ipython kernel).
3. Load the pyMCDS class as follows:

```python3
from pyMCDS import pyMCDS
```

Now you're rolling!

pyMCDS.py and the pyMCDS class is very lightweight.
Besides the python3 core library, this code has only matplotlib, numpy, pandas, scipy, and vtk library dependencies.\
The pyMCDS class evolved into the pcdl.TimeStep class, which has additionally anndata dependency, which makes the library slightly heavier but much more powerful for downstream data analysis.
Apart from that, pcdl offers the pcdl.TimeSeries class to handle the mcds snapshots from an entire PhysiCell run, and a set of functions that can be run straight from the command line, without even having to fire up a python3 shell.
Finally, branch version 4 broke with this ancient library structure because it is just out of time to run the code like this.\
Stay assured, if you like pyMCDS.py, it is there to last.
We will keep on maintaining pyMCDS.py from branch version 3.
