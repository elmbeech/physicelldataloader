# mcds.custom_data_astype()


## input:
```
            custom_data_type: dictionary; default is {}
                variable to specify custom_data variable types other than
                floats (namely: int, bool, str) like this: {var: dtype, ...}.
                downstream float and int will be handled as numeric,
                bool as Boolean, and str as categorical data.

```

## output:
```
            self.data['cell']['df_cell']:
                the dtype of columns as specified in the custom_data_type dictionary.

```

## description:
```
            function to set the dtype of custom_data variables,
            even after the data is loaded.
        
```