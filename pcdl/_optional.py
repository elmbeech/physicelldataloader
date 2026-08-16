#########
# title: _optional.py
#
# language: python3
# date: 2026-08-14
# license: BSD-3-Clause
# author: Elmar Bucher
#
# description:
#     pcdl, by default, only installs lightweight core dependencies
#     (matplotlib, numpy, pandas, scipy), enough to load PhysiCell
#     output into pandas dataframes, and to render basic contour and
#     scatter plots.
#     a handful of heavyweight, specialized libraries (anndata, bioio,
#     bioio-ome-tiff, geopandas, neuroglancer, requests, scikit-image,
#     shapely, spatialdata, vtk) are only needed by specific functions
#     (e.g. get_anndata, get_spatialdata, make_ome_tiff, make_conc_vtk,
#     make_cell_vtk, render_neuroglancer, install_data).
#     optional_import loads such a library only the moment a function
#     that actually needs it is called (lazy import), and raises a
#     clear, actionable error message in case the library is missing.
#########


import importlib


def optional_import(s_module, s_attr=None, s_pip=None, s_caller=None):
    """
    input:
        s_module: string
            dotted module path to import, e.g. 'anndata' or 'bioio.writers'.

        s_attr: string; default None
            if given, the attribute to fetch out of the imported module
            (equivalent to "from s_module import s_attr").

        s_pip: string; default None
            pip install name for the module, if this differs from s_module
            (e.g. s_module='skimage' but s_pip='scikit-image').
            if None, the first dot-separated part of s_module is used.

        s_caller: string; default None
            name of the calling pcdl function, to mention in the error message.

    output:
        the imported module, or, if s_attr is given, the requested attribute
        of the imported module.

    description:
        helper function to lazily load an optional, heavyweight pcdl
        dependency, only the moment a function that actually needs it
        is called. if the library is not installed, a ModuleNotFoundError
        with an actionable error message is raised, pointing the user to
        `pip install pcdl[full]` or to install the missing library manually.
    """
    s_pip = s_module.split('.')[0] if (s_pip is None) else s_pip
    try:
        o_module = importlib.import_module(s_module)
    except ImportError as e:
        s_fct = f' {s_caller}' if not (s_caller is None) else ''
        raise ModuleNotFoundError(
            f"Error{s_fct} : this functionality requires the optional dependency '{s_pip}', which is not installed.\n" +
            f"pcdl was installed light weight (default), without this and other heavyweight, specialized libraries.\n" +
            f"to fix this, either:\n" +
            f"+ install pcdl with all optional dependencies: pip install pcdl[full]\n" +
            f"+ or install only the missing library manually: pip install {s_pip}\n"
        ) from e
    return o_module if (s_attr is None) else getattr(o_module, s_attr)
