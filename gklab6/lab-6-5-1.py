import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import glfw

# Parametry jajka
n = 20
texture_path = "tekstura.tga"

# Matryce przechowujące dane
vertices = np.zeros((n + 1, n + 1, 3))
normals = np.zeros((n + 1, n + 1, 3))
tex_coords = np.zeros((n + 1, n + 1, 2))

# Funkcja generująca wierzchołki jajka
def generate_vertices():
    for i in range(n + 1):
        for j in range(n + 1):
            u = i / n
            v = j / n
            x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.cos(np.pi * v)
            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2
            z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.sin(np.pi * v)
            vertices[i, j] = [x, y - 5, z]  # Przesunięcie w osi Y dla lepszego widoku

# Funkcja generująca wektory normalne
def generate_normals():
    for i in range(n + 1):
        for j in range(n + 1):
            u = i / n
            v = j / n
            xu = (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * np.cos(np.pi * v)
            xv = np.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * np.sin(np.pi * v)
            yu = 640 * u ** 3 - 960 * u ** 2 + 320 * u
            yv = 0
            zu = (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * np.sin(np.pi * v)
            zv = -np.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * np.cos(np.pi * v)

            nx = yu * zv - zu * yv
            ny = zu * xv - xu * zv
            nz = xu * yv - yu * xv
            length = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)

            if length > 0:
                nx, ny, nz = nx / length, ny / length, nz / length

            if i > n / 2:
                nx, ny, nz = -nx, -ny, -nz

            normals[i, j] = [nx, ny, nz]

# Funkcja generująca współrzędne tekstur
def generate_tex_coords():
    for i in range(n + 1):
        for j in range(n + 1):
            u = i / n
            v = j / n
            if i > n / 2:
                tex_coords[i, j] = [v, 1 - 2 * u]
            else:
                tex_coords[i, j] = [v, 2 * u]

# Funkcja renderująca jajko
def draw_egg():
    for i in range(n):
        for j in range(n):
            # Górna i dolna połowa jajka - ustawienie orientacji trójkątów
            if i > n / 2:
                glFrontFace(GL_CW)
            else:
                glFrontFace(GL_CCW)

            glBegin(GL_TRIANGLES)
            for k in range(3):
                idx = [(i, j + 1), (i, j), (i + 1, j + 1)][k]
                glTexCoord2f(*tex_coords[idx])
                glNormal3f(*normals[idx])
                glVertex3f(*vertices[idx])
            glEnd()

            glBegin(GL_TRIANGLES)
            for k in range(3):
                idx = [(i + 1, j + 1), (i, j), (i + 1, j)][k]
                glTexCoord2f(*tex_coords[idx])
                glNormal3f(*normals[idx])
                glVertex3f(*vertices[idx])
            glEnd()

# Funkcja ustawiająca teksturę
def set_texture():
    img = Image.open(texture_path)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes("raw", "RGB", 0, -1))

# Funkcja inicjalizacyjna
def startup():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    set_texture()

# Główna pętla
def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Egg with Texture", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    startup()

    generate_vertices()
    generate_normals()
    generate_tex_coords()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
        draw_egg()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
