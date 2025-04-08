#!/usr/bin/env python3
import sys


#1 - wybór Ambient.
#2 - wybór Diffuse.
#3 - wybór Specular.
#R - wybór składowej Red.
#G - wybór składowej Green.
#B - wybór składowej Blue.
#UP - zwiększenie wartości wybranej składowej o 0.1.
#DOWN - zmniejszenie wartości wybranej składowej o 0.1.




from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

current_component = 0  # 0: ambient, 1: diffuse, 2: specular
current_color_index = 0  # Index for RGB components (0: R, 1: G, 2: B)


def print_current_light_values():
    print(f"Ambient: {light_ambient[:3]}")
    print(f"Diffuse: {light_diffuse[:3]}")
    print(f"Specular: {light_specular[:3]}")


def adjust_light_component(increase):
    global current_component, current_color_index
    step = 0.1 if increase else -0.1

    if current_component == 0:
        light_ambient[current_color_index] = max(0.0, min(1.0, light_ambient[current_color_index] + step))
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    elif current_component == 1:
        light_diffuse[current_color_index] = max(0.0, min(1.0, light_diffuse[current_color_index] + step))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    elif current_component == 2:
        light_specular[current_color_index] = max(0.0, min(1.0, light_specular[current_color_index] + step))
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    print_current_light_values()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    print_current_light_values()


def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global current_component, current_color_index

    if action != GLFW_PRESS:
        return

    if key == GLFW_KEY_ESCAPE:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_1:
        current_component = 0  # Ambient
        print("Selected Ambient")
    elif key == GLFW_KEY_2:
        current_component = 1  # Diffuse
        print("Selected Diffuse")
    elif key == GLFW_KEY_3:
        current_component = 2  # Specular
        print("Selected Specular")
    elif key == GLFW_KEY_R:
        current_color_index = 0  # Red
        print("Selected Red Component")
    elif key == GLFW_KEY_G:
        current_color_index = 1  # Green
        print("Selected Green Component")
    elif key == GLFW_KEY_B:
        current_color_index = 2  # Blue
        print("Selected Blue Component")
    elif key == GLFW_KEY_UP:
        adjust_light_component(True)
    elif key == GLFW_KEY_DOWN:
        adjust_light_component(False)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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
