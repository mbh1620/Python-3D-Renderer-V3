from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
from Classes.Face import Face
from Classes.FileWriteReader import FileWriteReader
from Functions.cubeGenerator import cubeGenerator
from Functions.axisGenerator import axisGenerator
from Functions.normaliseVector import crossProduct
import numpy as np

centerPoint = Wireframe()

centerPoint.addNodes([[0,0,0]])

projectionViewer1 = ProjectionViewer(1200,1000, centerPoint)
	
projectionViewer1.addWireframe('centerPoint', centerPoint)

object1 = FileWriteReader("./blenderCube.obj", 1000)

objwireframe = object1.createWireframe()

cube1 = cubeGenerator([2000,-1000,0], 2000)

projectionViewer1.addWireframe('cube', objwireframe)

projectionViewer1.addWireframe('cube2', cube1)

projectionViewer1.run()