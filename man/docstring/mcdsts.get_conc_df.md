# mcdsts.get_conc_df()


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
            df_conc or ldf_conc: pandas dataframe or list of dataframe
                dataframe stores all substrate concentrations in each voxel.

```

## description:
```
            function returns for the whole time series in one or many dataframes
            with concentration values for all chemical species in all voxels.
            additionally, this dataframe lists voxel and mesh center coordinates.
        
```