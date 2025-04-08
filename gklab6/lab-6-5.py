#!/usr/bin/env python3
import math
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

N = 50  # Liczba punktów
points = np.zeros((N, N, 3))  # Punkty jajka
texture_coords = np.zeros((N, N, 2))  # Współrzędne tekstury

def calculate_egg_points():
        u_values = np.linspace(0, 1, N)
        v_values = np.linspace(0, 1, N)
        for i, u in enumerate(u_values):
            for j, v in enumerate(v_values):
                x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.cos(np.pi * v)
                y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
                z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.sin(np.pi * v)
                points[i][j] = [x, y, z]

                u = i / (N - 1)  # Współrzędne tekstury (odbicie na połowie sfery)
                v = j / (N - 1)
                texture_coords[i][j] = [u if u <= 0.5 else 1 - u, v]  # Odbicie

def draw_egg():
    """Rysuje sferę z teksturą."""
    glBegin(GL_QUADS)
    for i in range(N - 1):
        for j in range(N - 1):
            for k in [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]:
                u, v = texture_coords[k[0]][k[1]]
                x, y, z = points[k[0]][k[1]]
                glTexCoord2f(u, v)
                glVertex3f(x, y, z)
    glEnd()

# Mapowanie tekstury

def load_texture():
    # glEnable(GL_TEXTURE_2D)
    # glEnable(GL_CULL_FACE)
    # glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #
    # image = Image.open("drewno.tga")
    # glTexImage2D(
    #     GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0,
    #     GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    # )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    image = Image.open("tekstura.tga")
    image_data = image.tobytes("raw", "RGB", 0, -1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    calculate_egg_points()
    load_texture()

def shutdown():
    pass

def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)  # X
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)  # Y
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)  # Z
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 5, 15, 0, 0, 0, 0, 1, 0)

    # glRotatef(time * 30 % 360, 1.0, 1.0, 1.0)
    glRotatef(time * 50, 0.0, 1.0, 0.0)
    # axes()
    draw_egg()

    # glEnable(GL_TEXTURE_2D)

    # glBegin(GL_QUADS)
    # for i in range(N - 1):
    #     for j in range(N - 1):
    #         # Punkt 1
    #         glTexCoord2f(*texture_coords[i][j])
    #         glVertex3f(*points[i][j])
    #         # Punkt 2
    #         glTexCoord2f(*texture_coords[i + 1][j])
    #         glVertex3f(*points[i][j+1])
    #         # Punkt 3
    #         glTexCoord2f(*texture_coords[i + 1][j + 1])
    #         glVertex3f(*points[i + 1][j + 1])
    #         # Punkt 4
    #         glTexCoord2f(*texture_coords[i][j + 1])
    #         glVertex3f(*points[i+1][j])
    # glEnd()

    glFlush()

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "3D Egg with Texture", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
