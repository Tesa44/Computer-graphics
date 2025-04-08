#!/usr/bin/env python3
import math
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


N = 50 
points = np.zeros((N, N, 3))  


def calculate_egg_points():
    u_values = np.linspace(0, 1, N)
    v_values = np.linspace(0, 1, N)
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
           
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.cos(np.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5 
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.sin(np.pi * v)
            points[i][j] = [x, y, z]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)  
    glEnable(GL_DEPTH_TEST)  
    calculate_egg_points()  

def shutdown():
    pass

# Funkcja do rysowania osi X, Y, Z
def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)  # Oś X w kolorze czerwonym
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)  # # Oś Y w kolorze zielonym
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)  # # Oś Z w kolorze niebieskim
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

# Funkcja do obracania obiektów
def spin(angle):
    glRotatef(angle, 1.0, 1.0, 1.0)  # Obracaj po osi X, Y, Z

# Funkcja renderowania
def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Wyczyść bufor i kolor
    glLoadIdentity()


    angle = time * (180/math.pi)
    spin(angle)
    axes()
    glColor3f(1.0, 1.0, 0.0)  
    glBegin(GL_LINES)
    
    for i in range(N - 1):
        for j in range(N):
            glVertex3f(*points[i][j])
            glVertex3f(*points[i + 1][j])
 
    for i in range(N):
        for j in range(N - 1):
            glVertex3f(*points[i][j])
            glVertex3f(*points[i][j + 1])
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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Main function
def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "3D Egg Model", None, None)
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
