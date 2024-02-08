import math
from random import randint

def normaliseVector(vector):

	magnitude = math.sqrt((vector[0]**2)+(vector[1]**2)+(vector[2]**2))

	if magnitude == 0:

		return [0,0,0]

	else:

		return vectorDivide(vector, magnitude)

def dotProduct(vector1, vector2):

	return (vector1[0]*vector2[0])+(vector1[1]*vector2[1])+(vector1[2]*vector2[2])

def vectorSubtract(vector1, vector2):

	return [vector1[0] - vector2[0], vector1[1]-vector2[1], vector1[2]-vector2[2]]

def vectorAdd(vector1, vector2):

	return [vector1[0] + vector2[0], vector1[1] + vector2[1], vector1[2] + vector2[2]]

def crossProduct(vector1, vector2):

	output = [None, None, None]

	output[0] = (vector1[1]*vector2[2]) - (vector1[2]*vector2[1])
	output[1] = (vector1[2]*vector2[0]) - (vector1[0]*vector2[2])
	output[2] = (vector1[0]*vector2[1]) - (vector1[1]*vector2[0])

	return output

def vectorMultiply(vector, scalar):

	output = [None, None, None]

	output[0] = vector[0] * scalar
	output[1] = vector[1] * scalar
	output[2] = vector[2] * scalar

	return output

def vectorDivide(vector, scalar):

	output = [None, None, None]

	output[0] = vector[0] / scalar
	output[1] = vector[1] / scalar
	output[2] = vector[2] / scalar

	return output

def sortFaces(trianglePointsList):
	
	trianglePointsList.sort(key=sortKey, reverse=True)

def sortKey(inputs):

	return (addPerspectiveToNode(inputs[0])[2] + addPerspectiveToNode(inputs[1])[2] + addPerspectiveToNode(inputs[2])[2])/3.0

def sortWireframes(wireframesDictionary):

	wireframesList = list(wireframesDictionary.values())

	wireframesList.sort(key=sortWireframesKey, reverse=True)

def sortWireframesKey(inputs):

	if int(len(inputs.nodes)/3) == 0:

		numberOfApproximationPoints = 1

	else:

		numberOfApproximationPoints = int(len(inputs.nodes)/3)

	return approximateCentroid(inputs,numberOfApproximationPoints)[2]

def calculateTriangleCenter(n1, n2, n3):

	center = vectorDivide(vectorAdd(vectorAdd(n1, n2), n3), 3.0)

	return center

def calculateFaceNormal(n1, n2, n3):

	faceNormal = [None, None, None]

	vectorU = vectorSubtract(n2, n1)
	vectorV = vectorSubtract(n3, n1)

	faceNormal = crossProduct(vectorU, vectorV)
	faceNormal = normaliseVector(faceNormal)

	return faceNormal

def clamp(value, minValue, maxValue):
		return max(min(value, maxValue), minValue)

def addPerspectiveToNode(node):

		perspectiveNode = node.copy()
		pNode = perspectiveNode
		center = [1200/2, 1000/2]

		if (250-node[2]) != 0:

			pNode[0] = (center[0] + (node[0]-center[0])*250/(250-(node[2])))
			pNode[1] = (center[1] + (node[1]-center[1])*250/(250-(node[2])))
			pNode[2] = node[2] * 1

		return pNode

def approximateCentroid(wireframe, numberOfApproximationPoints):

	output = [0, 0, 0]
	usedRandomIndices = []
	randomIndex  = randint(0,len(wireframe.nodes)-1)

	for i in range(0,numberOfApproximationPoints-1):

		while randomIndex in usedRandomIndices:
			
			randomIndex = randint(0,len(wireframe.nodes)-1)

		else:

			usedRandomIndices.append(randomIndex)
			output[0] += wireframe.nodes[randomIndex][0]
			output[1] += wireframe.nodes[randomIndex][1]
			output[2] += wireframe.nodes[randomIndex][2]

	output = vectorDivide(output, numberOfApproximationPoints)

	return output



