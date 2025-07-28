from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import os

weather_data = [
    {"type": "Cloudy", "temp": "27°", "wind": "10 km/h", "humidity": "55%"},
    {"type": "Sunny", "temp": "31°", "wind": "6 km/h", "humidity": "40%"},
    {"type": "Night", "temp": "22°", "wind": "5 km/h", "humidity": "60%"},
    {"type": "Storm", "temp": "25°", "wind": "30 km/h", "humidity": "80%"},
    {"type": "Stormy Cloud", "temp": "24°", "wind": "35 km/h", "humidity": "85%"},
    {"type": "Night Cloud", "temp": "20°", "wind": "7 km/h", "humidity": "70%"},
    {"type": "Overcast", "temp": "26°", "wind": "12 km/h", "humidity": "65%"},
    {"type": "Partly Cloudy", "temp": "28°", "wind": "9 km/h", "humidity": "58%"},
    {"type": "Rain", "temp": "23°", "wind": "20 km/h", "humidity": "90%"},
    {"type": "Snow", "temp": "-2°", "wind": "10 km/h", "humidity": "75%"},
]


textures = []
current_index = 0

def load_textures():
    global textures
    textures = glGenTextures(len(weather_data))

    for i in range(len(weather_data)):
        image_path = f"icon{i}.png"   # assumes icon0.png to icon9.png
        if not os.path.exists(image_path):
            print(f"Missing: {image_path}")
            continue

        img = Image.open(image_path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGBA").tobytes()
        width, height = img.size

        glBindTexture(GL_TEXTURE_2D, textures[i])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0, 0, 0)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def draw_icon(index):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[index])
    glColor3f(1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-0.3, 0.3)
    glTexCoord2f(1, 0); glVertex2f( 0.3, 0.3)
    glTexCoord2f(1, 1); glVertex2f( 0.3, 0.9)
    glTexCoord2f(0, 1); glVertex2f(-0.3, 0.9)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def display():
    glClearColor(1.0, 1.0, 1.0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    data = weather_data[current_index]
    draw_icon(current_index)

    draw_text(-0.1, 0.05, f"{data['temp']}")
    draw_text(-0.1, -0.05, f"{data['type']}")
    draw_text(-0.3, -0.2, f"Wind: {data['wind']}")
    draw_text(-0.3, -0.3, f"Humidity: {data['humidity']}")
    draw_text(-0.4, -0.5, "Click to switch weather ➡️")

    glutSwapBuffers()

def mouse(button, state, x, y):
    global current_index
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        current_index = (current_index + 1) % len(weather_data)
        glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(600, 800)
    glutCreateWindow(b"Weather Dashboard (with Icons)")
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    load_textures()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMainLoop()

if __name__ == "__main__":
    main()
