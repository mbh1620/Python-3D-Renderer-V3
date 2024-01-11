import pygame
import numpy as np
import math
from Classes.Face import Face
from Classes.Camera import Camera
from Classes.Wireframe import Wireframe
from Classes.Light import Light
from Classes.FileWriteReader import FileWriteReader
from Functions.normaliseVector import normaliseVector
from Functions.normaliseVector import dotProduct
from Functions.normaliseVector import vectorSubtract
from Functions.normaliseVector import crossProduct
from Functions.normaliseVector import vectorMultiply
from Functions.normaliseVector import vectorAdd
from Functions.normaliseVector import vectorDivide
from Functions.normaliseVector import sortFaces
from Functions.normaliseVector import calculateTriangleCenter
from Functions.normaliseVector import calculateFaceNormal
from Functions.normaliseVector import clamp

class ProjectionViewer:

	def __init__(self, width, height, centerPoint):

		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('3D Renderer')

		self.backgroundColour = (10,10,50)
		self.camera = Camera([0,0,0],0,0, self)
		self.centerPoint = centerPoint

		self.lights = {}

		self.wireframes = {}
		self.materials = {}

		self.initialise()

		pygame.init()

	def initialise(self):

		light1 = Light([200,200,200], 1, [1,1,1])

		self.addLight(light1)

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

		if wireframe.displayNodes:

			for node in wireframe.perspectiveNodes:

				if self.clipNodeAgainstPlane([0,0,400], [0,0,1], node) == True:

					pygame.draw.circle(self.screen, wireframe.nodeColour, (int(node[0]), int(node[1])), wireframe.nodeRadius, 0)

	def displayEdges(self, wireframe):

		if wireframe.displayEdges:

			for edge in wireframe.edges:

				outputPoints = self.clipEdgeAgainstPlane([0,0,400], [0,0,1], edge, wireframe)

				if len(outputPoints) == 2:

					pygame.draw.aaline(self.screen, wireframe.edgeColour, outputPoints[0][:2], outputPoints[1][:2], 1)

	def displayFaces(self, wireframe):

		triangles = []

		if wireframe.displayFaces:

			for face in wireframe.faces:

				baseColour = face.material

				outputPoints = self.clipFaceAgainstPlane([0,0,400], [0,0,1], face, wireframe)

				if len(outputPoints) == 3:

					if self.backFaceCull(self.addPerspectiveToNode(outputPoints[0]), self.addPerspectiveToNode(outputPoints[1]), self.addPerspectiveToNode(outputPoints[2])):

						triangles.append([outputPoints[0], outputPoints[1], outputPoints[2]])

				elif len(outputPoints) == 6:
				
					if self.backFaceCull(self.addPerspectiveToNode(outputPoints[0]), self.addPerspectiveToNode(outputPoints[1]), self.addPerspectiveToNode(outputPoints[2])):

						triangles.append([outputPoints[0], outputPoints[1], outputPoints[2]])

					if self.backFaceCull(self.addPerspectiveToNode(outputPoints[3]), self.addPerspectiveToNode(outputPoints[4]), self.addPerspectiveToNode(outputPoints[5])):

						triangles.append([outputPoints[3], outputPoints[4], outputPoints[5]])

			j = 0

			sortFaces(triangles)

			for i in triangles:

				shading = self.calculateShading([i[0], i[1], i[2]], wireframe, baseColour)

				iPerspective = [self.addPerspectiveToNode(i[0]), self.addPerspectiveToNode(i[1]), self.addPerspectiveToNode(i[2])]
				
				pygame.draw.polygon(self.screen, shading, [iPerspective[0][:2], iPerspective[1][:2], iPerspective[2][:2]], 0)
				
				j+=1

	def calculateShading(self, trianglePoints, wireframe, baseColour):

		shadedColour = [0,0,0]

		faceCenter = calculateTriangleCenter(trianglePoints[0], trianglePoints[1], trianglePoints[2])

		triangleNormal = calculateFaceNormal(trianglePoints[0], trianglePoints[1], trianglePoints[2])

		for i in self.lights.keys():

			directionVector = normaliseVector(vectorSubtract(self.wireframes[i].nodes[0], faceCenter))
		
			cosTheta = clamp(dotProduct(directionVector, triangleNormal), 0, 1)

			shadedColour[0] += self.lights[i].intensity*self.lights[i].colour[0]*cosTheta*baseColour[0]
			shadedColour[1] += self.lights[i].intensity*self.lights[i].colour[1]*cosTheta*baseColour[1]
			shadedColour[2] += self.lights[i].intensity*self.lights[i].colour[2]*cosTheta*baseColour[2]

		shadedColour[0] = clamp(shadedColour[0], 0, 255)
		shadedColour[1] = clamp(shadedColour[1], 0, 255)
		shadedColour[2] = clamp(shadedColour[2], 0, 255)

		return shadedColour

	def checkLineOnPlane(self, pointOnPlane, planeNormal, lineStart, lineEnd):

		planeNormal = normaliseVector(planeNormal)
		plane = -dotProduct(planeNormal, pointOnPlane)

		ad = dotProduct(lineStart, planeNormal)
		bd = dotProduct(lineEnd, planeNormal)

		t = (-plane-ad)/(bd-ad)

		lineStartToEnd = vectorSubtract(lineEnd, lineStart)
		lineToIntersect = vectorMultiply(lineStartToEnd, t)

		return vectorAdd(lineStart, lineToIntersect)

	def clipNodeAgainstPlane(self, pointOnPlane, planeNormal, node):

		if self.distanceOfPointToPlane(pointOnPlane, planeNormal, node) > 0:

			return True

		else: 

			return False

	def clipEdgeAgainstPlane(self, pointOnPlane, planeNormal, edge, wireframe):

		planeNormal = normaliseVector(planeNormal)

		distance1 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[edge[0]])
		distance2 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[edge[1]])

		insidePoints = []
		insidePointsDict = {'d1':False, 'd2':False}
		outsidePoints = []
		outputPoints = []

		if distance1 > 0:

			insidePoints.append(wireframe.nodes[edge[0]])
			insidePointsDict['d1'] = True

		else:

			outsidePoints.append(wireframe.nodes[edge[0]])

		if distance2 > 0:

			insidePoints.append(wireframe.nodes[edge[1]])
			insidePointsDict['d2'] = True

		else:

			outsidePoints.append(wireframe.nodes[edge[1]])

		if len(insidePoints) == 2:
			
			outputPoints.append(wireframe.perspectiveNodes[edge[0]])
			outputPoints.append(wireframe.perspectiveNodes[edge[1]])

		elif len(insidePoints) == 1:

			outputPoints.append(self.addPerspectiveToNode(insidePoints[0]))
			outputPoints.append(self.addPerspectiveToNode(self.checkLineOnPlane(pointOnPlane, planeNormal, insidePoints[0], outsidePoints[0])))

		elif len(insidePoints) == 0:
			pass

		return outputPoints

	def clipFaceAgainstPlane(self, pointOnPlane, planeNormal, face, wireframe):

		planeNormal = normaliseVector(planeNormal)

		distance1 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[face.vertices[0]])
		distance2 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[face.vertices[1]])
		distance3 = self.distanceOfPointToPlane(pointOnPlane, planeNormal, wireframe.nodes[face.vertices[2]])

		insidePoints = []
		insidePointsDict = {'d1':False, 'd2':False, 'd3':False}
		outsidePoints = []
		outputPoints = []

		if distance1 > 0:

			insidePoints.append(face.vertices[0])
			insidePointsDict['d1'] = True

		else:

			outsidePoints.append(face.vertices[0])

		if distance2 > 0:

			insidePoints.append(face.vertices[1])
			insidePointsDict['d2'] = True

		else:

			outsidePoints.append(face.vertices[1])

		if distance3 > 0:

			insidePoints.append(face.vertices[2])
			insidePointsDict['d3'] = True

		else:

			outsidePoints.append(face.vertices[2])

		if insidePoints == 0:
			pass

		elif len(insidePoints) == 1:
			
			if insidePointsDict['d2'] == True:

				outputPoints.append(wireframe.nodes[insidePoints[0]])
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[1]]))
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[0]]))

			else:

				outputPoints.append(wireframe.nodes[insidePoints[0]])
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[0]]))
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[1]]))

		elif len(insidePoints) == 2:

			if insidePointsDict['d2'] == False:

				outputPoints.append(wireframe.nodes[insidePoints[0]])
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[0]]))
				outputPoints.append(wireframe.nodes[insidePoints[1]])

				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[1]], wireframe.nodes[outsidePoints[0]]))
				outputPoints.append(wireframe.nodes[insidePoints[1]])
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[0]]))

			else:

				outputPoints.append(wireframe.nodes[insidePoints[0]])
				outputPoints.append(wireframe.nodes[insidePoints[1]])
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[0]]))
			
				outputPoints.append(wireframe.nodes[insidePoints[1]])
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[1]], wireframe.nodes[outsidePoints[0]]))
				outputPoints.append(self.checkLineOnPlane(pointOnPlane, planeNormal, wireframe.nodes[insidePoints[0]], wireframe.nodes[outsidePoints[0]]))

		elif len(insidePoints) == 3:
			
			outputPoints.append(wireframe.nodes[insidePoints[0]])
			outputPoints.append(wireframe.nodes[insidePoints[1]])
			outputPoints.append(wireframe.nodes[insidePoints[2]])

		return outputPoints

	def addPerspectiveToNode(self, node):

		perspectiveNode = node.copy()
		pNode = perspectiveNode
		center = [self.width/2, self.height/2]

		if (self.camera.zoom-node[2]) != 0:

			pNode[0] = (center[0] + (node[0]-center[0])*self.camera.fieldOfView/(self.camera.zoom-(node[2])))
			pNode[1] = (center[1] + (node[1]-center[1])*self.camera.fieldOfView/(self.camera.zoom-(node[2])))
			pNode[2] = node[2] * 1

		return pNode

	def backFaceCull(self, n1, n2, n3):

		output = ((n1[0] * n2[1]) + (n2[0]* n3[1]) + (n3[0] * n1[1])) - ((n3[0] * n2[1]) + (n2[0] * n1[1]) + (n1[0] * n3[1]))

		if output > 0:
			return False
		else: 
			return True

	def distanceOfPointToPlane(self, pointOnPlane, planeNormal, point):

		return ((planeNormal[0] * point[0])+(planeNormal[1]*point[1])+(planeNormal[2]*point[2]) - dotProduct(planeNormal, pointOnPlane))

	def addWireframe(self, name, wireframe):
		
		self.wireframes[name] = wireframe

	def addLight(self, light):

		wireframe = Wireframe()

		wireframe.addNodes(np.array([[light.position[0],light.position[1],light.position[2]]]))

		wireframe.nodeColour = (0, 255, 0)

		self.lights['Light'+str(len(self.lights.values()))] = light

		self.addWireframe('Light'+str(len(self.lights)-1), wireframe)

	def openFile(self, fileName, scaleFactor):

		tempFile = FileWriteReader(fileName, scaleFactor)

		wireframe = tempFile.createWireframe()

		self.addWireframe(fileName+str(len(self.wireframes)), wireframe)

	def processKeys(self, keys):

		key_to_function = {

		pygame.K_LEFT: (lambda x: x.camera.LEFT()),
 		pygame.K_RIGHT:(lambda x: x.camera.RIGHT()),

 		pygame.K_DOWN: (lambda x: x.camera.DOWN()),
 		pygame.K_UP:   (lambda x: x.camera.UP()),

 		pygame.K_w: (lambda x: x.camera.W()),
 		pygame.K_s: (lambda x: x.camera.S()),
 		pygame.K_a: (lambda x: x.camera.A()),
 		pygame.K_d: (lambda x: x.camera.D()),

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

			self.camera.position[2] += amount

			self.translateAll([0, 0, amount])

