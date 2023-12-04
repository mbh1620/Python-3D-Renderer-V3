import math
import numpy as np

class Wireframe:

	def __init__(self):

		self.nodes = np.zeros((0,4))
		self.edges = []
		self.faces = []

		self.nodeRadius = 3
		self.nodeColour = (255,255,255)

		self.edgeWidth = 1
		self.edgeColour = (255,255,255)

	def addNodes(self, nodeArray):

		onesColumn = np.ones((len(nodeArray), 1))
		onesAdded = np.hstack((nodeArray, onesColumn))
		self.nodes = np.vstack((self.nodes, onesAdded))

	def addFaces(self, faceList):
		self.faces += faceList

	def addEdges(self, edgeList):
		self.edges += edgeList

	def transform(self, matrix):
		self.nodes = np.dot(self.nodes, matrix)

	def translationMatrix(self, dx=0, dy=0, dz=0):

		return np.array([[1,0,0,0],
						 [0,1,0,0],
						 [0,0,1,0],
						 [dx,dy,dz,1]])

	def scaleMatrix(self, sx=0, sy=0, sz=0):

		return np.array([[sx, 0, 0, 0],
						 [0, sy, 0, 0],
						 [0, 0, sz, 0],
						 [0, 0, 0, 1]])

	def rotateXMatrix(self, radians):

		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[1,0,0,0],
						 [0,c,-s,0],
						 [0,s,c,0],
						 [0,0,0,1]])

	def rotateYMatrix(self, radians):

		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[c,0,s,0],
						 [0,1,0,0],
						 [-s,0,c,0],
						 [0,0,0,1]])

	def rotateZMatrix(self, radians):

		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[c,-s,0,0],
						 [s,c,0,0],
						 [0,0,1,0],
						 [0,0,0,1]])

