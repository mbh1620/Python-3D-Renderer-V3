import numpy as np
from Classes.Face import Face
from Classes.Wireframe import Wireframe

class FileWriteReader:

	def __init__(self, filename, scaleFactor):

		self.filename = filename
		self.scaleFactor = scaleFactor

		self.nodeArray = []
		self.faceArray = []

		self.processFile()


	def processFile(self):

		#Work out the file type

		fileType = self.filename.split('.')[-1]

		f = open(self.filename, "r")

		print(f)

		for i in f:

			if i[0] == 'v' and i[1] == 't':
				#
				pass

			elif i[0] == 'v' and i[1] == 'n':
				#Process the vertex normal
				pass

			elif i[0] == 'v' and i[1] == ' ':

				#Create a node

				i = i.split()

				self.nodeArray.append([float(i[1])*self.scaleFactor, float(i[2])*self.scaleFactor, float(i[3])*self.scaleFactor])

			elif i[0] == 'f':

				i = i.split()
				face = []

				for subsection in i:
					subsections = subsection.split('/')

					if subsection[0] != 'f':
						face.append(subsections[0])

				if len(face) == 4:
					#reduce the quad down into two triangles
					triangle1 = Face((int(face[0])-1, int(face[1])-1, int(face[2])-1), [0,0,0], [])
					triangle2 = Face((int(face[2])-1, int(face[3])-1, int(face[0])-1), [0,0,0], [])


					self.faceArray.append(triangle1)
					self.faceArray.append(triangle2)

				elif len(face) == 3:

					triangle1 = Face((int(face[0])-1, int(face[1])-1, int(face[2])-1), [0,0,0], [])

					self.faceArray.append(triangle1)

				else:
					pass

		f.close()

	def createWireframe(self):

		Object = Wireframe()

		Object.addNodes(np.array(self.nodeArray))

		for i in self.faceArray:
			Object.addFaces([i])

		return Object






