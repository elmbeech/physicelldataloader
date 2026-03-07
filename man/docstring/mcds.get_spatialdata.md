# mcds.get_spatialdata()


## input:
```
            images: set of string; default {'subs'}
                specify if from the subs or cell dataset
                a multichannel image should be generate.
                so far, only the subs image element is implemented.

            labels: set of strings; default is an empty set
                specify if from the subs or cell dataset
                a label element should be generated.
                so far, neither subs nor cell label elements are implemented.

            points: set of string; default {'subs'}
                specify if from the subs or cell dataset
                a points element should be generated.
                both, subs and cell point elements, are implemented.

            shapes: set of string; default {'cell'}
                specify if from the subs or cell dataset
                a shape element should be generated.
                so far, only the cell shape element is implemented.

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
                don't worry: essential columns like ID, coordinates
                and time will always be kept.

            scale: string; default 'maxabs'
                specify how the data should be scaled.
                possible values are None, maxabs, minmax, std.
                for more input, check out: help(pcdl.scaler)

```

## output:
```
            self.l_sdmcds: list of spatialdata objects.

```

## description:
```
            function to transform a mcds time step into
            a spatialdata object for downstream analysis.
        
```