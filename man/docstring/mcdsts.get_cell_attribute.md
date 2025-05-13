# mcdsts.get_cell_attribute()


## input:
```
            self: TimeSeries class instance.

            values: integer; default is 1
                minimal number of values a variable has to have
                in any of the mcds time steps to be outputted.
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
                don't worry: essential columns like ID, coordinates
                and time will always be kept.

            allvalues: boolean; default is False
                for numeric data, should only the min and max values or
                all values be returned?

```

## output:
```
            dl_variable: dictionary of list
                dictionary with an entry of all non-coordinate column names
                that at least in one of the time steps or in between
                time steps, reach the given minimal value count.
                key is the column name, mapped is a list of all values
                (bool, str, and, if allvalues is True, int and float) or
                a list with minimum and maximum values (int, float).

```

## description:
```
            function to detect informative variables in a time series.
            this function detects even variables which have less than the
            minimal state count in each time step, but different values
            from time step to time step.
        
```