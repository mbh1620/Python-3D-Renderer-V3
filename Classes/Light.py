
class Light:

	def __init__(self, position, intensity=0.5):

		self.position = position
		self.intensity = intensity

class OmniDirectionalLight(Light):

	def __init__(self):

		pass

class DirectionalLight(Light):

	def __init__(self, directionVector):

		pass