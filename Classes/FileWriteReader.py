import numpy as np
from Classes.Face import Face
from Classes.Wireframe import Wireframe
from Functions.normaliseVector import getFaceNormal

class FileWriteReader:

	def __init__(self, filename, scaleFactor):

		self.filename = filename
		self.scaleFactor = scaleFactor

		self.nodeArray = []
		self.faceArray = []

		self.vertexNormalArray = []

		self.materialDictionary = {}
		self.processMaterialFile(self.filename[:-3]+'mtl')
		self.processFile()

	def processFile(self):

		fileType = self.filename.split('.')[-1]

		f = open(self.filename, "r")

		for i in f:

			if i[0] == 'v' and i[1] == 't':
				
				pass

			elif i[0] == 'v' and i[1] == 'n':				
				
				i = i.split()
				self.vertexNormalArray.append([(float(i[1])*self.scaleFactor), (float(i[2])*self.scaleFactor), (float(i[3])*self.scaleFactor)])

			elif i[0] == 'v' and i[1] == ' ':

				i = i.split()

				self.nodeArray.append([float(i[1])*self.scaleFactor, float(i[2])*self.scaleFactor, float(i[3])*self.scaleFactor])

			elif i.find('usemtl') != -1:
				
				i = i.split(' ')
				
				material = i[1]

			elif i[0] == 'f':

				i = i.split()
				face = []
				faceVertexNormals = []

				for subsection in i:
					subsections = subsection.split('/')

					if subsection[0] != 'f':

						face.append(subsections[0])
						faceVertexNormals.append(subsections[2])

				if len(face) == 4:
					
					triangle1 = Face((int(face[0])-1, int(face[1])-1, int(face[2])-1), getFaceNormal(self.vertexNormalArray[int(faceVertexNormals[0])-1], self.vertexNormalArray[int(faceVertexNormals[1])-1], self.vertexNormalArray[int(faceVertexNormals[2])-1]), self.materialDictionary[material])
					triangle2 = Face((int(face[2])-1, int(face[3])-1, int(face[0])-1), getFaceNormal(self.vertexNormalArray[int(faceVertexNormals[2])-1], self.vertexNormalArray[int(faceVertexNormals[3])-1], self.vertexNormalArray[int(faceVertexNormals[0])-1]), self.materialDictionary[material])

					self.faceArray.append(triangle1)
					self.faceArray.append(triangle2)

				elif len(face) == 3:

					triangle1 = Face((int(face[0])-1, int(face[1])-1, int(face[2])-1), getFaceNormal(self.vertexNormalArray[int(faceVertexNormals[0])-1], self.vertexNormalArray[int(faceVertexNormals[1])-1], self.vertexNormalArray[int(faceVertexNormals[2])-1]), self.materialDictionary[material])

					self.faceArray.append(triangle1)

				else:
					pass

		f.close()

	def processMaterialFile(self, mtlFileName):

		f = open(mtlFileName, 'r')

		for i in f:
			
			if i.find('newmtl') == 0:
				
				i = i.split(' ')
				materialName = i[-1]

			if i[0] == 'K' and i[1] =='d':
				
				i = i.split(' ')
				r = float(i[1])*255
				g = float(i[2])*255
				b = float(i[3])*255

				self.materialDictionary[materialName] = (r,g,b)

		f.close()

	def createWireframe(self):

		Object = Wireframe()

		Object.addNodes(np.array(self.nodeArray))

		for i in self.faceArray:
			Object.addFaces([i])

		return Object

