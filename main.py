from sphere import *
from triangleMesh import *

# Nathan Hutton

def make_image():
    # image
    aspect_ratio = 16/9
    image_width = 400
    image_height = int(image_width / aspect_ratio)

    #camera
    viewport_height = 2
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1

    # origin = Point3(0, .75, 4)  # for sphere
    origin = Point3(-1, 0.5, 2.5)  # for gourd
    # origin = Point3(0, 0, 2)  # for custom scene
    horizontal = Vec3(viewport_width, 0, 0)
    vertical = Vec3(0, viewport_height, 0)
    lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0, 0, focal_length)

    # objects and lights
    world = []
    lights = []
    gourd = TriangleMesh("gourd.obj", Material(RGB(1, 0, 1), .1, .7, .8, 15))
    # cube = TriangleMesh("cube.obj", Material(RGB(1, 0, 0.5), .2, .9, .8, 15))
    # dodecahedron = TriangleMesh("dodecahedron.obj", Material(RGB(1, 0.5, 0), .2, .9, .8, 15))
    # cube.translate(0.3, -1, 0)
    # cube.rotate(0, 45, 45)
    # cube.scale(1, 1, 2)
    # dodecahedron.translate(-1.5, -0.3, 0)
    # dodecahedron.rotate(-40, -50, -60)
    # dodecahedron.scale(1.5, 1.5, 1.5)
    # world.append(cube)
    # world.append(dodecahedron)
    world.append(gourd)
    lights.append(DirectionalLight(Vec3(0, -1, -0.3), RGB(1, 1, 1)))
    lights.append(DirectionalLight(Vec3(-1, 0, -1), RGB(1, 1, 1)))
    # lights.append(DirectionalLight(Vec3(0.5, 0, -1), RGB(1, 1, 1)))
    # lights.append(PointLight(Vec3(0, 0, 1), RGB(1, 1, 1)))

    # Render
    outfile = open(f'gourd.ppm', 'w')
    outfile.write(f'P3\n{image_width} {image_height}\n255\n')
    for i in reversed(range(image_height)):
        for j in range(image_width):
            u = j / (image_width-1)
            v = i / (image_height-1)
            r = Ray(origin, lower_left_corner + horizontal*u + vertical*v - origin)
            color_pixel = r.ray_color(world, lights)
            write_color(outfile, color_pixel)


if __name__ == "__main__":
    make_image()
