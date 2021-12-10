from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QPolygon, QPolygonF
from PyQt5.uic.properties import QtCore

import GrafObject
from Selection import FramedObjSelection, LineSelection
import math
import typing as t


class Line(GrafObject.Figure):
    """
    Класс фигуры - Линия
    """

    def __init__(self, frame, pen_color, pen_width, brush_prop):
        super().__init__(frame, pen_color, pen_width, brush_prop)

    def draw_geometry(self, painter):
        """
        Отрисовка линии
        :param painter: средство рисования
        """
        pen = QPen(self.pen_color, self.pen_width)
        painter.painter.addLine(self.frame.x1, self.frame.y1, self.frame.x2, self.frame.y2, pen)

    def in_body(self, x, y):
        """
        Определение попадания точки на линию
        :param x: координата x
        :param y: координата y
        """
        xmax = max(self.frame.x1, self.frame.x2)
        xmin = min(self.frame.x1, self.frame.x2)
        ymax = max(self.frame.y1, self.frame.y2)
        ymin = min(self.frame.y1, self.frame.y2)

        distance = abs((ymax - ymin) * x - (xmax - xmin) * y + xmax * ymin - ymax * xmin) / (
            math.sqrt(pow(ymax - ymin, 2) + pow(xmax - xmin, 2)))
        print(f"{xmax} {self.frame.x1} {self.frame.x2} {x}")
        print(f"{ymax} {self.frame.y1} {self.frame.y2} {y} {distance}")

        return xmin - 5 <= x <= xmax + 5 and ymin - 5 <= y <= ymax + 5 and distance < 5

    def create_selection(self):
        """
        Создание селектора линии
        """
        return LineSelection(self)


class Rectangle(GrafObject.Figure):
    """
    Класс фигуры - Прямоугольник
    """

    def __init__(self, frame, pen_color, pen_width, brush_prop):
        super().__init__(frame, pen_color, pen_width, brush_prop)

    def draw_geometry(self, painter):
        """
        Отрисовка прямоугольника
        :param painter: средство рисования
        """

        xmax = max(self.frame.x1, self.frame.x2)
        xmin = min(self.frame.x1, self.frame.x2)
        ymax = max(self.frame.y1, self.frame.y2)
        ymin = min(self.frame.y1, self.frame.y2)
        w = xmax - xmin
        h = ymax - ymin
        pen = QPen(self.pen_color, self.pen_width)
        painter.painter.addRect(xmin, ymin, w, h, pen, self.brush_color)

    def create_selection(self):
        """
        Создание селектора прямоугольника
        """
        return FramedObjSelection(self)

    def in_body(self, x, y):
        """
        Определение попадания точки в прямоугольник
        :param x: координата x
        :param y: координата y
        """
        xmax = max(self.frame.x1, self.frame.x2)
        xmin = min(self.frame.x1, self.frame.x2)
        ymax = max(self.frame.y1, self.frame.y2)
        ymin = min(self.frame.y1, self.frame.y2)
        w = xmax - xmin
        h = ymax - ymin
        return xmin < x < xmin + w and ymin < y < ymin + h


class Ellipse(GrafObject.Figure):
    """
    Класс фигуры - Эллипс
    """

    def __init__(self, frame, pen_color, pen_width, brush_prop):
        super().__init__(frame, pen_color, pen_width, brush_prop)

    def draw_geometry(self, painter):
        """
        Отрисовка эллипса
        :param painter: средство рисования
        """
        xmax = max(self.frame.x1, self.frame.x2)
        xmin = min(self.frame.x1, self.frame.x2)
        ymax = max(self.frame.y1, self.frame.y2)
        ymin = min(self.frame.y1, self.frame.y2)
        w = xmax - xmin
        h = ymax - ymin

        pen = QPen(self.pen_color, self.pen_width)
        painter.painter.addEllipse(xmin, ymin, w, h, pen, self.brush_color)

    def create_selection(self):
        """
        Создание селектора для эллипса
        """
        return FramedObjSelection(self)

    def in_body(self, x, y):
        """
        Определение попадания точки в эллипс
        :param x: координата x
        :param y: координата y
        """
        x_c = (self.frame.x1 + self.frame.x2) / 2
        y_c = (self.frame.y1 + self.frame.y2) / 2

        return pow(x - x_c, 2) / pow((self.frame.x2 - self.frame.x1) / 2, 2) + pow(y - y_c, 2) / pow(
            (self.frame.y2 - self.frame.y1) / 2, 2) <= 1
