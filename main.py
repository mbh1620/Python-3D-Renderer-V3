from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Functions.cubeGenerator import cubeGenerator
import numpy as np

centerPoint = Wireframe()

centerPoint.addNodes([[0,0,0]])

projectionViewer1 = ProjectionViewer(1200,1000, centerPoint)
	
projectionViewer1.addWireframe('centerPoint', centerPoint)

cube1 = cubeGenerator([0,0,0], 1000)

projectionViewer1.addWireframe('cube1', cube1)

projectionViewer1.wireframes['cube1'].displayFaces = False

# projectionViewer1.openFile('./blenderCube.obj', 100)
# projectionViewer1.wireframes['./blenderCube.obj2'].displayFaces = True


projectionViewer1.run()