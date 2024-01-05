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

projectionViewer1.openFile('./blenderCube.obj', 1000)

projectionViewer1.wireframes['./blenderCube.obj2'].displayNodes = True

projectionViewer1.run()