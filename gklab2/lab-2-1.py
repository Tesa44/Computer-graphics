import sys
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

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    #Pierwszy trójkąt
    glBegin(GL_TRIANGLES)
    #Pierwszy wierzchołek - zielony
    glColor3f(0.0,1.0,0.0)
    glVertex2f(0.0,0.0)

    #drugi wierzchołek - czerwony
    glColor3f(1.0,0.0,0.0)
    glVertex2f(0.0,50.0)

    #trzeci wierzchołek - niebieski
    glColor3f(0.0,0.0,1.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    #drugi trójkąt
    glBegin(GL_TRIANGLES)
    glColor3f(0.0,1.0,1.0)
    glVertex2f(0.0, 0.0)
    glColor3f(1.0,0.0,1.0)
    glVertex2f(0.0, 50.0)
    glColor3f(1.0,1.0,0.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

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