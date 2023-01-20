from material import *
import math
from shape import Shape


def rotate_along_x(vertex, radians):
    y_coordinate = vertex.y * math.cos(radians) - vertex.z * math.sin(radians)
    z_coordinate = vertex.y * math.sin(radians) + vertex.z * math.cos(radians)

    return Vec3(vertex.x, y_coordinate, z_coordinate)


def rotate_along_y(vertex, radians):
    x_coordinate = vertex.x * math.cos(radians) + vertex.z * math.sin(radians)
    z_coordinate = (vertex.x * -1) * math.sin(radians) + vertex.z * math.cos(radians)

    return Vec3(x_coordinate, vertex.y, z_coordinate)


def rotate_along_z(vertex, radians):
    x_coordinate = vertex.x * math.cos(radians) - vertex.y * math.sin(radians)
    y_coordinate = vertex.x * math.sin(radians) + vertex.y * math.cos(radians)

    return Vec3(x_coordinate, y_coordinate, vertex.z)


class TriangleMesh(Shape):

    def __init__(self, obj_file_name, material):
        self.obj_file_name = obj_file_name
        self.material = material
        self.vertices = []
        self.normals = []
        self.triangle_normals = []
        self.triangles = []
        self.read_obj_file()

    def read_obj_file(self):
        """Sets up instance variables for TriangleMesh object"""
        fp = open(self.obj_file_name, "r")
        all_lines = fp.readlines()
        fp.close()

        for line in all_lines:
            values = line.split()
            # only process lines that contain vertices, normals, and faces
            if len(values) > 3:
                if values[0] == 'v':
                    self.vertices.append(Vec3(float(values[1]), float(values[2]), float(values[3])))
                elif values[0] == 'vn':
                    self.normals.append(Vec3(float(values[1]), float(values[2]), float(values[3])))
                elif values[0] == 'f':
                    v = []  # vertex numbers
                    if '/' in line:
                        n = []  # normals
                        # ignoring textures
                        for i in range(1, 4):
                            face = values[i].split('/')
                            v.append(int(face[0]) - 1)  # modify vertex number so first is in 0
                            if len(face[2]):
                                n.append((int(face[2])) - 1)  # modify normal number so first is 0
                        self.triangle_normals.append((n[0], n[1], n[2]))
                    else:
                        for i in range(1, 4):
                            v.append(int(values[i]) - 1)  # modify vertex number so first is in 0
                    self.triangles.append((v[0], v[1], v[2]))

    def hit(self, ray, t_min=0, t_max=math.inf):
        """Returns triangle one of mesh that intercepts with a ray closest to the origin of the ray"""
        closest_triangle = (False, )
        for i in range(len(self.triangles)):
            if self.triangle_normals:
                intersection = self.get_intersection(ray, self.triangles[i], self.triangle_normals[i])
            else:
                intersection = self.get_intersection(ray, self.triangles[i], None)
            if intersection[0] and t_max > intersection[1] >= t_min:
                t_max = intersection[1]
                closest_triangle = intersection
        return closest_triangle

    def shadow_hit(self, shadow_ray, t_min=0, t_max=math.inf):
        """Returns true if a ray hits an object. Used for shadows"""
        for triangle in self.triangles:
            intersection = self.get_shadow_intersection(shadow_ray, triangle)
            if intersection[0] and t_max > intersection[1] >= t_min:
                return True

    def get_intersection(self, ray, triangle, triangle_normals):
        """Returns intersection point of a specific triangle and ray if one exists"""
        a = self.vertices[int(triangle[0])]
        b = self.vertices[int(triangle[1])]
        c = self.vertices[int(triangle[2])]
        ab = b - a
        ac = c - a

        # Get alpha and beta values:
        A = a.x-b.x
        B = a.x-c.x
        C = ray.direction.x
        D = a.x - ray.origin.x
        E = a.y-b.y
        F = a.y-c.y
        G = ray.direction.y
        H = a.y-ray.origin.y
        I = a.z-b.z
        J = a.z-c.z
        K = ray.direction.z
        L = a.z-ray.origin.z

        try:
            alpha = (D*(F*K-G*J)+B*(G*L-H*K)+C*(H*J-F*L)) / (A*(F*K-G*J)+B*(G*I-E*K)+C*(E*J-F*I))
            beta = (A*(H*K-G*L)+D*(G*I-E*K)+C*(E*L-H*I)) / (A*(F*K-G*J)+B*(G*I-E*K)+C*(E*J-F*I))
        except ZeroDivisionError:
            return (False,)
        gamma = 1 - (alpha + beta)


        # Intersection point isn't in the triangle
        if alpha < 0 or beta < 0 or alpha + beta > 1:
            return (False, )

        if not triangle_normals:
            # surface unit normal
            normal = ab.cross(ac).unit_vector()
        else:
            # interpolated unit normal (using vertex normals)
            a_normal = self.normals[triangle_normals[0]]
            b_normal = self.normals[triangle_normals[1]]
            c_normal = self.normals[triangle_normals[2]]
            normal = (a_normal * alpha) + (b_normal * beta) + (c_normal * gamma)

        # Calculate t and point of intersection (assuming a triangle collision)
        t = (A*(F*L-H*J)+B*(H*I-E*L)+D*(E*J-F*I)) / (A*(F*K-G*J)+B*(G*I-E*K)+C*(E*J-F*I))
        p = ray.at(t)

        return True, t, normal, self.material, p

    def get_shadow_intersection(self, ray, triangle):
        """Returns a tuple which contains True and t if a ray hits a triangle. Used for shadows"""
        a = self.vertices[int(triangle[0])]
        b = self.vertices[int(triangle[1])]
        c = self.vertices[int(triangle[2])]

        # Get alpha and beta values:
        A = a.x - b.x
        B = a.x - c.x
        C = ray.direction.x
        D = a.x - ray.origin.x
        E = a.y - b.y
        F = a.y - c.y
        G = ray.direction.y
        H = a.y - ray.origin.y
        I = a.z - b.z
        J = a.z - c.z
        K = ray.direction.z
        L = a.z - ray.origin.z

        try:
            alpha = (D * (F * K - G * J) + B * (G * L - H * K) + C * (H * J - F * L)) / (
                        A * (F * K - G * J) + B * (G * I - E * K) + C * (E * J - F * I))
            beta = (A * (H * K - G * L) + D * (G * I - E * K) + C * (E * L - H * I)) / (
                        A * (F * K - G * J) + B * (G * I - E * K) + C * (E * J - F * I))
        except ZeroDivisionError:
            return (False,)

        if alpha < 0 or beta < 0 or alpha + beta > 1:
            return (False,)

        t = (A*(F*L-H*J)+B*(H*I-E*L)+D*(E*J-F*I)) / (A*(F*K-G*J)+B*(G*I-E*K)+C*(E*J-F*I))
        return True, t

    def translate(self, x_translation, y_translation, z_translation):
        translation_vector = Vec3(x_translation, y_translation, z_translation)
        for i in range(len(self.vertices)):
            vertex = self.vertices[i]
            vertex += translation_vector
            self.vertices[i] = vertex

    def rotate(self, x_degrees, y_degrees, z_degrees):
        x_radians = math.radians(x_degrees)
        y_radians = math.radians(y_degrees)
        z_radians = math.radians(z_degrees)

        for i in range(len(self.vertices)):
            vertex = self.vertices[i]
            vertex = rotate_along_x(vertex, x_radians)
            vertex = rotate_along_y(vertex, y_radians)
            vertex = rotate_along_z(vertex, z_radians)
            self.vertices[i] = vertex

    def scale(self, x_scale, y_scale, z_scale):
        scale_vector = Vec3(x_scale, y_scale, z_scale)
        for i in range(len(self.vertices)):
            vertex = self.vertices[i]
            vertex *= scale_vector
            self.vertices[i] = vertex
