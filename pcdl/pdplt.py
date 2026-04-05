####
# title: biotransistor.pdplt.py
#
# language: python3
# date: 2019-06-29
# license: GPL>=v3
# author: Elmar Bucher
#
# description:
#    library with the missing pandas plot features.
#    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html
####


# library
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
import matplotlib.patches as mpatches
import numpy as np
import random
import sys

# pandas to matplotlib
#fig, ax = plt.subplots()
#ax = ax.ravel()
#ax.axis('equal')
#df.plot(ax=ax)
#plt.tight_layout()
#fig.savefig(s_filename, facecolor='white')
#plt.close()


# plot stuff
def df_label_to_color(df_abc=None, s_focus=None, ls_label=None, s_nolabel='silver', s_cmap='viridis', b_shuffle=False):
    '''
    input:
        df_abc: dataframe to which the color column will be added.
        s_focus: column name with sample labels for which a color column
            will be generated.
        ls_label: ordered list of labels to color. if None,
            ls_label will be extracted for the s_focus column.
        s_nolabel: color for labels not defined in ls_label.
        s_cmap:  matplotlib color map label.
            https://matplotlib.org/stable/tutorials/colors/colormaps.html
        b_shuffle: should colors be given by alphabetical order,
            or should the label color mapping order be random.

    output:
        df_abc: dataframe updated with color column.
        ds_color: lable to hex color string mapping dictionary

    description:
        function adds for the selected label column
        a color column to the df_abc dataframe.
    '''
    # map labels to color
    if (ls_label is None):
        ls_label = sorted(set(df_abc.loc[:,s_focus]))
    if b_shuffle:
       random.shuffle(ls_label)
    as_color = np.apply_along_axis(
        colors.to_hex,
        axis=1,
        arr=plt.get_cmap(s_cmap)(np.linspace(0, 1, len(ls_label))),
    )
    ds_color = dict(zip(ls_label, as_color))
    # process no data frame
    if (df_abc is None) and (s_focus is None):
        pass
    # process data frame
    elif (not (df_abc is None)) and (not (s_focus is None)):
        df_abc[f'{s_focus}_color'] = s_nolabel
        for s_category, s_color in ds_color.items():
            df_abc.loc[(df_abc.loc[:,s_focus] == s_category), f'{s_focus}_color'] = s_color
    # error handling
    else:
        sys.exit('Error @ both, df_abc and s_focus, have either to be None or not None!')
    # output
    return(ds_color)


def ax_colorlegend(ax, ds_color, ls_label=None, s_loc='lower left', s_fontsize='small'):
    '''
    input:
        ax: matplotlib axis object to which a color legend will be added.
        ds_color: lables to color strings mapping dictionary
        ls_label: ordered list of labels to color. if None, ls_label
            will be extracted from ds_color and sortred alphabetically.
        s_loc: the location of the legend.
            possible strings are: best,
            upper right, upper center, upper left, center left,
            lower left, lower center, lower right, center right,
            center.
        s_fontsize: font size used for the legend. known are:
            xx-small, x-small, small, medium, large, x-large, xx-large.

    output:
        ax: matplotlib axis object updated with color legend.

    description:
        function to add color legend to a figure.
    '''
    # manimupate input
    if (ls_label is None):
        ls_label = sorted(ds_color.keys())
    # processing
    lo_patch = []
    for s_label in ls_label:
        o_patch = mpatches.Patch(color=ds_color[s_label], label=s_label)
        lo_patch.append(o_patch)
    ax.legend(
        handles = lo_patch,
        loc = s_loc,
        fontsize = s_fontsize
    )


def ax_colorbar(ax, r_vmin, r_vmax, s_cmap='viridis', s_text=None, o_fontsize='medium', b_axis_erase=False):
    '''
    input:
        ax: matplotlib axis object to which a colorbar will be added.
        r_vmin: colorbar min value.
        r_vmax: colorbar max value.
        s_cmap: matplotlib color map label.
            https://matplotlib.org/stable/tutorials/colors/colormaps.html
        s_text: to label the colorbar axis.
        o_fontsize: font size used for the legend. known are:
            xx-small, x-small, small, medium, large, x-large, xx-large.
        b_axis_erase: should the axis ruler be erased?

    output:
        ax: matplotlib axis object updated with colorbar.

    description"
        function to add colorbar to a figure.
    '''
    if b_axis_erase:
        ax.axis('off')
    if not (s_text is None):
        ax.text(0.5,0.5, s_text, fontsize=o_fontsize)
    plt.colorbar(
        cm.ScalarMappable(
            norm=colors.Normalize(vmin=r_vmin, vmax=r_vmax, clip=False),
            cmap=s_cmap,
        ),
        ax=ax,
    )

