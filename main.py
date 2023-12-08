from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
from Classes.Face import Face
from Functions.cubeGenerator import cubeGenerator
from Functions.axisGenerator import axisGenerator
import numpy as np

centerPoint = Wireframe()

centerPoint.addNodes([[0,0,0]])

projectionViewer1 = ProjectionViewer(1200, 1000, centerPoint)

axis1 = axisGenerator(500)

cube1 = cubeGenerator([200,200,200], 200)

cube2 = cubeGenerator([0,0,0], 100)

projectionViewer1.addWireframe('axis1', axis1)
projectionViewer1.addWireframe('cubeWireframe', cube1)
projectionViewer1.addWireframe('cubeWireframe2', cube2)

projectionViewer1.run()