from Classes.Wireframe import Wireframe
from Classes.Face import Face
import numpy as np

def planeGenerator(axis, position, scale):

	planeWireframe = Wireframe()
	
	if axis == 'X':
		nodes = np.array([[0,0,0],
						  [1*scale, 0,0],
						  [1*scale, 0, 1*scale],
						  [0, 0, 1*scale]])

	if axis == 'Y':
		nodes = np.array([[0,0,0],
						  [0, 1*scale,0],
						  [0, 1*scale, 1*scale],
						  [0, 0, 1*scale]])

	if axis == 'Z':
		nodes = np.array([[0,0,0],
						  [1*scale, 0,0],
						  [1*scale, 1*scale, 0],
						  [0, 1*scale, 0]])

	planeWireframe.addNodes(nodes)

	planeWireframe.addFaces([Face([0,2,1], [0,0,0], []),
							 Face([3,2,0], [0,0,0], [])])

	return planeWireframe
