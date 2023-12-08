class Camera:

	def __init__(self, position, horizontalAngle, verticalAngle, fieldOfView=250, zoom=500, projectionType='orthographic'):

		self.position = position
		self.horizontalAngle = horizontalAngle
		self.verticalAngle = verticalAngle
		self.fieldOfView = fieldOfView
		self.zoom = zoom
		self.projectionType = projectionType
