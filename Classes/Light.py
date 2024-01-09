
class Light:

	def __init__(self, position, intensity=0.5, colour=[1,1,1]):

		self.position = position
		self.intensity = intensity
		self.colour = colour

class OmniDirectionalLight(Light):

	def __init__(self):

		pass

class DirectionalLight(Light):

	def __init__(self, directionVector):

		pass