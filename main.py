from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random as rand
import os


HEIGHT, WIDTH = 800, 1000
BACKGROUND_COLOR = (0.0, 0.0, 0.0, 0.0)
BACKGROUND_COLORs = {
    "black": (0.0, 0.0, 0.0, 0.0),
    "white": (1.0, 1.0, 1.0, 0.0),
    "red": (1.0, 0.0, 0.0, 0.0),
    "green": (0.0, 1.0, 0.0, 0.0),
    "blue": (0.0, 0.0, 1.0, 0.0),
    "yellow": (1.0, 1.0, 0.0, 0.0),
    "cyan": (0.0, 1.0, 1.0, 0.0),
    "magenta": (1.0, 0.0, 1.0, 0.0),
    "gray": (0.5, 0.5, 0.5, 0.0),
    "skyblue": (0.529, 0.808, 0.922, 0.0),
    "nightblue": (0.0, 0.0, 0.2, 0.0),
}

SCORE = 0
# 3 shades of white
WHITECOLORS3f = [(1.0, 1.0, 1.0), (0.9, 0.9, 0.9), (0.8, 0.8, 0.8)]


VEL = 10
x_VEL = 5
ANGULAR_VEL = 5
PLAY = True
GAME_OVER = False
DAY = True
CURRENT_TIME = time.time()


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
    midPointLine(x4, y4, x3, y3, size)
    midPointLine(x4, y4, x1, y1, size)


def drawSolidPolygon(x1, y1, x2, y2, x3, y3, x4, y4, size):
    while x1 <= x4:
        midPointLine(x1, y1, x2, y2, size)
        x1 += 1
        x2 += 1


def drawBall(xc, yc, r, pix, cross=False):
    x = r
    while x > 0:
        midPointCircle(xc, yc, x, pix, "fullcircle")
        x -= 1
    x = r
    while x > 0:
        midPointCircle(xc, yc, x, 1.5, "halfcircleUp")
        x -= 2
    if cross:
        glColor3f(*COLORS3f["white"])
        midPointLine(xc - r, yc, xc + r, yc, 2)


def spiralBall(xc, yc, r, pix):
    x = r
    while x > 0:
        midPointCircle(xc, yc, x, pix, "fullcircle")
        x -= 1
    glColor3f(*COLORS3f["red"])
    p = 2
    midPointLine(xc, yc, xc, yc + r, p)
    midPointLine(xc, yc - r, xc, yc, p)
    midPointLine(xc, yc, xc + r, yc, p)
    midPointLine(xc, yc, xc - r, yc, p)
    midPointLine(xc, yc, xc + r, yc + r, p)
    midPointLine(xc, yc, xc + r, yc - r, p)
    midPointLine(xc, yc, xc - r, yc + r, p)
    midPointLine(xc, yc, xc - r, yc - r, p)


# ************************   buttons  ************************


def dayTime(size):
    drawPolygon(50, 600, 50, 650, 100, 650, 100, 600, size)
    # sun inside box
    glColor3f(*COLORS3f["yellow"])
    drawBall(75, 625, 15, size)


def nightTime(size):
    drawPolygon(50, 600, 50, 650, 100, 650, 100, 600, size)
    # moon inside box
    glColor3f(*COLORS3f["white"])
    drawBall(75, 625, 15, size)


def drawLeftArrow(size):
    drawPolygon(50, 700, 50, 750, 100, 750, 100, 700, size)

    # arrow inside box
    midPointLine(60, 725, 90, 740, size)
    midPointLine(60, 725, 90, 710, size)


def cross(size):
    drawPolygon(900, 700, 900, 750, 950, 750, 950, 700, size)

    # cross inside box
    midPointLine(910, 710, 940, 740, size)
    midPointLine(910, 740, 940, 710, size)


def play(size):
    drawPolygon(800, 700, 800, 750, 850, 750, 850, 700, size)

    # play inside box

    midPointLine(810, 710, 810, 740, size)
    midPointLine(810, 740, 840, 725, size)
    midPointLine(810, 710, 840, 725, size)


def pause(size):
    drawPolygon(800, 700, 800, 750, 850, 750, 850, 700, size)
    # pause inside box
    midPointLine(815, 710, 815, 740, size)
    midPointLine(835, 710, 835, 740, size)


