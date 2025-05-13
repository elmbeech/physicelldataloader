# mcdsts.get_mcds_list()


## input:
```
            self: TimeSeries class instance.

```

## output:
```
            self.l_mcds: list of chronologically ordered mcds objects.
                watch out, this is a pointer to the
                self.l_mcds list of mcds objects, not a copy of self.l_mcds!

```

## description:
```
            function returns a pointer to the self.l_mcds list of mcds objects.
        
```