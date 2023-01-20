from vec3 import *


class DirectionalLight:

    def __init__(self, direction: Vec3, color: RGB):
        self.direction = direction
        self.color = color

    def direction_unit_vector(self):
        """Returns unit vector of a directional light's direction"""
        return self.direction.unit_vector()

class PointLight:

    def __init__(self, location: Point3, color: RGB, intensity=1.0):
        self.location = location
        self.color = color
        self.intensity = intensity
