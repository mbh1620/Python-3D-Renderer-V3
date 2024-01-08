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

	edges = [[0,1],[1,2],[2,3],[3,0],
		[4,5], [5,6], [6,7], [7,4],
		[4,0], [5,1], [6,2], [7,3]]

	faces = [Face([0,2,1], [0,0,0], []),
			 Face([0,3,2], [0,0,0], []),
			 Face([7,4,5], [0,0,0], []),
			 Face([7,5,6], [0,0,0], []),
			 Face([6,5,1], [0,0,0], []),
			 Face([6,1,2], [0,0,0], []),
			 Face([3,0,4], [0,0,0], []),
			 Face([3,4,7], [0,0,0], []),
			 Face([1,5,4], [0,0,0], []),
			 Face([0,1,4], [0,0,0], []),
			 Face([6,2,3], [0,0,0], []),
			 Face([7,6,3], [0,0,0], [])]
			 
	cubeWireframe.addEdges(edges)
	cubeWireframe.addFaces(faces)

	return cubeWireframe

