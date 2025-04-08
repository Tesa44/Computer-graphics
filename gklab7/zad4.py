#!/usr/bin/env python3

import ctypes
import sys

from glfw.GLFW import *
import glm
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *

rendering_program = None
vertex_array_object = None
vertex_buffer = None
color_buffer = None
P_matrix = None


def compile_shaders():
    vertex_shader_source = """
        #version 330 core

        layout(location = 0) in vec4 position;
        layout(location = 1) in vec4 color;

        uniform mat4 V_matrix;
        uniform mat4 P_matrix;
        uniform float time; // Time uniform for dynamic rotation

        out vec4 vertex_color; // Output color to fragment shader

        void main(void) {
            // Compute translation based on instance ID
            int row = gl_InstanceID / 10;  // Row in the grid
            int col = gl_InstanceID % 10; // Column in the grid

            mat4 translation = mat4(1.0);
            translation[3] = vec4(col - 5.0, row - 5.0, 0.0, 1.0);

            // Dynamic rotation based on time
            mat4 rotation = mat4(1.0);
            float angle = time; 
            rotation[0][0] = cos(angle);
            rotation[0][2] = sin(angle);
            rotation[2][0] = -sin(angle);
            rotation[2][2] = cos(angle);

            mat4 M_matrix = translation * rotation;

            gl_Position = P_matrix * V_matrix * M_matrix * position;
            vertex_color = color; // Pass color to fragment shader
        }
    """

    fragment_shader_source = """
        #version 330 core

        in vec4 vertex_color; // Input from vertex shader
        out vec4 color;

        void main(void) {
            color = vertex_color; // Use vertex color
        }
    """

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, [vertex_shader_source])
    glCompileShader(vertex_shader)
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(vertex_shader).decode('UTF-8'))

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, [fragment_shader_source])
    glCompileShader(fragment_shader)
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(fragment_shader).decode('UTF-8'))

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    success = glGetProgramiv(program, GL_LINK_STATUS)

    if not success:
        print('Program linking error:')
        print(glGetProgramInfoLog(program).decode('UTF-8'))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program




