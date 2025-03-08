#########
# title: ometiff2neuro.py
#
# language: python3
# date: 2022-02-16
# license: MIT
# author: jason lu, viviana kwong, elmar bucher
#
# installation:
#     conda create -n neuro python=3   # generate an own python environment for to run this code.
#     conda activate neuro   # activate the generated python environment.
#     pip install neuroglancer   # the basics
#     pip install ipython   # for coding
#     pip install matplotlib   # for expression value color maps
#     pip install scikit-image   # for loading images as numpy array and signal thresh
#     #pip install bioio   # for extracting ometiff metadata
#
# test dataset:
#     conda activate neuro
#     pip install synapseclient   # for downloading the test dataset from synapse
#     synapse get -r syn26848775   # download test dataset into the current work directory folder.
#
# run:
#     python3 -i ometiff2neuro.py <path/filename.tiff>
#
# description:
#   script to render multi channel multi slice (ome)tiff files into the
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
from matplotlib import cm
import neuroglancer
import neuroglancer.cli
import numpy as np
from skimage import exposure, filters, io, util
import sys


# functions
def ometiff2neuro(
        o_state,
        s_pathfile_tiff,
        ls_channel_label = None, # ['DNA1','PD1','TLR3','SOX10', 'DNA2','CD163','CD3D','PDL1','DNA3','CD4','ICOS','HLADPB1','DNA4','CD8A','CD68','GZMB','DNA5','CD40L','LAG3','HLAA','DNA6','SQSTM','VIN','TIM3', 'DNA7','LAMP1/CD107A','PDL1_2','PD1_2', 'nuc_segement'], # dataset dependent information.
        o_intensity_cm = cm.gray,  # None
        b_intensity_norm = True,  # False
        o_thresh = filters.threshold_li,  # None
        di_coor = {'c':1, 'z':0, 'y':2, 'x':3},  # dataset dependent information.
        di_nm = {'z':200, 'y':108, 'x':108},  # microscope dependent information.
        e_render = None,  # {0, 'CD4', 'CD8A', 'GZMB', 28},
    ):
    '''
    input:
        o_state: neuroglancer viewer state object.

        s_pathfile_tiff: file name and path to input tiff file.

        ls_channel_label: list of channel labels.
            default is None.
            if None, hexadecimal channel labels will be generated.
            this is dataset dependent information.
            in future, if ometiff metadata is provided, this information will be extracted from the ometiff metadata.

        o_intensity_cm: matlab color map object, used to display expression intensity values.
            default is cm.gray.
            if None, no intensity layers will be generated.

        b_intensity_norm: boolean.
            default is True.
            if True, expression intensity values will be cut by the 2.5 and 97.5 percentiles, to remove outliers,
                and intensity will be stretched over the whole range.

        o_thresh: skimage.filter thresh method object to threshold non-threshed data.
            default is filters.threshold_li.
            this is dataset dependent information.
            set None if the tiff contains no raw but already threshed or segmentation mask data!

        di_coor: dictionary of integers, to link c,z,y, and x channel to the corresponding tiff (numpy array) columns.
            this is dataset dependent information.
            in future, if ometiff metadata is provided, this information will be extracted from the ometiff metadata.

        di_nm: dictionary of integers, to specify z slice distance, and y x pixel size in nanometer.
            this is microscope dependent information.
            in future, if ometiff metadata is provided, this information will be extracted from the ometiff metadata.

        e_render: set of channel marker labels and/or integers to specify which markers should be rendered into neurogalncer.
            default is None.
            if None, all channels will be rendered into neuroglancer (if enough RAM is available).

    output:
        local url where the rendered data can be viewed.

    description:
        function to render multi channel multi slice (ome)tiff files into the neuroglancer software.
    '''
    print(f'\nprocessing: {s_pathfile_tiff}')

    # load tiff image as numpy array
    a_img =  io.imread(s_pathfile_tiff)
    print(f'image shape ({[m[0] for m in sorted(di_coor.items(), key=lambda n: n[1])]}): {a_img.shape}')

    # channel count
    i_channel = a_img.shape[di_coor['c']]

    # handle channel labels
    if ls_channel_label is None:
        ls_channel_label = [hex(n) for n in range(i_channel)]
    elif len(ls_channel_label) != i_channel:
        sys.exit(f'Error @ ometiff2neuro : ls_channel_label shape (len(ls_channel_label)) does not match channel shape {i_channel}.')
    print(f'ls_channel_label: {ls_channel_label}')

    # handle set with labels from channels that will be rendered
    if e_render is None:
        e_render = set(range(i_channel))

    # generate neuroglancer layers #
    i_c = di_coor['c']
    for i_n in range(i_channel):
        s_label = ls_channel_label[i_n]
        print(f'check channel {i_n}/{i_channel}: {s_label}')
        if (i_n in e_render) or (s_label in e_render):
            print(f'rendering channel {i_n}/{i_channel}: {s_label}')

            # extract data and xyz coordinate columns
            i_x = di_coor['x']
            i_y = di_coor['y']
            i_z = di_coor['z']
            if i_c == 0:
                a_channel = a_img[i_n,:,:,:]
            elif i_c == 1:
                a_channel = a_img[:,i_n,:,:]
                if di_coor['x'] > i_c:
                    i_x -= 1
                if di_coor['y'] > i_c:
                    i_y -= 1
                if di_coor['z'] > i_c:
                    i_z -= 1
            elif i_c == 2:
                a_channel = a_img[:,:,i_n,:]
                if di_coor['x'] > i_c:
                    i_x -= 1
                if di_coor['y'] > i_c:
                    i_y -= 1
                if di_coor['z'] > i_c:
                    i_z -= 1
            elif i_c == 3:
                a_channel = a_img[:,:,:,i_n]
            else:
                sys.exit(f'Error @ ometiff2neuro : the source code is broken. please, fix the script.')


            # 3D rendering #
            # thresh data
            a_thresh = a_channel.copy()
            if not (o_thresh is None):
                r_thresh = o_thresh(a_thresh)
                a_thresh[a_thresh < r_thresh] = 0
            ab_thresh = a_thresh > 0

            # shape
            a_shape = np.zeros(ab_thresh.shape, dtype=np.uint32)
            a_shape[ab_thresh] = i_n + 1

            # generate neuroglancer object
            ls_name = [None, None, None]
            ls_name[i_x] = 'x'
            ls_name[i_y] = 'y'
            ls_name[i_z] = 'z'
            li_scale = [None, None, None]
            li_scale[i_x] = di_nm['x']
            li_scale[i_y] = di_nm['y']
            li_scale[i_z] = di_nm['z']
            state.layers.append(
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
            )


            # expression intensity rendering #
            if not (o_intensity_cm is None):

                # normalize expression values by clip by two sigma and scale over the whole uint range
                if (b_intensity_norm):
                    i_min_clip = int(np.percentile(a_channel, 2.5))
                    i_max_clip = int(np.percentile(a_channel, 97.5))
                    a_clipped = np.clip(a_channel, a_min=i_min_clip, a_max=i_max_clip)
                    a_channel = exposure.rescale_intensity(a_clipped, in_range='image')  # 16 or 8[bit] normalized

                # translate intensity by color map
                a_8bit = util.img_as_ubyte(a_channel)
                a_intensity = o_intensity_cm(a_8bit, alpha=None, bytes=True)[:,:,:,0:3]

                # generate neuroglancer object
                ls_name = [None, None, None,'c^']
                ls_name[i_x] = 'x'
                ls_name[i_y] = 'y'
                ls_name[i_z] = 'z'
                li_scale = [None, None, None, 3]
                li_scale[i_x] = di_nm['x']
                li_scale[i_y] = di_nm['y']
                li_scale[i_z] = di_nm['z']
                state.layers.append(
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
    o_parser = argparse.ArgumentParser(description='Script to render ome.tiff files into the neuroglancer software.')
    # request path to ometiff and file name as command line argument
    o_parser.add_argument('ometiff', type=str, nargs=1, help='ome.tiff path/filename')
    # start neuroglancer
    neuroglancer.cli.add_server_arguments(o_parser)
    neuroglancer.cli.handle_server_arguments(o_parser.parse_args())
    viewer = neuroglancer.Viewer()
    with viewer.txn() as state:
        # render ometiff
        ometiff2neuro(
            o_state = state,
            s_pathfile_tiff = o_parser.parse_args().ometiff[0],
        )
    # print neuroglancer viewer url
    print(viewer)
