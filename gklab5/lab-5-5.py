#!/usr/bin/env python3
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math


N = 50
points = np.zeros((N, N, 3))
normals = np.zeros((N, N, 3))
colors = np.zeros((N, N, 3))


viewer = [0.0, 0.0, 60.0]
theta = 0.0
phi = 0.0
pix2angle = 1.0
left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0


light_theta = 0.0
light_phi = 0.0
light_radius = 20.0


show_normals = False


def calculate_egg_points():
    u_vals = np.linspace(0, 1, N)
    v_vals = np.linspace(0, 1, N)
    for i, u in enumerate(u_vals):
        for j, v in enumerate(v_vals):
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.cos(np.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.sin(np.pi * v)
            points[i, j] = [x, y, z]
            colors[i, j] = [random.random(), random.random(), random.random()]

    points[:, -1] = points[:, 0]
    colors[:, -1] = colors[:, 0]

def calculate_normals():
    for i in range(N):
        for j in range(N):
            u = points[(i + 1) % N, j] - points[i - 1, j]
            v = points[i, (j + 1) % N] - points[i, j - 1]
            normal = np.cross(u, v)
            normal_length = np.linalg.norm(normal)
            if normal_length != 0:
                normal /= normal_length

            if i >= N // 2:
                normal = -normal
            normals[i, j] = normal

    normals[:, -1] = normals[:, 0]


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = 50.0
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)


    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    calculate_egg_points()
    calculate_normals()


def render(time):
    global theta, phi, light_theta, light_phi, show_normals

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()


    r = 60.0
    x = r * math.cos(math.radians(phi)) * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(phi))
    z = r * math.cos(math.radians(phi)) * math.sin(math.radians(theta))

    gluLookAt(x, y, z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


    light_x = light_radius * math.cos(math.radians(light_phi)) * math.cos(math.radians(light_theta))
    light_y = light_radius * math.sin(math.radians(light_phi))
    light_z = light_radius * math.cos(math.radians(light_phi)) * math.sin(math.radians(light_theta))
    glLightfv(GL_LIGHT0, GL_POSITION, [light_x, light_y, light_z, 1.0])


    glPushMatrix()
    glTranslatef(light_x, light_y, light_z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glColor3f(1.0, 1.0, 0.0)
    gluSphere(quadric, 0.5, 10, 10)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):

            glNormal3f(*normals[i, j])
            glColor3f(*colors[i, j])
            glVertex3f(*points[i, j])

            glNormal3f(*normals[i + 1, j])
            glColor3f(*colors[i + 1, j])
            glVertex3f(*points[i + 1, j])

            glNormal3f(*normals[i, j + 1])
            glColor3f(*colors[i, j + 1])
            glVertex3f(*points[i, j + 1])

            glNormal3f(*normals[i + 1, j])
            glColor3f(*colors[i + 1, j])
            glVertex3f(*points[i + 1, j])

            glNormal3f(*normals[i + 1, j + 1])
            glColor3f(*colors[i + 1, j + 1])
            glVertex3f(*points[i + 1, j + 1])

            glNormal3f(*normals[i, j + 1])
            glColor3f(*colors[i, j + 1])
            glVertex3f(*points[i, j + 1])
    glEnd()

    if show_normals:
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                start = points[i, j]
                end = start + normals[i, j] * 2
                glVertex3f(*start)
                glVertex3f(*end)
        glEnd()

    glFlush()

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height if height else 1, 1.0, 200.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def mouse_motion_light_callback(window, x_pos, y_pos):
    global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old, light_theta, light_phi

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos

    light_theta += delta_x * pix2angle
    light_phi -= delta_y * pix2angle
    light_phi = max(-89.0, min(89.0, light_phi))  # Limit light_phi to avoid gimbal lock


def keyboard_callback(window, key, scancode, action, mods):
    global show_normals
    if key == GLFW_KEY_N and action == GLFW_PRESS:
        show_normals = not show_normals


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetCursorPosCallback(window, mouse_motion_light_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetKeyCallback(window, keyboard_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())

        global theta, phi
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi -= delta_y * pix2angle
            phi = max(-89.0, min(89.0, phi))

        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()
 
if __name__ == "__main__":
    main()
