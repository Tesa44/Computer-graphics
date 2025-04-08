#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

viewer = [0.0, 0.0, 10.0]

theta_x = 0.0
theta_y = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

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

hidden_face = None  # Ściana do ukrycia: "front", "right", "back", "left" lub None

# Tekstury
default_texture = Image.open("tekstura.tga")
wood_texture = Image.open("drewno.tga")
current_texture = default_texture


def update_texture(texture):
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, texture.size[0], texture.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, texture.tobytes("raw", "RGB", 0, -1)
    )


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

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Ustawienie domyślnej tekstury
    update_texture(current_texture)


def shutdown():
    pass


def render(time):
    global theta_x, theta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta_x += delta_y * pix2angle
        theta_y += delta_x * pix2angle

    glRotatef(theta_x, 1.0, 0.0, 0.0)
    glRotatef(theta_y, 0.0, 1.0, 0.0)

    # Podstawa
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2.5, 0.0, -2.5)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2.5, 0.0, -2.5)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(2.5, 0.0, 2.5)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2.5, 0.0, 2.5)
    glEnd()

    # Ściany boczne
    draw_wall("front", [-2.5, 0.0, -2.5], [0.0, 5.0, 0.0], [2.5, 0.0, -2.5],
              [0.0, 0.0], [0.5, 0.5], [1.0, 0.0])
    draw_wall("right", [2.5, 0.0, -2.5], [0.0, 5.0, 0.0], [2.5, 0.0, 2.5],
              [1.0, 0.0], [0.5, 0.5], [1.0, 1.0])
    draw_wall("back", [2.5, 0.0, 2.5], [0.0, 5.0, 0.0], [-2.5, 0.0, 2.5],
              [1.0, 1.0], [0.5, 0.5], [0.0, 1.0])
    draw_wall("left", [-2.5, 0.0, 2.5], [0.0, 5.0, 0.0], [-2.5, 0.0, -2.5],
              [0.0, 1.0], [0.5, 0.5], [0.0, 0.0])

    glFlush()


def draw_wall(face, v1, v2, v3, tex1, tex2, tex3):
    global hidden_face

    if hidden_face == face:
        return  # Nie rysuj tej ściany

    glBegin(GL_TRIANGLES)
    glTexCoord2f(*tex1)
    glVertex3f(*v1)
    glTexCoord2f(*tex2)
    glVertex3f(*v2)
    glTexCoord2f(*tex3)
    glVertex3f(*v3)
    glEnd()


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
    global hidden_face, current_texture

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if action == GLFW_PRESS:
        if key == GLFW_KEY_1:
            hidden_face = "front" if hidden_face != "front" else None
        elif key == GLFW_KEY_2:
            hidden_face = "right" if hidden_face != "right" else None
        elif key == GLFW_KEY_3:
            hidden_face = "back" if hidden_face != "back" else None
        elif key == GLFW_KEY_4:
            hidden_face = "left" if hidden_face != "left" else None
        elif key == GLFW_KEY_T:  # Zmiana tekstury
            current_texture = wood_texture if current_texture == default_texture else default_texture
            update_texture(current_texture)


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
