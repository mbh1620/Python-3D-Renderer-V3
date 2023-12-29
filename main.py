from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
from Classes.Face import Face
from Classes.Light import Light
from Classes.FileWriteReader import FileWriteReader
from Functions.cubeGenerator import cubeGenerator
from Functions.axisGenerator import axisGenerator
from Functions.normaliseVector import crossProduct
import numpy as np

centerPoint = Wireframe()

centerPoint.addNodes([[0,0,0]])

projectionViewer1 = ProjectionViewer(1200,1000, centerPoint)
	
projectionViewer1.addWireframe('centerPoint', centerPoint)

# cube1 = cubeGenerator([0,0,0], 1000)

object1 = FileWriteReader("./teapot.obj", 1000)

objwireframe = object1.createWireframe()

projectionViewer1.addWireframe('teapot', objwireframe)

projectionViewer1.run()