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

def sortFaces(trianglePointsList):
	
	trianglePointsList.sort(key=sortKey, reverse=True)

def sortKey(inputs):

	return (inputs[0][2] + inputs[1][2] + inputs[2][2])/3.0


