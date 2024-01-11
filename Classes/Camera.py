class Camera:

	def __init__(self, position, horizontalAngle, verticalAngle, projectionViewer, fieldOfView=250, zoom=250, projectionType='orthographic'):

		self.position = position
		self.horizontalAngle = horizontalAngle
		self.verticalAngle = verticalAngle
		self.fieldOfView = fieldOfView
		self.zoom = zoom
		self.projectionType = projectionType
		self.projectionViewer = projectionViewer

	def LEFT(self):
		
		self.projectionViewer.rotateAboutCamera('Y', 0.05)

	def RIGHT(self):
		
		self.projectionViewer.rotateAboutCamera('Y', -0.05)

	def DOWN(self):
		
		self.projectionViewer.moveCameraVertically(20)

	def UP(self):
		
		self.projectionViewer.moveCameraVertically(-20)

	def W(self):
		
		self.projectionViewer.moveCameraHorizontally('Z', -20)

	def S(self):
		
		self.projectionViewer.moveCameraHorizontally('Z', 20)

	def A(self):
		
		self.projectionViewer.moveCameraHorizontally('X', -20)
	
	def D(self):
		
		self.projectionViewer.moveCameraHorizontally('X', 20)
