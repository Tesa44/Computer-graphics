#!/usr/bin/env python3
import math
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Parametery dla modelu "torus"
N = 50  # Rozdzielczość punktów (u,v)
R = 3.0  # Promień do zewnątrz torusa
r = 1.0  # Promień do środka torusa

colors = np.random.rand(N, N, 3) # Tablica do przetrzymywania kolorów dla każdego wierzchołka
points = np.zeros((N, N, 3)) # Tablica przechowująca współrzędne (x, y, z)
# Funkcja do obliczenia (x, y, z) bazując na parametrach torusa
def calculate_torus_points():
    u_values = np.linspace(0, 1, N)
    v_values = np.linspace(0, 1, N)
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            x = (R + r * np.cos(2 * np.pi * v)) * np.cos(2 * np.pi * u)
            y = (R + r * np.cos(2 * np.pi * v)) * np.sin(2 * np.pi * u)
            z = r * np.sin(2 * np.pi * v)
            points[i][j] = [x, y, z]

def startup():
    update_viewport(None, 600, 600)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    calculate_torus_points()  # Wstępne obliczenie punktów dla modelu torus
def shutdown():
    pass

def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)  # Oś X w kolorze czerwonym
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)  # Oś Y w kolorze zielonym
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)  # Oś Z w kolorze niebieskim
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 1.0, 1.0)  # Rotuj względem osi X, Y,Z

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    angle = time * (180/math.pi)
    spin(angle)
    axes()

    #Rysowanie modelu Torusa za pomocą GL_TRAINGLE_STRIP
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3f(*colors[i][j])
            glVertex3f(*points[i][j])

            glColor3f(*colors[i+1][j])
            glVertex3f(*points[i + 1][j])
        glEnd()

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
        glOrtho(-10.0, 10.0, -10.0 / aspect_ratio, 10.0 / aspect_ratio, -20.0, 20.0)
    else:
        glOrtho(-10.0 * aspect_ratio, 10.0 * aspect_ratio, -10.0, 10.0, -20.0, 20.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(600, 600, __file__, None, None)
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
