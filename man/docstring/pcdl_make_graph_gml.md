```
usage: pcdl_make_graph_gml [-h] [--custom_type [CUSTOM_TYPE ...]]
                           [--microenv MICROENV] [--settingxml SETTINGXML]
                           [-v VERBOSE] [--edge_attr EDGE_ATTR]
                           [--node_attr [NODE_ATTR ...]]
                           [path] [graph_type]

function to generate graph files in the gml graph modelling language standard
format. gml was the outcome of an initiative that started at the international
symposium on graph drawing 1995 in Passau and ended at Graph Drawing 1996 in
Berkeley. the networkx python and igraph C and python libraries for graph
analysis are gml compatible and can as such read and write this file format.

positional arguments:
  path                  path to the PhysiCell output directory or a
                        outputnnnnnnnn.xml file. default is . .
  graph_type            to specify which physicell output data should be
                        processed. attached: processes
                        mcds.get_attached_graph_dict dictionary. neighbor:
                        processes mcds.get_neighbor_graph_dict dictionary.
                        default is neighbor.

options:
  -h, --help            show this help message and exit
  --custom_type [CUSTOM_TYPE ...]
                        parameter to specify custom_data variable types other
                        than float (namely: int, bool, str) like this
                        var:dtype myint:int mybool:bool mystr:str . downstream
                        float and int will be handled as numeric, bool as
                        Boolean, and str as categorical data. default is an
                        empty string.
  --microenv MICROENV   should the microenvironment be extracted? setting
                        microenv to False will use less memory and speed up
                        processing, similar to the original pyMCDS_cells.py
                        script. default is True.
  --settingxml SETTINGXML
                        from which settings.xml should the cell type ID label
                        mapping be extracted? set to None or False if the xml
                        file is missing! default is PhysiCell_settings.xml.
  -v VERBOSE, --verbose VERBOSE
                        setting verbose to False for less text output, while
                        processing. default is True.
  --edge_attr EDGE_ATTR
                        specifies if the spatial Euclidean distance is used
                        for edge attribute, to generate a weighted graph.
                        default is True.
  --node_attr [NODE_ATTR ...]
                        listing of mcds.get_cell_df dataframe columns, used
                        for node attributes. default is and empty list.

homepage: https://github.com/elmbeech/physicelldataloader
```
