# mcdsts = pcdl.TimeSeries('path/to/output')


## input:
```
            output_path: string, default '.'
                relative or absolute path to the directory where
                the PhysiCell output files are stored.

            custom_data_type: dictionary; default is {}
                variable to specify custom_data variable types
                other than float (int, bool, str) like this: {var: dtype, ...}.
                downstream float and int will be handled as numeric,
                bool as Boolean, and str as categorical data.

            load: boole; default True
                should the whole time series data, all time steps, straight at
                object initialization be read and stored to mcdsts.l_mcds?

            microenv: boole; default True
                should the microenvironment data be loaded?
                setting microenv to False will use less memory and speed up processing.

            graph: boole; default True
                should the graphs, like cell_neighbor_graph.txt, be loaded?
                setting graph to False will use less memory and speed up processing.

            physiboss: boole; default True
                should physiboss state data be loaded, if found?
                setting physiboss to False will use less memory and speed up processing.

            settingxml: string; default PhysiCell_settings.xml
                the settings.xml that is loaded, from which the cell type ID
                label mapping, is extracted, if this information is not found
                in the output xml file.
                set to None or False if the xml file is missing!

            verbose: boole; default True
                setting verbose to False for less text output, while processing.

```

## output:
```
            mcdsts: TimeSeries class instance
                this instance offers functions to process all stored time steps
                from a simulation.

```

## description:
```
            TimeSeries.__init__ generates a class instance the instance offers
            functions to process all time steps in the output_path directory.
        
```