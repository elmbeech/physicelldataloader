# PhysiCell Data Loader Tutorial: pcdl and Python and MuSpAn

[MuSpAn](https://www.muspan.co.uk/) is a multiscale spatial analysis toolbox for analyzing spatial transcriptomics data, multiplex immunohistochemistry data, imaging mass cytometry data, and more.
It uses cutting-edge mathematical and statistical approaches to data analysis to provide the most comprehensive spatial analysis available and is being continually expanded, with a team of quantitative researchers constantly developing new methodology to tackle multiscale spatial analysis problems.

Pcdl offers a time step and time series get\_muspan function to translate cell and substrate data into a dictionary of muspan domain objects, one domain per time step z-layer.

Additionally, pcdl provides a pcdl\_get\_muspan command line command to translate PhysiCell output into muspan domain files.

For installation and learning how to use muspan, please follow the official documentation.

+ https://www.muspan.co.uk/
+ https://docs.muspan.co.uk/latest/Documentation.html
+ https://github.com/joshwillmoore1/MuSpAn-Public

## Translate mcds time step and time series into muspan domains.

```python
import pcdl
import muspan as ms

mcdsts = pcdl.TimeSeries('output/')
do_domain = mcdsts.get_muspan()  # translate the mcds time seris into a dictionary of muspan domain objects.
ls_domain =  sorted(do_domain.keys())  # generate an orderes list of domain names

print(ls_domain)   # print a list of domain names
print(do_domain[ls_domain[0]])  # take a look at the first domain in the ls_domain list.
```

That's it. The rest is analysis!
