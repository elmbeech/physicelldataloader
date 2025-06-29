# PhysiCell Data Loader Tutorial: pcdl and Python and Vtk

[Vtk](https://vtk.org/) the visualization tool kit is a software for image processing, 3D graphics, volume rendering and visualization. \
Naturally, we will work here with the [vtk](https://pypi.org/project/vtk/) python binding.
Additionally, we will have a look at the [pyvista](https://docs.pyvista.org/) and [fury](https://fury.gl/latest/index.html) python libraries for scientific visualization that can read vtk files too.



### How to load and visualize a vtk file with the vtk python library

Installation.

```bash
pip3 install vtk
pip3 install matplotlib
```

Load and display conc.vtr **rectilinear grid** files ~ **colored, transparent cube**.

```python
import vtk

# load file
reader = vtk.vtkXMLRectilinearGridReader()
reader.SetFileName('output/output00000012_conc.vtr')
reader.Update()
grid = reader.GetOutput()

# use scalar field for coloring the grid
scalar_name = 'oxygen'   # 'water'
scalar_array = grid.GetPointData().GetArray(scalar_name)
if scalar_array is None:
    raise RuntimeError(f'Scalar array "{scalar_name}" not found.')
grid.GetPointData().SetActiveScalars(scalar_name)
scalar_range = scalar_array.GetRange()

# generate color lookup table
lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(256)
lut.SetTableRange(scalar_range)
lut.SetHueRange(0.667, 0.0)  # blue to red rainbow
lut.Build()

# convert grid to surface to data
surface = vtk.vtkDataSetSurfaceFilter()
surface.SetInputData(grid)
surface.Update()
polydata = surface.GetOutput()
#polydata.GetPointData().SetScalars(scalar_array)  # overkill

# mapper: map data to geometry
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetLookupTable(lut)
mapper.SetScalarRange(scalar_range)  # min and max value
mapper.SetScalarModeToUsePointData()
mapper.SetColorModeToMapScalars()
mapper.ScalarVisibilityOn()

# actor: map actor to data mapped geometry
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(0.3)  # transparency: 0 is invisible, 1 is opaque
actor.GetProperty().BackfaceCullingOff()  # so we can see interior faces

# actor: color bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle(scalar_name)

# renderer: director
renderer = vtk.vtkRenderer()
renderer.SetBackground(1/3, 1/3, 1/3)  # gray background
renderer.AddActor(actor)
renderer.AddActor2D(scalar_bar)

# enable depth peeling
renderer.UseDepthPeelingOn()
renderer.SetMaximumNumberOfPeels(100)
renderer.SetOcclusionRatio(0.1)

# render window: stage
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)
render_window.AlphaBitPlanesOn()  # enable RGBA rendering
render_window.SetMultiSamples(0)  # disable multisampling (needed for peeling)

# interactor: 4th wall
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# initialize and start the rendering loop
renderer.ResetCamera()
render_window.Render()
interactor.Start()
```

Load and display conc.vtr **rectilinear grid** files ~ **colored z slice out of the cube**.

```python
import vtk

# load file
reader = vtk.vtkXMLRectilinearGridReader()
reader.SetFileName('output/output00000012_conc.vtr')
reader.Update()
grid = reader.GetOutput()

# use scalar field for coloring the grid
scalar_name = 'oxygen'   # 'water'
scalar_array = grid.GetPointData().GetArray(scalar_name)
if scalar_array is None:
    raise RuntimeError(f'Scalar array "{scalar_name}" not found.')
grid.GetPointData().SetActiveScalars(scalar_name)
scalar_range = scalar_array.GetRange()

# generate color lookup table
lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(256)
lut.SetTableRange(scalar_range)
lut.SetHueRange(0.667, 0.0)  # blue to red rainbow
lut.Build()

# convert grid to z slice to data
# generate xy plane at z center
bounds = grid.GetBounds()
z_center = 0.5 * (bounds[4] + bounds[5])
plane = vtk.vtkPlane()
plane.SetOrigin(0.5 * (bounds[0] + bounds[1]), 0.5 * (bounds[2] + bounds[3]), center_z)
plane.SetNormal(0, 0, 1)  # slice in z
# cut xy plain at z center
cutter = vtk.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputData(grid)
cutter.Update()
# get xy plain data at z center
polydata_zslice = cutter.GetOutput()

# mapper: map data to geometry
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata_zslice)
mapper.SetLookupTable(lut)
mapper.SetScalarRange(scalar_range)
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUsePointData()
mapper.ScalarVisibilityOn()

# actor: map actor to data mapped geometry
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# actor: color bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle(scalar_name)

# renderer: director
renderer = vtk.vtkRenderer()
renderer.SetBackground(1/3, 1/3, 1/3)  # gray background
renderer.AddActor(actor)
renderer.AddActor2D(scalar_bar)

# render window: stage
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# interactor: 4th wall
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# initialize and start the rendering loop
renderer.ResetCamera()
render_window.Render()
interactor.Start()
```

Load and display cell.vtp **polydata** files ~ **no coloring**.

```python
import vtk

# load file
vtp_reader = vtk.vtkXMLPolyDataReader()
vtp_reader.SetFileName('output/output00000012_cell.vtp')
vtp_reader.Update()
polydatapipe = vtp_reader.GetOutputPort()

# mapper: map data to geometry
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(polydatapipe)

# actor: map actor to data mapped geometry
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# renderer: director
renderer = vtk.vtkRenderer()
renderer.SetBackground(1/3, 1/3, 1/3)  # gray background
renderer.AddActor(actor)

# render window: stage
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# interactor: 4th wall
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# initialize and start the rendering loop
render_window.Render()
interactor.Start()
```

Load and display cell.vtp **polydata** files ~ **numerical data coloring**.

```python
import vtk

# load file
vtp_reader = vtk.vtkXMLPolyDataReader()
vtp_reader.SetFileName('output/output00000012_cell.vtp')
vtp_reader.Update()
polydata = vtp_reader.GetOutput()

# get color data
scalar_name = 'pressure'    # 'positions_and_radii'
scalar_array = polydata.GetPointData().GetArray(scalar_name)
if scalar_array is None:
    raise RuntimeError(f'Scalar array "{scalar_name}" not found.')
scalar_range = scalar_array.GetRange()

# set color data
polydata.GetPointData().SetActiveScalars(scalar_name)

# mapper: map data to geometry
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetScalarRange(scalar_range)  # min and max value
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray(scalar_name)
mapper.SetColorModeToMapScalars()
mapper.ScalarVisibilityOn()

# actor: map actor to data mapped geometry
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# actor: map actor to color bar
scalar_bar = vtk.vtkScalarBarActor()
lut = mapper.GetLookupTable()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle(scalar_name)

# renderer: director
renderer = vtk.vtkRenderer()
renderer.SetBackground(1/3, 1/3, 1/3)  # gray background
renderer.AddActor(actor)
renderer.AddActor2D(scalar_bar)  # color bar ~ if color mapping

# render window: stage
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# interactor: 4th wall
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# initialize and start the rendering loop
render_window.Render()
interactor.Start()
```

Load and display cell.vtp **polydata** files ~ **categorical data coloring**.

```python
import matplotlib.pyplot as plt
import vtk

# load file
vtp_reader = vtk.vtkXMLPolyDataReader()
vtp_reader.SetFileName('output/output00000012_cell.vtp')
vtp_reader.Update()
polydata = vtp_reader.GetOutput()

# get color data
scalar_name_cat = 'cell_type'
scalar_array_str = polydata.GetPointData().GetAbstractArray(scalar_name_cat)
scalar_name_num = scalar_name_cat + '_numeric'
scalar_array = vtk.vtkIntArray()
scalar_array.SetName(scalar_name_num)

# unique categoris
es_cat = set()
for i_cat in range(scalar_array_str.GetNumberOfValues()):
    s_cat = scalar_array_str.GetValue(i_cat)
    es_cat.add(s_cat)

# index unique categories
dsi_cat = {}
for i_cat, s_cat in enumerate(sorted(es_cat)):
    dsi_cat.update({s_cat: i_cat})

# map each element of the array to the category index
for i in range(scalar_array_str.GetNumberOfValues()):
    s_cat = scalar_array_str.GetValue(i)
    scalar_array.InsertNextValue(dsi_cat[s_cat])
scalar_range = scalar_array.GetRange()

# set color data
polydata.GetPointData().AddArray(scalar_array)
polydata.GetPointData().SetActiveScalars(scalar_name_num)

# look up table
lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(len(es_cat))
lut.Build()
cmap = plt.get_cmap('turbo', len(es_cat))
for s_cat, i_cat in dsi_cat.items():
    r, g, b, _ = cmap(i_cat)
    lut.SetTableValue(i_cat, r, g, b, 1.0)
    lut.SetAnnotation(i_cat, s_cat)

# mapper: map data to geometry
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetLookupTable(lut)
mapper.SetScalarRange(scalar_range)  # min and max value
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray(scalar_name_num)
mapper.SetColorModeToMapScalars()
mapper.ScalarVisibilityOn()

# actor: map actor to data mapped geometry
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# actor: color bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle(scalar_name_cat)
scalar_bar.DrawTickLabelsOff()

# renderer: director
renderer = vtk.vtkRenderer()
renderer.SetBackground(1/3, 1/3, 1/3)  # gray background
renderer.AddActor(actor)
renderer.AddActor2D(scalar_bar)  # color bar ~ if color mapping

# render window: stage
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# interactor: 4th wall
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# initialize and start the rendering loop
render_window.Render()
interactor.Start()
```

Official documentation:
+ https://book.vtk.org/en/latest/index.html
+ https://docs.vtk.org/en/latest/index.html
+ https://examples.vtk.org/site/Python/
+ https://examples.vtk.org/site/PythonHowTo/
+ https://examples.vtk.org/site/PythonicAPI/
+ https://examples.vtk.org/site/PythonicAPIComments/


### How to load and visualize a vtk file with the pyvista python library

Installation.

```bash
pip3 install pyvista
```

Load, color, and display **cell.vtr rectilinear grid** files.

```python
import pyvista as pv

grid = pv.read('output/output00000012_conc.vtr')
grid.plot(scalars='oxygen', cmap='turbo', opacity=1/3)  # 'water'
```

Load, color, and display **cell.vtp polydata** files.

```python
import pyvista as pv

poly = pv.read('output/output00000012_cell.vtp')
poly.plot(scalars='cell_type', cmap='turbo', opacity=2/3)  # 'pressure', 'positions_and_radii'
```

Official documentation:
+ https://docs.pyvista.org/

Hasta la vista, baby!


### How to load and visualize a vtk file with the fury python library

Installation.

```bash
pip3 install fury
```

Unfortunately, **conc.vtr rectilinear grid** files are not yet supported (v0.12.0 and 2.0.0a1); conc.vtr files cannot be loaded.
Although this issue might be resolved any time now.
+ https://github.com/fury-gl/fury/issues/971


Load and display **cell.vtp polydata** files ~ **no coloring**.

```python
import fury

# load file
v_cell = fury.io.load_polydata('output/output00000012_cell.vtp')

# actor
actor = fury.get_actor_from_polydata(v_cell)

# scene
scene = fury.window.Scene()
scene.add(actor)

# initialize and start the rendering loop
showm = fury.window.ShowManager(scene)
showm.initialize()
showm.start()
```

Official documentation:
+ https://fury.gl/latest/index.html

