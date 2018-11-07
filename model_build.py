import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

def vertex():
    verticies = (  # 顶点坐标  瞎写的
        (-2, -0.5, 8),
        (2, -0.5, 8),
        (2, 0.5, 8),
        (-2, 0.5, 8),
        (-2, -0.5, 8.5),
        (2, -0.5, 8.5),
        (2, 0.5, 8.5),
        (-2, 0.5, 8.5)
    )

    edges = (  # 边的顺序
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4)
    )
    return verticies, edges


def Cube(verticies, edges):
    glColor3f(1.0, 0.0, 0.0)  # 设置颜色
    glBegin(GL_LINES)  # glBegin和glEnd()是绘图的必备函数
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])  # 这个函数就是连点，这个函数执行两次画一条线，两点确定一条直线，参数为三维的坐标
    glEnd()


def draw_two_cable(verticies, edges):
    glColor(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3fv((1.5, -4, 8.5))
    glVertex3fv((1.5, 4, 8.5))
    glVertex3fv((-1.5, -4, 8.5))
    glVertex3fv((-1.5, 4, 8.5))
    glEnd()

def draw_mid_cable(verticies, edges):
    glColor(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3fv((0, -4, 10))
    glVertex3fv((0, 4, 10))
    glEnd()


def draw_cylinder(radius, height, num_slices):
    glColor3f(1.0, 0.0, 0.0)
    r = radius
    h = height
    n = float(num_slices)

    circle_pts = []
    for i in range(int(n) + 1):
        angle = 2 * math.pi * (i/n)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        pt = (x, y)
        circle_pts.append(pt)

    glBegin(GL_TRIANGLE_FAN)#drawing the back circle
    #glColor(1, 0, 0)
    glVertex(0, 0, h/2.0)
    for (x, y) in circle_pts:
        z = h/2.0
        glVertex(x, y, z)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)#drawing the front circle
    #glColor(0, 0, 1)
    glVertex(0, 0, h/2.0)
    for (x, y) in circle_pts:
        z = -h/2.0
        glVertex(x, y, z)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)#draw the tube
    #glColor(0, 1, 0)
    for (x, y) in circle_pts:
        z = h/2.0
        glVertex(x, y, z)
        glVertex(x, y, -z)
    glEnd()

def main():
    verticies, edges = vertex()
    pygame.init()
    display = (900, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)  # 设置背景颜色
    gluPerspective(100, (display[0] / display[1]), 0.1, 50.0)
    # Z轴就是我们眼睛到屏幕方向的轴，负是远，正是近，其实就是让物体相对与屏幕在XYZ各方向移动几个距离
    glTranslatef(0, 0, -20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出事件响应
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 用来删除就得画面，清空画布
        ##############################################################################################
        Cube(verticies, edges)  # 创建模型
        #             r   h   n_slice
        draw_cylinder(0.5, 20, 20)
        draw_two_cable(verticies, edges)
        draw_mid_cable(verticies, edges)
        ##############################################################################################
        glRotatef(1, 0, -1, 0)  # 旋转矩阵

        pygame.display.flip()  # 显示画面
        pygame.time.wait(10)  # 10ms刷新一次


if __name__ == '__main__':
    main()

