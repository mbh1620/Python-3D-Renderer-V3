from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
import numpy as np

centerPoint = []

projectionViewer1 = ProjectionViewer(1200, 1000, centerPoint)

cubeWireframe = Wireframe()

nodes = np.array([[0,10,0],
				  [100,10,100],
				  [0,0,100]])

cubeWireframe.addNodes(nodes)

edge1 = Edge(0,1)
edge2 = Edge(1,2)

cubeWireframe.addEdges([edge1, edge2])

projectionViewer1.addWireframe('cubeWireframe', cubeWireframe)

projectionViewer1.run()