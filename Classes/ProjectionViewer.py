
import pygame
import numpy as np
from Classes.Face import Face
from Classes.Camera import Camera
from Classes.Wireframe import Wireframe

class ProjectionViewer:

	def __init__(self, width, height, centerPoint):

		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('3D Renderer')

		self.viewType = 'orthographic' #Can be orthographic or perspective (this would be better to be a property of the camera)

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

			self.displayNodes(wireframe)

			self.displayEdges(wireframe)

			self.displayFaces(wireframe)

	def displayNodes(self, wireframe):

		for node in wireframe.nodes:

			pygame.draw.circle(self.screen, wireframe.nodeColour, (int(node[0]), int(node[1])), wireframe.nodeRadius, 0)

	def displayEdges(self, wireframe):

		for edge in wireframe.edges:

			pygame.draw.aaline(self.screen, wireframe.edgeColour, wireframe.nodes[edge.node1Index][:2], wireframe.nodes[edge.node2Index][:2], 1)

	def displayFaces(self, wireframe):

		for face in wireframe.faces:

			n1, n2, n3 = face.vertices

			pygame.draw.polygon(self.screen, (255,255,255), [wireframe.nodes[n1][:2], wireframe.nodes[n2][:2], wireframe.nodes[n3][:2]], 0)

	def addWireframe(self, name, wireframe):
		self.wireframes[name] = wireframe

	def processKeys(self, keys):

		key_to_function = {

		pygame.K_LEFT: (lambda x: x.rotateAboutCamera('Y', 0.05)),
 		pygame.K_RIGHT:(lambda x: x.rotateAboutCamera('Y', -0.05)),
 		pygame.K_DOWN: (lambda x: x.moveCameraVertically(20)),
 		pygame.K_UP:   (lambda x: x.moveCameraVertically(-20)),

 		pygame.K_w: (lambda x: x.moveCameraHorizontally('Z', 20)),
 		pygame.K_s: (lambda x: x.moveCameraHorizontally('Z', -20)),
 		pygame.K_a: (lambda x: x.moveCameraHorizontally('X', 20)),
 		pygame.K_d: (lambda x: x.moveCameraHorizontally('X', -20)),

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

