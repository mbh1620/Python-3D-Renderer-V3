from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
import numpy as np

centerPoint = Wireframe()

centerPoint.addNodes([[0,0,0]])

projectionViewer1 = ProjectionViewer(1200,1000, centerPoint)
	
projectionViewer1.addWireframe('centerPoint', centerPoint)

projectionViewer1.openFile('./blenderCube.obj', 1000)
projectionViewer1.wireframes['./blenderCube.obj2'].displayNodes = False

projectionViewer1.run()