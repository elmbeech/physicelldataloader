#########
# title: ometiff2neuro.py
#
# language: python3
# date: 2022-02-16
# license: MIT
# author: jason lu, viviana kwong, elmar bucher
#
# installation:
#     pip install neuroglancer   # the basics
#     pip install ipython   # for coding
#     pip install matplotlib   # for expression value color maps
#     pip install numpy   # for basic code manipulation
#     pip install scikit-image   # signal thresh and image manipulation.
#     pip install bioio bioio-ome-tiff   # for loading the image and extracting ometiff metadata
#
# run:
#     python3 -i neuromancer.py <path/filename.ome.tiff>
#
# description:
#   script to render multi channel multi slice ome.tiff files into the
#   neuroglancer software.
#
#   the script here makes use of the neuroglancer python library and is based
#   on the neuroglancer/python/examples/example.py code.
#   with this script, it is possible to load three-dimensional single
#   time step ome-tiff files straight into the neuroglancer software.
#   for each channel, mesh generation, rendering, and expression intensity
#   coloring is done on the fly.
#   channels can be viewed together or alone by toggling them on or off in
#   the neuroglancer user interface.
#
# references:
#   + https://www.openmicroscopy.org/ome-files/
#   + https://github.com/google/neuroglancer
#   + https://github.com/google/neuroglancer/tree/master/python
#########


# library
import argparse
from bioio import BioImage
import matplotlib as mpl
import neuroglancer
import neuroglancer.cli
import numpy as np
from skimage import exposure, util
import sys


# functions
def ometiff2neuro(
        o_state,
        s_pathfile_tiff,
        i_timestep = 0,
        s_intensity_cmap = 'gray',  # None
    ):
    '''
    input:
        o_state: neuroglancer viewer state object.

        s_pathfile_tiff: file name and path to input tiff file.

        s_intensity_cmap: matlab color map object, used to display expression intensity values.
            default is cm.gray.
            if None, no intensity layers will be generated.

    output:
        local url where the rendered data can be viewed.

    description:
        function to render multi channel multi slice (ome)tiff files into the neuroglancer software.
    '''
    # off we go #
    print(f'\nprocessing: {s_pathfile_tiff}')

    # load tiff image as numpy array
    o_img =  BioImage(s_pathfile_tiff)

    # check dimensionality
    if (o_img.dims.order.lower() != 'tczyx'):
        sys.exit(f'Error @ ometiff2neuro : cannot handle ome tiff file with dimension {o_img.dims.order.lower()}')

    # generate neuroglancer layers
    for i_channel in range(o_img.shape[1]):

        # extract channel label
        s_label = o_img.channel_names[i_channel]
        print(f'check channel {i_channel}/{o_img.shape[1]}: {s_label}')

        # extract data
        a_channel = o_img.data[i_timestep, i_channel, :, :, :]

        # 3D rendering #
        # thresh data
        # shape
        a_shape = np.zeros(a_channel.shape, dtype=np.uint32)
        a_shape[a_channel > 0] = i_channel + 1

        # generate neuroglancer object
        ls_name = ['z', 'y', 'x']
        li_scale = [
            o_img.physical_pixel_sizes.Z,
            o_img.physical_pixel_sizes.Y,
            o_img.physical_pixel_sizes.X,
        ]

        o_state.layers.append(
            name = s_label,
            layer = neuroglancer.LocalVolume(
                data = a_shape,
                dimensions = neuroglancer.CoordinateSpace(
                    # rgb, x, y, z
                    names = ls_name,
                    scales = li_scale,
                    units = ['nm', 'nm', 'nm'],
                ),
            ),
            visible = False,  # special thanks to Jeremy Maitin-Shepard.
        )

        # expression intensity rendering #
        if not (s_intensity_cmap is None):
            a_channel = exposure.rescale_intensity(a_channel, in_range='image')  # 16 or 8[bit] normalized

            # translate intensity by color map
            a_8bit = util.img_as_ubyte(a_channel)
            a_intensity =  mpl.colormaps[s_intensity_cmap](a_8bit, alpha=None, bytes=True)[:,:,:,0:3]

            # generate neuroglancer object
            ls_name = ['z', 'y', 'x','c^']
            li_scale = [
                o_img.physical_pixel_sizes.Z,
                o_img.physical_pixel_sizes.Y,
                o_img.physical_pixel_sizes.X,
                3
            ]

            o_state.layers.append(
                name = s_label + '_intensity',
                layer = neuroglancer.LocalVolume(
                    data = a_intensity,
                    dimensions = neuroglancer.CoordinateSpace(
                        # rgb, x, y, z
                        names = ls_name,
                        scales = li_scale,
                        units = ['nm', 'nm', 'nm', ''],
                    ),
                ),
                visible = False,  # special thanks to Jeremy Maitin-Shepard.
                shader=
"""
void main() {
  emitRGB(
    vec3(toNormalized(getDataValue(0)),
    toNormalized(getDataValue(1)),
    toNormalized(getDataValue(2)))
  );
}
""",
            )


# run the code from the command line
if __name__ == '__main__':
    import neuroglancer
    o_parser = argparse.ArgumentParser(
        description='script to render an ome.tiff file into the neuroglancer software.',
        epilog = 'homepage: https://github.com/elmbeech/physicelldataloader',
    )

    # request path to ometiff and file name as command line argument
    o_parser.add_argument(
        'ometiff',
        type=str,
        nargs=1,
        help='ome.tiff path/filename'
    )
    # time step
    o_parser.add_argument(
        '--timestep',
        default = 0,
        type = int,
        help = 'time step, within a possibly collapsed ome tiff file, to render. the default will work with single time step ome tiff files.',
    )
    # intensity colormap
    o_parser.add_argument(
        '--intensity_cmap',
        default = 'gray',
        help = 'matlab color map label, used to display expression intensity values. if None, no intensity layers will be generated. https://matplotlib.org/stable/users/explain/colors/colormaps.html',
    )

    # start neuroglancer
    neuroglancer.cli.add_server_arguments(o_parser)
    neuroglancer.cli.handle_server_arguments(o_parser.parse_args())
    viewer = neuroglancer.Viewer()
    with viewer.txn() as state:
        # render ometiff
        ometiff2neuro(
            o_state = state,
            s_pathfile_tiff = o_parser.parse_args().ometiff[0],
            i_timestep = o_parser.parse_args().timestep,
            s_intensity_cmap = None if (o_parser.parse_args().intensity_cmap.lower() == 'none') else o_parser.parse_args().intensity_cmap,
        )
    # print neuroglancer viewer url
    print(viewer)
