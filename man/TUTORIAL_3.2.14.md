# PhysiCell Data Loader Tutorial

If you not have already done so, please install the latest version of physicelldataloader (pcdl),
as described in the [HowTo](https://github.com/elmbeech/physicelldataloader/blob/master/man/HOWTO.md) section.\
The current development happens in branch v3.
Branch v1 and v2 exists, if ever needed, for reproducibility of old results.


## Tutorial - branch v1 and v2
The original python-loader tutorial can be found here.
+ http://www.mathcancer.org/blog/python-loader/


## Tutorial - branch v3

### Understanding PhysiCell's Time Step Output: the MultiCellular Data Standard (MCDS) Format

Each time PhysiCell's internal time tracker passes a time step where data is to be saved, it generates a number of files of various types.\
Each of these files will have a number at the end that indicates where it belongs in the sequence of outputs.\
All files from the first round of output will end in 00000000.\*, and the second round will be 00000001.\*, and so on.\
If you have run a PhysiCell model, have a look at the PhysiCell/output folder.

Let's assume we captured data every simulation time hour, and we're interested in the set of output half a day through the run, the 13th set of output files.\
The files we care about most from this set consists of:

+ **output00000012.xml**: This file is the main organizer of the data.
    It contains an overview of the data stored in the MultiCellDS as well as some actual data, including:\
    metadata (MultiCellDS version, PhysiCell or BioFVM version, simulation time, runtime, and processing time stamp),\
    coordinates for the computational domain (mesh),\
    parameters for diffusing substrates in the microenvironment (continuum\_variables),\
    column labels and units for the cell data (cell\_population),\
    file names for the files that contain microenvironment and cell data at this time step (mat and possibly graph.txt files),
+ **output00000012_cells.mat**: This is a MATLAB matrix file that contains tracked information about the individual cells in the model.
    It tells us things like the cells' position, volume, secretion, cell cycle status, and user defined cell parameters.
+ **output00000012_microenvironment0.mat**: This is a MATLAB matrix file that contains data about the microenvironment at this time step.


### The History of the pcdl Library

In the very early days, PhysiCell output was with the help of a MATLAB script loaded into MATLAB for analysis.\
In 2019, a similar loader script was written for phython3.
The name of this script filed was pyMCDS.py basically defined one class named pyMCDS.

In autumn 2022 an endeavor was undertaken to pack the original pyMCDS.py script into a pip installable python3 library and develop it further, but always in such a way that, if necessary, the code could still be run like in the early days.\
The result is the pcdl physicelldataloader library here.\
The pyMCDS class evolved into the TimeStep class.
, which is slightly havyer but much more powerful for downstream data analysis.

If you inspect today's pcdl source code, you will see that the [pyMCDS.py](https://raw.githubusercontent.com/elmbeech/physicelldataloader/master/pcdl/pyMCDS.py) file still exists.
And if you feel so, it is still possible to [load PhysiCell output the ancient way](https://github.com/elmbeech/physicelldataloader/blob/master/man/HOWTO.md#how-to-run-physicelldataloader-like-in-the-early-days-before-autumn-2022)!


BUE: links to the separate tutorial sections.