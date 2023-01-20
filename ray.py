from vec3 import *
import math


class Ray:

    def __init__(self, origin: Point3, direction: Vec3):
        self.origin = origin
        self.direction = direction

    def at(self, time):
        """Returns position of a ray based on t (time)"""
        return self.origin + (self.direction * time)

    def ray_color(self, world, light_list):
        """Takes a list of objects and lights and decides color of pixel for ray"""
        t_min = 0
        t_max = math.inf
        normal = None
        hit_object = None
        intersection_point = None

        # Get object hit by ray
        for obj in world:
            hit_value = obj.hit(self, t_min, t_max)
            if hit_value[0] and hit_value[1] < t_max:
                normal = hit_value[2]
                t_max = hit_value[1]
                hit_object = obj
                intersection_point = hit_value[4]

        # Add light to hit object
        color = RGB(0, 0, 0)
        if hit_object:
            for light in light_list:
                color += hit_object.material.shade(light, normal, self.direction, intersection_point, world)
            color.clamp_color()

        return color
