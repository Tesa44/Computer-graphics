import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    glClearColor(0.5,0.5,0.5,1.0)
    update_viewport(None,800, 800)

def shutdown():
    pass

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,width, height)
    glLoadIdentity();

    if width <= height:
        glOrtho(-100.0,100.0,-100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def drawFractalTrian(x,y,a,st = 3):
    if st == 0:
        drawTriangle(x,y,a)
    else:
        h = (a * (3 ** (0.5))) / 2
        #Górny trójkąt
        drawFractalTrian(x,y + (h/3),a/2, st - 1)
        #Lewy trójkąt
        drawFractalTrian(x - (a/4), y - (h/6), a/2, st - 1)
        #Prawy trójkąt
        drawFractalTrian(x + (a/4), y - (h/6), a/2, st - 1)

def drawTriangle(x,y,a):
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    h = (a*(3**(0.5)))/2
    R = (2/3)*h
    r = (1/3)*h
    glVertex2f(x,y + R)
    glVertex2f(x - (a/2),y - r)
    glVertex2f(x + (a/2),y - r)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    drawFractalTrian(0.0,0.0,100,5)

    glFlush()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate();
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwWaitEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()