import math


class Vec3:

    def __init__(self, x, y, z):
        """A tuple used to store coordinates that can represent vectors, points, or colors"""
        self.coordinates = [x, y, z]
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        """Returns scalar product of 2 vectors"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Returns perpendicular vector of 2 vectors. Used to multiply vectors"""
        return Vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def unit_vector(self):
        return self / self.length()

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2)

    def clamp_color(self):
        self.x = min(1, self.x)
        self.y = min(1, self.y)
        self.z = min(1, self.z)

    def cast_to_int(self):
        self.x = int(self.x * 255)
        self.y = int(self.y * 255)
        self.z = int(self.z * 255)

    def __add__(self, other):
        if type(other) != Vec3:
            return Vec3(self.x + other, self.y + other, self.z + other)
        else:
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if type(other) != Vec3:
            return Vec3(self.x - other, self.y - other, self.z - other)
        else:
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if type(other) != Vec3:
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):
        if type(other) != Vec3:
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __iadd__(self, other):
        if type(other) != Vec3:
            self.x += other
            self.y += other
            self.z += other
        else:
            self.x += other.x
            self.y += other.y
            self.z += other.z
        return Vec3(self.x, self.y, self.z)

    def __isub__(self, other):
        if type(other) != Vec3:
            self.x -= other
            self.y -= other
            self.z -= other
        else:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        return Vec3(self.x, self.y, self.z)

    def __imul__(self, other):
        if type(other) != Vec3:
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        return Vec3(self.x, self.y, self.z)

    def __itruediv__(self, other):
        if type(other) != Vec3:
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        return Vec3(self.x, self.y, self.z)

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


def write_color(file, color: Vec3):
    color.cast_to_int()
    file.write(str(color) + '\n')


RGB = Vec3
Point3 = Vec3
