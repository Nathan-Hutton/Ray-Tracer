from shape import *
from material import *


class Sphere(Shape):

    def __init__(self, center: Point3, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min=0, t_max=math.inf):
        oc = ray.origin - self.center # Vector to center of sphere
        a = ray.direction.length_squared()
        half_b = oc.dot(ray.direction) # Float
        c = oc.length_squared() - pow(self.radius, 2)

        discriminant = pow(half_b, 2) - a * c
        if discriminant < 0:
            return (False, )
        sqrtd = math.sqrt(discriminant)

        # Find the nearest root in acceptable range
        root = (-half_b - sqrtd) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrtd) / a
            if root < t_min or root > t_max:
                return (False, )
        t = root
        p = ray.at(root)
        normal = (p - self.center) / self.radius

        return (True, t, normal, self.material, p)

    def shadow_hit(self, ray, t_min=0, t_max=math.inf):
        oc = ray.origin - self.center  # Vector to center of sphere
        a = ray.direction.length_squared()
        half_b = oc.dot(ray.direction)  # Float
        c = oc.length_squared() - pow(self.radius, 2)

        discriminant = pow(half_b, 2) - a * c
        if discriminant < 0:
            return (False,)
        sqrtd = math.sqrt(discriminant)

        # Find the nearest root in acceptable range
        root = (-half_b - sqrtd) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrtd) / a
            if root < t_min or root > t_max:
                return (False,)

        return (True,)

    def translate(self, x_translation, y_translation, z_translation):
        self.center += Vec3(x_translation, y_translation, z_translation)

    def scale(self, scaler):
        self.radius *= scaler
