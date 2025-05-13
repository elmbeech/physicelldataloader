# mcdsts.get_cell_df()


## input:
```
            self: TimeSeries class instance.

            values: integer; default is 1
                minimal number of values a variable has to have to be outputted.
                variables that have only 1 state carry no information.
                None is a state too.

            drop: set of strings; default is an empty set
                set of column labels to be dropped for the dataframe.
                don't worry: essential columns like ID, coordinates
                and time will never be dropped.
                Attention: when the keep parameter is given, then
                the drop parameter has to be an empty set!

            keep: set of strings; default is an empty set
                set of column labels to be kept in the dataframe.
                set values=1 to be sure that all variables are kept.
                don't worry: essential columns like ID, coordinates,
                time and runtime (wall time) will always be kept.

            collapse: boole; default True
                should all mcds time steps from the time series be collapsed
                into one pandas dataframe object, or a list of dataframe objects
                for each time step?

```

## output:
```
            df_cell or ldf_cell: pandas dataframe or list of dataframe
                dataframe stores one cell per row, all tracked variables
                values related to this cell. the variables are cell_position,
                mesh_center, and voxel coordinates, all cell_variables,
                all substrate rates and concentrations, and additional
                the surrounding cell density.

```

## description:
```
            function returns for the whole time series one or many dataframes
            with a cell centric view of the simulation.
        
```