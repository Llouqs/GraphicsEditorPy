from PyQt5 import QtGui
from PyQt5.QtGui import *

from Figures import Ellipse, Rectangle, Line
from Frame import Frame


class ObjectFactory:
    """
    Класс фабрики объектов
    """

    def __init__(self, store):
        self.object_type = None
        self.pen_width = 3
        self.pen_color = QtGui.QColor("black")
        self.brush_prop = QtGui.QColor("black")
        self.store = store

    def set_pen_width(self, pen_width):
        """
        Установка свойств ручки
        :param pen_width: толщина ручки
        """
        self.pen_width = pen_width

    def set_pen_color(self, pen_color):
        """
        Установка свойств ручки
        :param pen_color: цвет ручки
        """
        self.pen_color = pen_color

    def set_brush_prop(self, brush_prop):
        """
        Установка свойств ручки
        :param brush_prop: заливка
        """
        self.brush_prop = brush_prop

    def create_object(self, x, y):
        pass


class LineFactory(ObjectFactory):
    name = "Line"

    def __init__(self, store):
        super().__init__(store)
        self.object_type = "Line"

    def create_object(self, x, y):
        """
        Метод создания объекта
        :param x: координата х
        :param y: координата y
        """
        frame = Frame(x, y, x, y)
        line = Line(frame, self.pen_width, self.pen_color, self.brush_prop)
        self.store.add(line)


class EllipseFactory(ObjectFactory):
    name = "Ellipse"

    def __init__(self, store):
        super().__init__(store)
        self.object_type = "Ellipse"

    def create_object(self, x, y):
        """
        Метод создания объекта
        :param x: координата х
        :param y: координата y
        """
        frame = Frame(x, y, x, y)
        ellipse = Ellipse(frame, self.pen_width, self.pen_color, self.brush_prop)
        self.store.add(ellipse)


class RectangleFactory(ObjectFactory):
    name = "Rectangle"

    def __init__(self, store):
        super().__init__(store)
        self.object_type = "Rectangle"

    def create_object(self, x, y):
        """
        Метод создания объекта
        :param x: координата х
        :param y: координата y
        """
        frame = Frame(x, y, x, y)
        rectangle = Rectangle(frame, self.pen_width, self.pen_color, self.brush_prop)
        self.store.add(rectangle)