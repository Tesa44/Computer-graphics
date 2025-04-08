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


def drawRectangle(x,y,a,b, d = 0.0):
    if (d != 0.0):
        a *= d
        b *= d
    glColor3f(random.random(), random.random(), random.random())
    glBegin(GL_TRIANGLES)
    glVertex2f(x-(a/2),y+(b/2))
    glVertex2f(x+(a/2),y+(b/2))
    glVertex2f(x - (a / 2), y - (b / 2))
    glEnd()

    #glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + (a / 2), y - (b / 2))
    glVertex2f(x + (a / 2), y + (b / 2))
    glVertex2f(x - (a / 2), y - (b / 2))
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    drawRectangle(0.0,0.0,100.0,40.0,0.5)

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