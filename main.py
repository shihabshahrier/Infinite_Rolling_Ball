from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random as r


HEIGHT, WIDTH = 800, 1000
BACKGROUND_COLOR = (0.0, 0.0, 0.0, 0.0)
VEL = 20
x_VEL = 5


COLORS3f = {
    "red": (1.0, 0.0, 0.0),
    "green": (0.0, 1.0, 0.0),
    "blue": (0.0, 0.0, 1.0),
    "yellow": (1.0, 1.0, 0.0),
    "cyan": (0.0, 1.0, 1.0),
    "magenta": (1.0, 0.0, 1.0),
    "white": (1.0, 1.0, 1.0),
    "black": (0.0, 0.0, 0.0),
    "gray": (0.5, 0.5, 0.5),
    "darkgray": (0.3, 0.3, 0.3),
    "lightgray": (0.7, 0.7, 0.7),
    "orange": (1.0, 0.5, 0.0),
    "darkgreen": (0.0, 0.5, 0.0),
    "darkblue": (0.0, 0.0, 0.5),
    "darkred": (0.5, 0.0, 0.0),
    "darkyellow": (0.5, 0.5, 0.0),
    "darkcyan": (0.0, 0.5, 0.5),
    "darkmagenta": (0.5, 0.0, 0.5),
    "darkorange": (0.5, 0.3, 0.0),
    "lightgreen": (0.5, 1.0, 0.5),
    "lightblue": (0.5, 0.5, 1.0),
    "lightred": (1.0, 0.5, 0.5),
    "lightyellow": (1.0, 1.0, 0.5),
    "lightcyan": (0.5, 1.0, 1.0),
    "lightmagenta": (1.0, 0.5, 1.0),
}


def draw_points(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def drawCircle(xc, yc, x, y, pix, typ):
    if typ == "halfcircleUp" or typ == "fullcircle":
        draw_points(xc + x, yc + y, pix)  # zone 0
        draw_points(xc + y, yc + x, pix)  # zone 1
        draw_points(xc - y, yc + x, pix)  # zone 2
        draw_points(xc - x, yc + y, pix)  # zone 3
    if typ == "halfcircleDown" or typ == "fullcircle":
        draw_points(xc - x, yc - y, pix)  # zone 4
        draw_points(xc - y, yc - x, pix)  # zone 5
        draw_points(xc + y, yc - x, pix)  # zone 6
        draw_points(xc + x, yc - y, pix)  # zone 7


def midPointCircle(xc, yc, r, pix, typ):
    x = 0
    y = r
    drawCircle(xc, yc, x, y, pix, typ)
    d = 1 - r
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * (x - y) + 5
            x += 1
            y -= 1
        drawCircle(xc, yc, x, y, pix, typ)


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx >= 0 and dy >= 0:
        if dx >= dy:
            return 0
        else:
            return 1
    elif dx < 0 and dy >= 0:
        if -dx >= dy:
            return 3
        else:
            return 2
    elif dx < 0 and dy < 0:
        if dx <= dy:
            return 4
        else:
            return 5
    elif dx >= 0 and dy < 0:
        if dx >= -dy:
            return 7
        else:
            return 6


def toZoneZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def midPointLine(x1, y1, x2, y2, size):
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = toZoneZero(x1, y1, zone)
    x2, y2 = toZoneZero(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    de = 2 * dy
    dne = 2 * (dy - dx)
    x = x1
    y = y1
    while x <= x2:
        real_x, real_y = toZoneZero(x, y, zone)
        draw_points(real_x, real_y, size)
        if d <= 0:
            d = d + de
            x = x + 1
        else:
            d = d + dne
            x = x + 1
            y = y + 1


def drawPolygon(x1, y1, x2, y2, x3, y3, x4, y4, size):
    midPointLine(x1, y1, x2, y2, size)
    midPointLine(x2, y2, x3, y3, size)
    midPointLine(x3, y3, x4, y4, size)
    midPointLine(x4, y4, x1, y1, size)


def drawSolidPolygon(x1, y1, x2, y2, x3, y3, x4, y4, size):
    while x1 <= x4:
        midPointLine(x1, y1, x2, y2, size)
        x1 += 1
        x2 += 1


def drawBall(xc, yc, r, pix):
    x = r
    while x > 0:
        midPointCircle(xc, yc, x, pix, "fullcircle")
        x -= 1

    glColor3f(0.1, 0.1, 0.1)
    midPointLine(xc - r, yc, xc + r, yc, 2)


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        drawSolidPolygon(
            self.x,
            self.y,
            self.x,
            self.y + self.height,
            self.x + self.width,
            self.y + self.height,
            self.x + self.width,
            self.y,
            1,
        )

    def update(self):
        self.x -= VEL
        self.draw()


obstacle = Obstacle(1000, 100, 50, 50)


class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x_init = x
        self.y_init = y
        self.width, self.height = width, height
        self.jump = False
        self.fall = False

        self.angle = 0

    def draw(self):
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        radius = self.width / 2

        # Apply rotation
        glPushMatrix()
        glTranslatef(center_x, center_y, 0)
        glRotatef(self.angle, 0, 0, 1)  # Rotate around z-axis
        glTranslatef(-center_x, -center_y, 0)

        drawBall(center_x, center_y, radius, 1)

        # Reset transformation
        glPopMatrix()

    def update(self):
        if self.x > WIDTH - 600:
            if self.jump:
                self.fall = True
            self.jump = False

        if self.jump and self.y <= 200:
            self.y += VEL
            self.x += x_VEL
        else:
            self.fall = True
        if self.fall and self.y > 100:
            if self.jump:
                self.jump = False
            self.y -= VEL
            self.x += x_VEL
        else:
            self.fall = False
        if not self.fall and not self.jump and self.x > self.x_init:
            self.x -= x_VEL
        if self.x <= self.x_init:
            self.angle -= 60
        else:
            self.angle += 60

        self.draw()


character = Character(100, 100, 50, 50)


class Stipes:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width, self.height = width, height

        self.x1 = x - 200
        self.y1 = height / 2
        self.x2 = x + 600
        self.y2 = height / 2

    def draw(self):
        midPointLine(self.x1, self.y1, self.x1 + 200, self.y1, 20)
        midPointLine(self.x2, self.y2, self.x2 + 200, self.y2, 20)

    def update(self):
        if self.x1 <= -200:
            self.x1 = 1000
        if self.x2 <= -200:
            self.x2 = 1000
        self.x1 -= VEL
        self.x2 -= VEL
        self.draw()


stripes = Stipes(0, 0, 1000, 100)


def keyboard(key, x, y):
    if key == b" ":
        character.jump = True
        print("############ ")


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global BACKGROUND_COLOR
    glClearColor(*BACKGROUND_COLOR)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(*COLORS3f["gray"])
    # midPointCircle(250, 250, 100, 1, "fullcircle")
    # drawPolygon(0, 0, 0, 100, 1000, 100, 1000, 0, 1)
    drawSolidPolygon(0, 0, 0, 100, 1000, 100, 1000, 0, 1)

    glColor3f(*COLORS3f["red"])
    obstacle.update()

    glColor3f(*COLORS3f["green"])
    character.update()

    glColor3f(*COLORS3f["white"])
    stripes.update()
    
    glutSwapBuffers()


def main():
    glutInit()

    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)  # window size
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Task 01")  # window name

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboard)

    glutIdleFunc(showScreen)

    glutMainLoop()


if __name__ == "__main__":
    main()
