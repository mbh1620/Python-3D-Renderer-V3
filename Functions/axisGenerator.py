from Classes.Wireframe import Wireframe
from Classes.Edge import Edge
import numpy as np

def axisGenerator(size):

	axisWireframe = Wireframe()

	nodes = [[0,0,0],
			 [size, 0, 0],
			 [0, size, 0]]

	axisWireframe.addNodes(nodes)
	axisWireframe.addEdges([Edge(0,1), Edge(0,2)])

	return axisWireframe