class Obstacle:
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.angle = 0

    def draw(self):
        if self.type == "rectangle":
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
        if self.type == "spninig_rect" or self.type == "spninig_gear":
            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2
            radius = self.width / 2

            # Apply rotation
            glPushMatrix()
            glTranslatef(center_x, center_y, 0)
            glRotatef(self.angle, 0, 0, 1)
            glTranslatef(-center_x, -center_y, 0)

            if self.type == "spninig_rect":
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
            elif self.type == "spninig_gear":
                spiralBall(self.x + self.width / 2, self.y + self.height / 2, radius, 1)

            # Reset transformation
            glPopMatrix()

    def update(self):
        self.x -= VEL
        if self.type == "spninig_rect" or self.type == "spninig_gear":
            self.angle += ANGULAR_VEL
        self.draw()


# obstacle1 = Obstacle(1000, 100, 50, 50, "spninig_rect")
# obstacle2 = Obstacle(1000, 100, 50, 50, "rectangle")
# obstacle3 = Obstacle(1000, 125, 25, 25, "spninig_gear")
# obstacle4 = Obstacle(1000, 120, 25, 25, "rectangle")
# obstacle5 = Obstacle(1000, 120, 25, 25, "spninig_rect")

# OBSTACLES = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5]
OBSTACLES = []

for i in range(10):
    x = 1000
    y = rand.randint(100, 200)
    width = rand.randint(25, 50)
    height = rand.randint(25, 50)
    typ = rand.choice(["rectangle", "spninig_rect", "spninig_gear"])
    OBSTACLES.append(Obstacle(x, y, width, height, typ))


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

        drawBall(center_x, center_y, radius, 1, True)

        # Reset transformation
        glPopMatrix()

    def checkCollision(self, obstacle):
        if self.x + self.width >= obstacle.x and self.x <= obstacle.x + obstacle.width:
            if (
                self.y + self.height >= obstacle.y
                and self.y <= obstacle.y + obstacle.height
            ):
                return True
        return False

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


class SunMoon:
    def __init__(self, x, y, radius, typ):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = 0
        self.typ = typ

        self.glowx = self.x + self.radius / 2
        self.glowy = self.y + self.radius / 2
        self.glowradius = self.radius / 2

    def draw(self):
        center_x = self.x + self.radius / 2
        center_y = self.y + self.radius / 2
        radius = self.radius / 2

        # Apply rotation
        glPushMatrix()
        glTranslatef(center_x, center_y, 0)
        glRotatef(self.angle, 0, 0, 1)  # Rotate around z-axis
        glTranslatef(-center_x, -center_y, 0)

        drawBall(center_x, center_y, radius, 1)

        # Reset transformation
        glPopMatrix()

    def glow(self):
        # random white glow
        glColor3f(*rand.choice(WHITECOLORS3f))

        midPointCircle(self.glowx, self.glowy, self.glowradius - 40, 1, "fullcircle")
        midPointCircle(self.glowx, self.glowy, self.glowradius - 20, 1, "fullcircle")
        midPointCircle(self.glowx, self.glowy, self.glowradius, 1, "fullcircle")
        midPointCircle(self.glowx, self.glowy, self.glowradius + 20, 1, "fullcircle")
        midPointCircle(self.glowx, self.glowy, self.glowradius + 40, 1, "fullcircle")

    def update(self):
        self.glow()
        if self.typ == "sun":
            glColor3f(*COLORS3f["yellow"])
            self.draw()
        else:
            glColor3f(*COLORS3f["white"])
            self.draw()
        self.angle += 1
        self.glowradius += 1
        if self.glowradius >= self.radius:
            self.glowradius = self.radius / 2


SUN = SunMoon(400, 600, 100, "sun")
MOON = SunMoon(400, 600, 100, "moon")


def reSet():
    global character, obstacle_on_screen, curr_time
    character = Character(100, 100, 50, 50)
    obstacle_on_screen = []
    curr_time = time.time()
    PLAY = True
    SCORE = 0


# ************************   KeyBoard / Mouse Events  ************************


