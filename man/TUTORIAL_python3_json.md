# PhysiCell Data Loader Tutorial: pcdl and Python and the Json File Format

[Json](https://www.json.org/json-en.html) is a lightweight data exchange file format.

In pcdl output from the [TimeSeries](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_python3_timeseries.md) **mcdsts.get_conc_attribute()** and **mcdsts.get_cell_attribute()** can store, and output from the [pcdl command line command](https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL_commandline.md) **pcdl_get_conc_attribute** and **pcdl_get_cell_attribute** store into a json file.

The [json library](https://docs.python.org/3/library/json.html) is a part of core python.

Json is the ideal data format for unstructured data constructs that not can be stored in csv file format, like a dictionary of lists.
Please note, python objects are not per se json comaptible.
For example:
Python dictionary keys can be of almost any data type, but json object keys have to be strings.
Complex numbers are a standard data type in python, but complex numbers cannot be stored in json.


### Dump pcdl data construct from the command line into a json file

```bash
pcdl_get_conc_attribute output 2
```
```bash
pcdl_get_cell_attribute output 2
```

### Dump pcdl data construct from within python into a json file

```python
import json
import pcdl

mcdsts = pcdl.TimeSeries('output/')
dl_conc = mcdsts.get_conc_attribute(values=2)

fp = open('output/timeseries_conc_attribute_minmax.json', 'w')
json.dump(dl_conc, fp)
f.close()
```
```python
import json
import pcdl

mcdsts = pcdl.TimeSeries('output/')
dl_cell = mcdsts.get_cell_attribute(values=2)

fp = open('output/timeseries_cell_attribute_minmax.json', 'w')
json.dump(dl_cell, fp)
f.close()
```


### Load json files into python

```python
import json

dl_conc = json.load('output/timeseries_conc_attribute_minmax.json')
```
```python
import json

dl_cell = json.load('output/timeseries_cell_attribute_minmax.json')
```
The python object we retrieve from this pcdl conc attribute and cell attribute files is a dictionary of lists.


That's it. The rest is analysis!
