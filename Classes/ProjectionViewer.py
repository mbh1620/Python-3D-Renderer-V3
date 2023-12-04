
import pygame
import numpy as np
from Classes.Face import Face
from Classes.Camera import Camera

class ProjectionViewer:

	def __init__(self, width, height, centerPoint):

		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('3D Renderer')

		self.viewType = 'orthographic' #Can be orthographic or perspective

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

		pass

	def addWireframe(self, name, wireframe):
		self.wireframes[name] = wireframe

	def processKeys(self, keys):

		key_to_function = {

		pygame.K_LEFT: (lambda x: x.rotateAboutCamera()),
 		pygame.K_RIGHT:(lambda x: x.rotateAboutCamera()),
 		pygame.K_DOWN: (lambda x: x.moveCameraUp()),
 		pygame.K_UP:   (lambda x: x.moveCameraDown()),

 		pygame.K_w: (lambda x: x.moveCameraForward(20)),
 		pygame.K_s: (lambda x: x.moveCameraBackward(20)),
 		pygame.K_a: (lambda x: x.moveCameraLeft(20)),
 		pygame.K_d: (lambda x: x.moveCameraRight(20)),

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

	def rotateAboutCamera(self):
		pass
