import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (  # 顶点坐标  瞎写的
    (0, 0, 0),
    (2, 0, 0),
    (2, 2, 0),
    (0, 2, 0),
    (0, 0, 5),
    (2, 0, 5),
    (2, 2, 5),
    (0, 2, 5)
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


def Cube():
    glColor3f(1.0, 0.0, 0.0)  # 设置颜色
    glBegin(GL_LINES)  # glBegin和glEnd()是绘图的必备函数
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])  # 这个函数就是连点，这个函数执行两次画一条线，两点确定一条直线，参数为三维的坐标
    glEnd()


def main():
    pygame.init()
    display = (900, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)  # 设置背景颜色
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    # Z轴就是我们眼睛到屏幕方向的轴，负是远，正是近，其实就是让物体相对与屏幕在XYZ各方向移动几个距离
    glTranslatef(-1, -1, -10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出事件响应
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 用来删除就得画面，清空画布
        Cube()  # 创建模型
        glRotatef(1, 0, -1, 0)  # 旋转矩阵

        pygame.display.flip()  # 显示画面
        pygame.time.wait(10)  # 10ms刷新一次


main()
