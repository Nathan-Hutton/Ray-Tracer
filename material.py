import math

from light import *
from ray import Ray


class Material:

    def __init__(self, color: RGB, ambient_coefficient: float, diffuse_coefficient: float, specular_coefficient: float, exponent: int):
        """ambient_coefficient and diffuse_coefficient should both be between 0 and 1"""
        self.color = color
        self.ambient_coefficient = ambient_coefficient
        self.diffuse_coefficient = diffuse_coefficient
        self.specular_coefficient = specular_coefficient
        self.exponent = exponent

    def shade(self, light: DirectionalLight or PointLight, normal: Vec3, direction: Vec3, intersection_point: Point3, world: list):
        """Changes color variable for material class to represent how a specific pixel should be colored with shading"""

        if type(light) == DirectionalLight:
            vector_to_light = light.direction_unit_vector() * -1
            effective_color = light.color * self.color
        else:
            vector_to_light = light.location - intersection_point
            distance = vector_to_light.length()
            falloff = light.intensity / (distance ** 2)
            intensity_for_intersection = light.color * falloff
            effective_color = (light.color * intensity_for_intersection) * self.color

            vector_to_light = (light.location - intersection_point).unit_vector()

        ambient_component = effective_color * self.ambient_coefficient
        normal_dot_light = normal.unit_vector().dot(vector_to_light)
        reflected_vector = (normal * normal.dot(vector_to_light) * 2) - vector_to_light
        adjusted_point = intersection_point + (normal * 0.01)
        shadow_ray = Ray(adjusted_point, vector_to_light)

        # Object facing away from light
        if normal_dot_light < 0:
            return RGB(0, 0, 0) + ambient_component

        # Object in shadow
        for hittable in world:
            if hittable.shadow_hit(shadow_ray):
                return RGB(0, 0, 0) + ambient_component

        # Object in light
        reflected_dot_direction = reflected_vector.dot(direction * -1)
        if reflected_dot_direction < 0:
            specular = 0
        else:
            specular = effective_color * self.specular_coefficient * pow(reflected_dot_direction, self.exponent)

        diffuse = effective_color * self.diffuse_coefficient * normal_dot_light
        return ambient_component + diffuse + specular
