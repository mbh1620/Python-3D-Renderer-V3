from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
from Classes.Face import Face
import numpy as np

def cubeGenerator(position, size):

	cubeWireframe = Wireframe()

	nodes = np.array([[0+position[0],0+position[1],0+position[2]],
				  	[1*size+position[0],0+position[1],0+position[2]],
				  	[1*size+position[0],1*size+position[1],0+position[2]],
				  	[0+position[0],1*size+position[1],0+position[2]],
				  	[0+position[0],0+position[1],1*size+position[2]],
				  	[1*size+position[0],0+position[1],1*size+position[2]],
				  	[1*size+position[0],1*size+position[1],1*size+position[2]],
				  	[0+position[0],1*size+position[1],1*size+position[2]]],
				  	)

	cubeWireframe.addNodes(nodes)

	edges = [Edge(0,1),Edge(1,2),Edge(2,3),Edge(3,0),
		Edge(4,5), Edge(5,6), Edge(6,7), Edge(7,4),
		Edge(4,0), Edge(5,1), Edge(6,2), Edge(7,3)]

	faces = [Face([0,1,2], [0,0,0], []),
			 Face([2,3,0], [0,0,0], []),
			 Face([4,5,6], [0,0,0], []),
			 Face([6,7,4], [0,0,0], []),
			 Face([1,5,6], [0,0,0], []),
			 Face([6,2,1], [0,0,0], []),
			 Face([1,5,4], [0,0,0], [])]
			 
	cubeWireframe.addEdges(edges)
	cubeWireframe.addFaces(faces)

	return cubeWireframe

