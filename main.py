from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
from Classes.Face import Face
from Functions.cubeGenerator import cubeGenerator
from Functions.axisGenerator import axisGenerator
from Functions.normaliseVector import crossProduct
import numpy as np

centerPoint = Wireframe()

centerPoint.addNodes([[0,0,0]])

projectionViewer1 = ProjectionViewer(1200, 1000, centerPoint)

axis1 = axisGenerator(500)

cube3 = cubeGenerator([500,500,500], 1000)

projectionViewer1.addWireframe('centerPoint', centerPoint)

projectionViewer1.addWireframe('axis1', axis1)
projectionViewer1.addWireframe('cubeWireframe3', cube3)

projectionViewer1.run()