def keyboardEvent(key, x, y):
    if key == b" " and not character.jump and PLAY:
        character.jump = True
        print("############ ")
    if key == b"\x1b":  # escape key
        os._exit(0)


def mouseEvent(button, state, x, y):
    global PLAY, DAY
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 50 <= x <= 100 and 700 <= HEIGHT - y <= 750:
            print("Left Arrow")
            reSet()
        elif 800 <= x <= 850 and 700 <= HEIGHT - y <= 750:
            print("Play")
            PLAY = not PLAY
        elif 900 <= x <= 950 and 700 <= HEIGHT - y <= 750:
            print("Exit")
            os._exit(0)
        elif 50 <= x <= 100 and 600 <= HEIGHT - y <= 650:
            print("Day")
            DAY = not DAY


obstacle_on_screen = [rand.choice(OBSTACLES)]


def gamePlay():
    global SCORE, PLAY, VEL, ANGULAR_VEL, DAY, CURRENT_TIME
    glColor3f(*COLORS3f["gray"])
    drawSolidPolygon(0, 0, 0, 100, 1000, 100, 1000, 0, 1)

    glColor3f(*COLORS3f["white"])
    stripes.update()
    if DAY:
        glColor3f(*COLORS3f["black"])
    else:
        glColor3f(*COLORS3f["cyan"])
    character.update()

    glColor3f(*COLORS3f["red"])

    # create random obstacles from obstacles list after every 2 seconds
    if time.time() - CURRENT_TIME >= 10:
        obstacle_on_screen.append(rand.choice(OBSTACLES))
        CURRENT_TIME = time.time()

    # update obstacles
    for ob in obstacle_on_screen:
        if character.checkCollision(ob):
            print("Game Over")
            print("Score: ", SCORE)
            PLAY = False
            reSet()
            time.sleep(5)
            return
        if ob.x < -100:
            ob.x = rand.randint(1000, 1200)
            ob.y = rand.randint(100, 200)
            obstacle_on_screen.remove(ob)
            SCORE += 1
            VEL += 0.2
            ANGULAR_VEL += 0.2
        ob.update()


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global BACKGROUND_COLOR

    if DAY:
        BACKGROUND_COLOR = BACKGROUND_COLORs["skyblue"]
    else:
        BACKGROUND_COLOR = BACKGROUND_COLORs["nightblue"]
    glClearColor(*BACKGROUND_COLOR)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    CURRENT_TIME = time.time()

    glColor3f(*COLORS3f["red"])
    cross(2)

    if PLAY:
        glColor3f(*COLORS3f["green"])
        pause(2)
    else:
        glColor3f(*COLORS3f["yellow"])
        play(2)

    glColor3f(*COLORS3f["white"])
    drawLeftArrow(2)

    if PLAY:
        gamePlay()
        if DAY:
            glColor3f(*COLORS3f["black"])
            nightTime(2)

            glColor3f(*COLORS3f["yellow"])
            SUN.update()
        elif not DAY:
            glColor3f(*COLORS3f["white"])
            dayTime(2)

            glColor3f(*COLORS3f["white"])
            MOON.update()

            for i in range(100):
                glColor3f(*rand.choice(WHITECOLORS3f))
                draw_points(rand.randint(10, 1000), rand.randint(300, 800), 1)
    else:
        glColor3f(*COLORS3f["gray"])
        drawSolidPolygon(0, 0, 0, 100, 1000, 100, 1000, 0, 1)
        glColor3f(*COLORS3f["white"])
        stripes.draw()
        glColor3f(*COLORS3f["green"])
        character.draw()
        glColor3f(*COLORS3f["red"])
        for ob in obstacle_on_screen:
            ob.draw()

        if DAY:
            glColor3f(*COLORS3f["black"])
            nightTime(2)

            glColor3f(*COLORS3f["yellow"])
            SUN.draw()
        elif not DAY:
            glColor3f(*COLORS3f["white"])
            dayTime(2)

            glColor3f(*COLORS3f["white"])
            MOON.draw()

    glutSwapBuffers()


def main():
    glutInit()

    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)  # window size
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Infinite Balling")  # window name

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardEvent)
    glutMouseFunc(mouseEvent)

    glutIdleFunc(showScreen)

    glutMainLoop()


if __name__ == "__main__":
    main()
