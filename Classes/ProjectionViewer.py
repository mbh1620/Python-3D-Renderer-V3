
import pygame
import numpy as np
from Classes.Face import Face
from Classes.Camera import Camera
from Classes.Wireframe import Wireframe
from Functions.normaliseVector import normaliseVector
from Functions.normaliseVector import dotProduct
from Functions.normaliseVector import vectorSubtract
from Functions.normaliseVector import crossProduct
from Functions.normaliseVector import vectorMultiply
from Functions.normaliseVector import vectorAdd

class ProjectionViewer:

	def __init__(self, width, height, centerPoint):

		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('3D Renderer')

		self.backgroundColour = (10,10,50)
		self.camera = Camera([0,0,0],0,0)
		self.centerPoint = centerPoint

		self.wireframes = {}

		pygame.init()

	def run(self):

		running = True

		while running:

			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			self.processKeys(keys)
			self.display()

			pygame.display.flip()

	def display(self):

		self.screen.fill(self.backgroundColour)

		for wireframe in self.wireframes.values():

			wireframe.transformForPerspective((self.width/2, self.height/2), self.camera.fieldOfView, self.camera.zoom)

			self.displayNodes(wireframe)

			self.displayEdges(wireframe)

			self.displayFaces(wireframe)

	def displayNodes(self, wireframe):

		for node in wireframe.perspectiveNodes:

			if self.checkNode(node, wireframe):

				pygame.draw.circle(self.screen, wireframe.nodeColour, (int(node[0]), int(node[1])), wireframe.nodeRadius, 0)

	def displayEdges(self, wireframe):

		for edge in wireframe.edges:

			if self.checkEdge(edge, wireframe):

				pygame.draw.aaline(self.screen, wireframe.edgeColour, wireframe.perspectiveNodes[edge.node1Index][:2], wireframe.perspectiveNodes[edge.node2Index][:2], 1)

	def displayFaces(self, wireframe):

		for face in wireframe.faces:

			n1, n2, n3 = face.vertices

			# if self.checkFace(face, wireframe):

			outputPoints = self.clipFaceAgainstPlane([0,0,1000], [0,0,1], face, wireframe)

			if len(outputPoints) == 3:

				pygame.draw.polygon(self.screen, (255,0,0), [outputPoints[0][:2], outputPoints[1][:2], outputPoints[2][:2]], 0)

			elif len(outputPoints) == 6:
				
				pygame.draw.polygon(self.screen, (0,0,255), [outputPoints[0][:2], outputPoints[1][:2], outputPoints[2][:2]], 0)
				pygame.draw.polygon(self.screen, (0,255,0), [outputPoints[3][:2], outputPoints[4][:2], outputPoints[5][:2]], 0)

	def checkNode(self, node, wireframe):

		if self.camera.zoom-node[2] < 0:

			return True

		else:

			return False

	def checkEdge(self, edge, wireframe):

		if self.camera.zoom - wireframe.perspectiveNodes[edge.node1Index][2] < 0 and self.camera.zoom - wireframe.perspectiveNodes[edge.node2Index][2] < 0:

			return True

		else:

			return False

	def checkFace(self, face, wireframe):

		n1, n2, n3 = face.vertices

		if self.camera.zoom - wireframe.perspectiveNodes[n1][2] < 0 and self.camera.zoom - wireframe.perspectiveNodes[n2][2] < 0 and self.camera.zoom - wireframe.perspectiveNodes[n3][2]:

			return True

		else:

			return False

	def checkLineOnPlane(self, pointOnPlane, planeNormal, lineStart, lineEnd):

		planeNormal = normaliseVector(planeNormal)
		plane = -dotProduct(planeNormal, pointOnPlane)

		ad = dotProduct(lineStart, planeNormal)
		bd = dotProduct(lineEnd, planeNormal)

		t = (-plane-ad)/(bd-ad)

		lineStartToEnd = vectorSubtract(lineEnd, lineStart)
		lineToIntersect = vectorMultiply(lineStartToEnd, t)

		return vectorAdd(lineStart, lineToIntersect)

	def clipFaceAgainstPlane(self, pointOnPlane, planeNormal, face, wireframe):

		planeNormal = normaliseVector(planeNormal)

		distance1 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[face.vertices[0]])
		distance2 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[face.vertices[1]])
		distance3 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[face.vertices[2]])

		insidePoints = []
		outsidePoints = []

		outputPoints = []

		if distance1 > 0:

			insidePoints.append(face.vertices[0])

		else:

			outsidePoints.append(face.vertices[0])

		if distance2 > 0:

			insidePoints.append(face.vertices[1])

		else:

			outsidePoints.append(face.vertices[1])

		if distance3 > 0:

			insidePoints.append(face.vertices[2])

		else:

			outsidePoints.append(face.vertices[2])

		if insidePoints == 0:
			pass

		elif len(insidePoints) == 1:
			
			outputPoints.append(wireframe.perspectiveNodes[insidePoints[0]])
			outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.perspectiveNodes[insidePoints[0]], wireframe.perspectiveNodes[outsidePoints[0]]))
			outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.perspectiveNodes[insidePoints[0]], wireframe.perspectiveNodes[outsidePoints[1]]))

		elif len(insidePoints) == 2:

			outputPoints.append(wireframe.perspectiveNodes[insidePoints[0]])
			outputPoints.append(wireframe.perspectiveNodes[insidePoints[1]])
			outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.perspectiveNodes[insidePoints[0]], wireframe.perspectiveNodes[outsidePoints[0]]))

			outputPoints.append(wireframe.perspectiveNodes[insidePoints[1]])
			outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.perspectiveNodes[insidePoints[1]], wireframe.perspectiveNodes[outsidePoints[0]]))
			outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.perspectiveNodes[insidePoints[0]], wireframe.perspectiveNodes[outsidePoints[0]]))

		elif len(insidePoints) == 3:
			
			outputPoints.append(wireframe.perspectiveNodes[insidePoints[0]])
			outputPoints.append(wireframe.perspectiveNodes[insidePoints[1]])
			outputPoints.append(wireframe.perspectiveNodes[insidePoints[2]])

		return outputPoints

	def distanceOfPointToPlane(self, pointOnPlane, planeNormal, point):

		return ((planeNormal[0] * point[0])+(planeNormal[1]*point[1])+(planeNormal[2]*point[2]) - dotProduct(planeNormal, pointOnPlane))

	def addWireframe(self, name, wireframe):
		self.wireframes[name] = wireframe

	def processKeys(self, keys):

		key_to_function = {

		pygame.K_LEFT: (lambda x: x.rotateAboutCamera('Y', 0.05)),
 		pygame.K_RIGHT:(lambda x: x.rotateAboutCamera('Y', -0.05)),
 		pygame.K_DOWN: (lambda x: x.moveCameraVertically(20)),
 		pygame.K_UP:   (lambda x: x.moveCameraVertically(-20)),

 		pygame.K_w: (lambda x: x.moveCameraHorizontally('Z', -20)),
 		pygame.K_s: (lambda x: x.moveCameraHorizontally('Z', 20)),
 		pygame.K_a: (lambda x: x.moveCameraHorizontally('X', -20)),
 		pygame.K_d: (lambda x: x.moveCameraHorizontally('X', 20)),

		}

		if keys[pygame.K_LEFT]:
			key_to_function[pygame.K_LEFT](self)
		if keys[pygame.K_RIGHT]:
			key_to_function[pygame.K_RIGHT](self)
		if keys[pygame.K_DOWN]:
			key_to_function[pygame.K_DOWN](self)
		if keys[pygame.K_UP]:
			key_to_function[pygame.K_UP](self)
		if keys[pygame.K_w]:
			key_to_function[pygame.K_w](self)
		if keys[pygame.K_a]:
			key_to_function[pygame.K_a](self)
		if keys[pygame.K_s]:
			key_to_function[pygame.K_s](self)
		if keys[pygame.K_d]:
			key_to_function[pygame.K_d](self)

	def translateAll(self, vector):

		wf = Wireframe()
		matrix = wf.translationMatrix(*vector)
		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def rotateAboutCamera(self, axis, theta):
		wf = Wireframe()

		matrix = wf.translationMatrix(-self.width/2, -self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		wf = Wireframe()
		if axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)
		
		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def moveCameraVertically(self, amount):
		
		self.translateAll([0, amount, 0])

	def moveCameraHorizontally(self, axis, amount):
		
		if axis == 'X':

			self.translateAll([amount, 0, 0])

		if axis == 'Z':

			self.translateAll([0, 0, amount])

