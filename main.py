from Classes.ProjectionViewer import ProjectionViewer
from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
from Classes.Face import Face
import numpy as np

centerPoint = []

projectionViewer1 = ProjectionViewer(1200, 1000, centerPoint)

cubeWireframe = Wireframe()

nodes = np.array([[0,0,0],
				  [100,0,0],
				  [100,100,0],
				  [0,100,0],
				  [0,0,100],
				  [100,0,100],
				  [100,100,100],
				  [0,100,100]],
				  )

cubeWireframe.addNodes(nodes)

edges = [Edge(0,1),Edge(1,2),Edge(2,3),Edge(3,0),
		Edge(4,5), Edge(5,6), Edge(6,7), Edge(7,4),
		Edge(4,0), Edge(5,1), Edge(6,2), Edge(7,3)]

cubeWireframe.addEdges(edges)

faces = [Face([0,1,2], [0,0,0], 0), Face([2,3,0], [0,0,0], 0)]

cubeWireframe.addFaces(faces)

projectionViewer1.addWireframe('cubeWireframe', cubeWireframe)

projectionViewer1.run()