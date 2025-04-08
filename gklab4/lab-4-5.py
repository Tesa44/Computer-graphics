#!/usr/bin/env python3
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, radians, fmod

viewer = [0.0, 0.0, 10.0]  # Camera position
look_at = [0.0, 0.0, -1.0]  # Direction the camera is looking at
up_vector = [0.0, 1.0, 0.0]  # Up direction

theta = 0.0  # Horizontal rotation angle
phi = 0.0  # Vertical rotation angle

mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

movement_speed = 0.1
left_mouse_button_pressed = False


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)

    # Drawing the teapot-like object
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    target = [viewer[0] + look_at[0], viewer[1] + look_at[1], viewer[2] + look_at[2]]

    # Prevent invalid camera settings
    if np.linalg.norm(look_at) < 1e-6:
        print("Invalid look_at vector detected!")
        look_at[0], look_at[1], look_at[2] = 0.0, 0.0, -1.0

    gluLookAt(viewer[0], viewer[1], viewer[2], target[0], target[1], target[2], up_vector[0], up_vector[1], up_vector[2])

    axes()
    example_object()
    glFlush()


def update_viewport(window, width, height):
    """
    Ustawia macierz projekcji, aby proporcje obiektów były zachowane
    przy dowolnym rozmiarze okna.
    """
    global pix2angle_x, pix2angle_y
    if height == 0:
        height = 1  # Zapobieganie dzieleniu przez zero
    aspect_ratio = width / height
    pix2angle_x = 360.0 / width
    pix2angle_y = 360.0 / height

    glViewport(0, 0, width, height)  # Całe okno jako viewport
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(75, aspect_ratio, 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global viewer, look_at
    direction = np.array(look_at)
    right_vector = np.cross(direction, np.array(up_vector))
    right_vector /= np.linalg.norm(right_vector)

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_W:
            viewer[0] += direction[0] * movement_speed
            viewer[1] += direction[1] * movement_speed
            viewer[2] += direction[2] * movement_speed
        elif key == GLFW_KEY_S:
            viewer[0] -= direction[0] * movement_speed
            viewer[1] -= direction[1] * movement_speed
            viewer[2] -= direction[2] * movement_speed
        elif key == GLFW_KEY_A:
            viewer[0] -= right_vector[0] * movement_speed
            viewer[1] -= right_vector[1] * movement_speed
            viewer[2] -= right_vector[2] * movement_speed
        elif key == GLFW_KEY_D:
            viewer[0] += right_vector[0] * movement_speed
            viewer[1] += right_vector[1] * movement_speed
            viewer[2] += right_vector[2] * movement_speed


mouse_sensitivity = 0.9

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old, theta, phi, look_at

    if left_mouse_button_pressed:
        delta_x = x_pos - mouse_x_pos_old
        delta_y = y_pos - mouse_y_pos_old

        theta = fmod(theta + delta_x * mouse_sensitivity, 360.0)
        phi -= delta_y * mouse_sensitivity
        phi = max(-89.0, min(89.0, phi))

        look_at[0] = cos(radians(phi)) * sin(radians(theta))
        look_at[1] = sin(radians(phi))
        look_at[2] = cos(radians(phi)) * cos(radians(theta))

    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos



def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, mouse_x_pos_old, mouse_y_pos_old
    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            left_mouse_button_pressed = True
            mouse_x_pos_old, mouse_y_pos_old = glfwGetCursorPos(window)
        elif action == GLFW_RELEASE:
            left_mouse_button_pressed = False


def main():
    if not glfwInit():
        sys.exit(-1)
    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
