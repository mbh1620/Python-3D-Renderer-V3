import math

def normaliseVector(vector):

	magnitude = math.sqrt((vector[0]**2)+(vector[1]**2)+(vector[2]**2))

	return [vector[0]/magnitude, vector[1]/magnitude, vector[2]/magnitude]

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

	return (inputs[0][2] + inputs[1][2] + inputs[2][2])/3.0

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

def getFaceNormal(vertexNormalA, vertexNormalB, vertexNormalC):

	averagedVertexNormal = calculateTriangleCenter(vertexNormalA, vertexNormalB, vertexNormalC)

	averagedVertexNormalX = averagedVertexNormal[0]
	averagedVertexNormalY = averagedVertexNormal[1]
	averagedVertexNormalZ = averagedVertexNormal[2]

	denominator = math.sqrt((averagedVertexNormalX**2) + (averagedVertexNormalY**2) + (averagedVertexNormalZ**2))

	averagedVertexNormal = vectorDivide(averagedVertexNormal, denominator)

	return averagedVertexNormal

def clamp(value, minValue, maxValue):
		return max(min(value, maxValue), minValue)



