from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
from Classes.Face import Face
from Classes.Light import Light
from Classes.FileWriteReader import FileWriteReader
from Functions.cubeGenerator import cubeGenerator
from Functions.axisGenerator import axisGenerator
from Functions.planeGenerator import planeGenerator
from Functions.normaliseVector import crossProduct
import numpy as np

centerPoint = Wireframe()

centerPoint.addNodes([[0,0,0]])

projectionViewer1 = ProjectionViewer(1200,1000, centerPoint)
	
projectionViewer1.addWireframe('centerPoint', centerPoint)

projectionViewer1.openFile('./grid.obj', 1000)

projectionViewer1.wireframes['./grid.obj2'].displayNodes = False

light2 = Light([5000, 5000, 0], 1, [0.95, 0.85, 0.8])

projectionViewer1.addLight(light2)

projectionViewer1.run()