# PhysiCell Data Loader Tutorial: pcdl and Python and Matplotlib

[Matplotlib](https://matplotlib.org/) is the python's plotting backbone.
It is an old library, matplotlib is not always intuitive how to use, but there is no way around.

Pcdl's  **mcds.plot_contour** and **mcds.plot_scatter** plotting function
can take a matplotlib axis object as input
and, by default, generate a matplotlib figure object as output.

Data in [pandas]() dataframes,
and as such output from pcdl's **mcds.get_conc_df** and **mcds.get_cell_df** function,
can easily be plotted.


## Matplotlib and [ipython](https://en.wikipedia.org/wiki/IPython)

```bash
cd path/to/PhysiCell
ipython
```

This is the ipython magic command,
for if you run the code in a plain ipython shell,
to load a suitable backend for displaying matplotlib plots.

```python
%matplotlib
```


## Load a pcdl time step

```python
import pcdl

mcds = pcdl.TimeStep('output/output00000024.xml')
```


## Overlay pcdl scatter and contour plot


Generate the plot.

```python
# load libraries
import matplotlib.pyplot as plt

# generate canvas
fig, ax = plt.subplots(figsize=(10.24, 7.68))

# plot substrate
mcds.plot_contour('oxygen', cmap='Blues', ax=ax)

# plot cell agents
mcds.plot_scatter(cmap='turbo', ax=ax)

# fine-tuning
ax.axis('equal')  # this is essential, to overlay the coordinates properly!
fig.suptitle('cell agents and substrate')
plt.tight_layout()

# save to file
fig.savefig(f'my_plot.png', facecolor='white')
#plt.close()

# display on screen
fig.show()
```


## Overlay scatter and contour plot from all substrates

```python
# load libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# generate canvas
i_total = len(mcds.get_substrate_list())
i_x = int(np.ceil(np.sqrt(i_total)))
i_y = int(np.floor(np.sqrt(i_total)))
fig, axs = plt.subplots(nrows=i_y, ncols=i_x, figsize=(10.24, 7.68))

# line up ax objects
if (type(axs) == mpl.axes._axes.Axes):
    axs = [axs]
else:
    axs = axs.ravel()

# plotting
for i_substarte, s_substarte in enumerate(mcds.get_substrate_list()):
    mcds.plot_contour(s_substarte, cmap='Oranges', ax=axs[i_substarte])
    mcds.plot_scatter(ax=axs[i_substarte])
    axs[i_substarte].axis('equal')

# fine-tuning
fig.suptitle('cell agents and substrates')
plt.tight_layout()

# save to file
fig.savefig(my_plot.png, facecolor='white')
#plt.close()

# display on screen
fig.show()
```


## Plotting data from conc and cell dataframes

Since microenvironment data and cell data can be retrieved as pandas datafarme,
basic plotting (line plot, bar plot, histogram, boxplot, kernel density estimation plot, area plot, pie plot, scatter plot, hexbin plot)
can easily be generated with the **pandas plot function**.

Load dataframes

```python
df_conc = mcds.get_conc_df()
df_cell = mcds.get_cell_df()
```


### Categorical data

Generate a dataframe with some categorical data

```pandas
df_cat = df_cell.loc[:, ['cell_type', 'cycle_model', 'current_phase', 'dead']]
df_cat['count'] = 1
df_catplot = df_cat.loc[:, ['cell_type','count']].groupby('cell_type').count()
df_catplot.info()
```

Bar plot (categorical data)

```python
df_catplot.plot(kind='bar')
```
```python
df_catplot.plot(kind='barh')
```


Pie plot (categorical data)

```python
df_catplot.plot(
    kind = 'pie',
    y = 'count',
    ylabel = '',
    legend = False,
    title = 'cell_type'
)
```


### Numerical data

Histogram count plot (numerical data)

```python
df_cell.loc[:, mcds.get_substrate_list()].plot(
    kind = 'hist',
    bins = 32,
    xlabel = 'Cell surrounding substrate concentration',
)
```

Histogram probability plot (numerical data)

```python
# import library
import numpy as np

# calculate a_weight
df_focus = df_cell.loc[:, mcds.get_substrate_list()]
a_ones = np.ones_like(df_focus.values)
a_weight = a_ones / df_focus.shape[0]

# plot
df_focus.plot(
    kind='hist',
    weights = a_weight,
    bins=32,
    xlabel = 'Cell surrounding substrate concentration',
)
```

Kde kernel density estimation plot (numerical data)

```python
df_cell.loc[:, mcds.get_substrate_list()].plot(
    kind = 'kde',
    xlabel = 'Cell surrounding substrate concentration'
)
```

Box plot (numerical data)

```python
df_conc.loc[:, mcds.get_substrate_list()].plot(kind='box')
```


### On x axis ordered 2D numerical data

Line plot (on x axis ordered 2D numerical data)

```python
df_focus = df_cell.loc[:, ['current_phase', 'elapsed_time_in_phase', 'surface_area']]
df_focus = df_focus.groupby(['current_phase', 'elapsed_time_in_phase']).mean().reset_index()
df_focus = df_focus.set_index(['current_phase','elapsed_time_in_phase']).unstack('current_phase').reset_index()

df_focus.plot(
    kind = 'line',
    x = 'elapsed_time_in_phase',
    y = [('surface_area','live'), ('surface_area', 'apoptotic')],
)
```

Area plot (on x axis ordered 2D numerical data)

```python
df_focus = df_cell.loc[:, ['current_phase', 'elapsed_time_in_phase', 'surface_area']]
df_focus = df_focus.groupby(['current_phase', 'elapsed_time_in_phase']).mean().reset_index()
df_focus = df_focus.set_index(['current_phase','elapsed_time_in_phase']).unstack('current_phase').reset_index()

df_focus.plot(
    kind = 'area',
    x = 'elapsed_time_in_phase',
    y = [('surface_area','live'), ('surface_area', 'apoptotic')],
)
```

This is like a continuous stacked bar plot.
Check it out!
Change the argument kind to *kind = 'bar'* and add the argument *stacked = True*.


### Unordered 2D or 3D numerical data

Scatter plot ~ the equivalent to mcds.plot\_scatter (unordered 2D or 3D numerical data)

```python
df_cell.plot(
    kind = 'scatter',
    x = 'position_x',
    y = 'position_y',
    c = 'oxygen',
)
```

Hexbin plot ~ the equivalent to mcds.plot\_contour (unordered 3D numerical data)

```python
df_conc.plot(
    kind = 'hexbin',
    x = 'mesh_center_m',
    y = 'mesh_center_n',
    C = 'oxygen',
    gridsize = 9,
    cmap = 'viridis',
)
```


### Further readings:

+ https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html

