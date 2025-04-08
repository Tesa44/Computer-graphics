#!/usr/bin/env python3
import math
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Parametry dla modelu jajka
N = 50  # Rozdzielczość siatki dla u i v
points = np.zeros((N, N, 3))  # Tablica przechowująca współrzędne (x, y, z)
colors = np.zeros((N, N, 3))  # Tablica przechowująca kolory dla każdego wierzchołka

# Funkcja do obliczania (x, y, z) na podstawie parametrów u, v dla kształtu jajka
def calculate_egg_points():
    u_values = np.linspace(0, 1, N)
    v_values = np.linspace(0, 1, N)
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            # Obliczenia na podstawie podanych wzorów dla x(u,v), y(u,v), i z(u,v)
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.cos(np.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5  # Dostosowane, aby jajko było wyśrodkowane wokół 0
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.sin(np.pi * v)
            points[i][j] = [x, y, z]
            colors[i][j] = [random.random(), random.random(), random.random()]  # Przypisanie losowego koloru

def spin(angle):
    glRotatef(angle, 1.0, 1.0, 1.0)  # Rotate around X, Y, Z axes
# Funkcja inicjalizująca okno i ustawiająca widok
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Ustawia kolor tła na czarny
    glEnable(GL_DEPTH_TEST)  # Włącza test głębokości
    calculate_egg_points()  # Wstępne obliczenie punktów dla modelu jajka

# Funkcja wyłączająca (pusta w tym przypadku)
def shutdown():
    pass

# Funkcja do rysowania osi X, Y, Z
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

# Funkcja renderująca scenę
def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    glLoadIdentity()

    angle = time * (180/math.pi)
    spin(angle)

    axes()
    # Rysowanie modelu jajka za pomocą GL_TRIANGLE_STRIP
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            # Dolny wierzchołek paska trójkątów
            glColor3f(*colors[i][j])  
            glVertex3f(*points[i][j])  

            # Górny wierzchołek paska trójkątów
            glColor3f(*colors[i + 1][j])  
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

    # Ustawienia projekcji ortograficznej w zależności od proporcji okna
    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 15.0, -15.0)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 15.0, -15.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Główna funkcja programu
def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
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