def startup():
    global rendering_program
    global vertex_array_object
    global vertex_buffer
    global color_buffer

    print("OpenGL {}, GLSL {}\n".format(
        glGetString(GL_VERSION).decode('UTF-8').split()[0],
        glGetString(GL_SHADING_LANGUAGE_VERSION).decode('UTF-8').split()[0]
    ))

    update_viewport(None, 400, 400)
    glEnable(GL_DEPTH_TEST)

    rendering_program = compile_shaders()

    # Correct usage for glGenVertexArrays
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)


    # Define vertex positions
    vertex_positions = numpy.array([
        -0.25, +0.25, -0.25,
        -0.25, -0.25, -0.25,
        +0.25, -0.25, -0.25,

        +0.25, -0.25, -0.25,
        +0.25, +0.25, -0.25,
        -0.25, +0.25, -0.25,

        +0.25, -0.25, -0.25,
        +0.25, -0.25, +0.25,
        +0.25, +0.25, -0.25,

        +0.25, -0.25, +0.25,
        +0.25, +0.25, +0.25,
        +0.25, +0.25, -0.25,

        +0.25, -0.25, +0.25,
        -0.25, -0.25, +0.25,
        +0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        -0.25, +0.25, +0.25,
        +0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        -0.25, -0.25, -0.25,
        -0.25, +0.25, +0.25,

        -0.25, -0.25, -0.25,
        -0.25, +0.25, -0.25,
        -0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        +0.25, -0.25, +0.25,
        +0.25, -0.25, -0.25,

        +0.25, -0.25, -0.25,
        -0.25, -0.25, -0.25,
        -0.25, -0.25, +0.25,

        -0.25, +0.25, -0.25,
        +0.25, +0.25, -0.25,
        +0.25, +0.25, +0.25,

        +0.25, +0.25, +0.25,
        -0.25, +0.25, +0.25,
        -0.25, +0.25, -0.25,
    ], dtype='float32')

    # Define colors for each face
    vertex_colors = numpy.array([
        # Red face
        # Triangle one
        1.0, 0.0, 0.5, 1.0,
        1.0, 0.0, 0.5, 1.0,
        1.0, 0.0, 0.5, 1.0,
        # Triangle two
        1.0, 0.0, 0.5, 1.0,
        1.0, 0.0, 0.5, 1.0,
        1.0, 0.0, 0.5, 1.0,

        # Green face
        0.0, 1.0, 0.5, 1.0,
        0.0, 1.0, 0.5, 1.0,
        0.0, 1.0, 0.5, 1.0,

        0.0, 1.0, 0.5, 1.0,
        0.0, 1.0, 0.5, 1.0,
        0.0, 1.0, 0.5, 1.0,

        # Blue face
        0.0, 0.9, 1.0, 1.0,
        0.0, 0.9, 1.0, 1.0,
        0.0, 0.9, 1.0, 1.0,

        0.0, 0.9, 1.0, 1.0,
        0.0, 0.9, 1.0, 1.0,
        0.0, 0.9, 1.0, 1.0,

        # Yellow face
        1.0, 1.0, 0.5, 1.0,
        1.0, 1.0, 0.5, 1.0,
        1.0, 1.0, 0.5, 1.0,

        1.0, 1.0, 0.4, 1.0,
        1.0, 1.0, 0.4, 1.0,
        1.0, 1.0, 0.4, 1.0,

        # White face
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,

        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,

        # Purple face
        0.5, 0.0, 1.0, 1.0,
        0.5, 0.0, 1.0, 1.0,
        0.5, 0.0, 1.0, 1.0,

        0.5, 0.0, 1.0, 1.0,
        0.5, 0.0, 1.0, 1.0,
        0.5, 0.0, 1.0, 1.0,
    ], dtype='float32')

    # Create and bind vertex buffer
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_positions, GL_STATIC_DRAW)

    # Create and bind color buffer
    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_colors, GL_STATIC_DRAW)

    # Enable position attribute
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Enable color attribute
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)


def shutdown():
    global rendering_program
    global vertex_array_object
    global vertex_buffer
    global color_buffer

    # Ensure vertex_array_object is passed as a NumPy array or list
    glDeleteProgram(rendering_program)
    glDeleteVertexArrays(1, [vertex_array_object])  # Pass as a list
    glDeleteBuffers(1, [vertex_buffer])
    glDeleteBuffers(1, [color_buffer])



def render(time):
    glClearBufferfv(GL_COLOR, 0, [0.0, 0.0, 0.0, 1.0])
    glClearBufferfi(GL_DEPTH_STENCIL, 0, 1.0, 0)

    glUseProgram(rendering_program)

    # View and projection matrices
    V_matrix = glm.lookAt(
        glm.vec3(0.0, 0.0, 5.0),  # Camera position
        glm.vec3(0.0, 0.0, 0.0),  # Look at the origin
        glm.vec3(0.0, 1.0, 0.0)   # Up direction
    )
    glUniformMatrix4fv(glGetUniformLocation(rendering_program, "V_matrix"), 1, GL_FALSE, glm.value_ptr(V_matrix))
    glUniformMatrix4fv(glGetUniformLocation(rendering_program, "P_matrix"), 1, GL_FALSE, glm.value_ptr(P_matrix))

    # Pass the time uniform
    glUniform1f(glGetUniformLocation(rendering_program, "time"), time)

    # Render all instances (10x10 grid = 100 instances)
    glDrawArraysInstanced(GL_TRIANGLES, 0, 36, 100)




def update_viewport(window, width, height):
    global P_matrix

    aspect = width / height
    P_matrix = glm.perspective(glm.radians(70.0), aspect, 0.1, 1000.0)

    glViewport(0, 0, width, height)


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def glfw_error_callback(error, description):
    print('GLFW Error:', description)


def main():
    glfwSetErrorCallback(glfw_error_callback)

    if not glfwInit():
        sys.exit(-1)

    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
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
