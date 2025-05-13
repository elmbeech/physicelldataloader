# PhysiCell Data Loader Tutorial: pcdl Introduction

If you have not already done so, please install the latest version of physicelldataloader (pcdl),
as described in the [HowTo](https://github.com/elmbeech/physicelldataloader/blob/master/man/HOWTO.md) section.\
The current development happens in branch v3 and v4.
Branch v1 and v2 exists, if ever needed, for reproducibility of old results.


## Tutorial - branch v1 and v2
The original python-loader tutorial can be found here.
+ http://www.mathcancer.org/blog/python-loader/


## Tutorial - branch v3 and v4


### History

In the very early days, [PhysiCell](https://github.com/MathCancer/PhysiCell) output was with the help of a MATLAB script loaded into MATLAB for analysis.\
In 2019, a similar loader script was written for python3.
The name of this script filed was pyMCDS.py and basically defined one class named pyMCDS.

In autumn 2022 an endeavor was undertaken to pack the original pyMCDS.py script into a pip installable python3 library and develop it further, but always in such a way that, if necessary, the code could still be run like in the early days.\
The result is the pcdl physicelldataloader library branch v2, v3.
In spring 2025 the code was stripped of some relics from the early days, to make the code more python3 than C++ like, which resulted in branch v4.

The result from all of this is the pcdl physicelldataloader library here.\
In the big picture, the pyMCDS class evolved into the TimeStep class, which is slightly heavier but much more powerful for downstream data analysis than the original pyMCDS class.
Additionally, a TimeSeries class was added.

If you inspect branch v3 pcdl source code, you will see that the [pyMCDS.py](https://github.com/elmbeech/physicelldataloader/blob/v3/pcdl/pyMCDS.py) file still exists.
And if you feel so, it is still possible to [load and process PhysiCell output the ancient way](https://github.com/elmbeech/physicelldataloader/blob/master/man/HOWTO.md#how-to-run-physicelldataloader-like-in-the-early-days-before-autumn-2022)!\
Naturally, the full-fledged pcdl library with the TimeSteps and TimeSeries class is much more powerful than pyMCDS.py only.


### Concept

PhysiCell data loader is not yet another analysis software, it is just an interface to analysis software!
If you work through the tutorials, and you will in in-depth grasp the meaning behind this sentence.


### Understanding PhysiCell's Time Step Output: the MultiCellular Data Standard (MCDS) Format

MCDS Time Steps are the input for pcdl.

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
    file names for the files that contain microenvironment and cell data at this time step (mat and possibly graph.txt files).
+ **output00000012_cells.mat**: This is a MATLAB matrix file that contains tracked information about the individual cells in the model.
    It tells us things like the cells' position, volume, secretion, cell cycle status, and user-defined cell parameters.
+ **output00000012_microenvironment0.mat**: This is a MATLAB matrix file that contains data about the microenvironment at this time step.
+ **output00000012_attached_cells_graph.txt** and **output00000036_cell_neighbor_graph.txt**: These are files describing the cell neighborhood graph.

With pcdl we can load a **MCDS time step** or a whole **MCDS time series** for data analysis.
