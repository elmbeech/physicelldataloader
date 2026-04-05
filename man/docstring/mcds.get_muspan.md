# mcds.get_muspan()


## input:
```
            z_slice: floating point number; default is None
                z-axis position to slice a 2D xy-plain out of the
                3D mesh. if None the whole 3D mesh will be returned.

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
                don't worry: essential columns like ID, coordinates
                and time will always be kept.

```

## output:
```
            do_domain:  dictionary of muspa domains, one for each z-layer.

```

## description:
```
            function returns a dictionary of muspa domains, containg a
            cell and subs collection with disrcete and continuous labels
            and all the graph as networks.
            + https://www.muspan.co.uk
            + https://docs.muspan.co.uk/latest/Documentation.html
        
```