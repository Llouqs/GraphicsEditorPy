from PyQt5.uic.properties import QtGui

from EditorModel import ObjectFactory
from Frame import Frame
from plugin import Plugin
import typing as t

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPen, QPolygonF

from GrafObject import Figure
from Selection import FramedObjSelection


class RightTriangleFactory(Plugin, ObjectFactory):
    name = "RightTriangleFactory"
    icon_path = "plugins/images/RightTriangle.png"

    def OnLoad(self):
        print(f"{self.name} подключен")

    def OnUnLoad(self):
        print(f"{self.name} отключен")

    def __init__(self, store=None):
        super().__init__(store)
        if store is None:
            store = []
        self.object_type = "right_triangle"

    def create_object(self, x, y):
        """
        Метод создания объекта
        :param x: координата х
        :param y: координата y
        """
        frame = Frame(x, y, x, y)
        rightTriangle = RightTriangle(frame, self.pen_width, self.pen_color, self.brush_prop)
        self.store.add(rightTriangle)


class RightTriangle(Figure):

    def __init__(self, frame, pen_color, pen_width, brush_prop):
        super().__init__(frame, pen_color, pen_width, brush_prop)

    def create_selection(self):
        """
        Создание селектора прямоугольника
        """
        return FramedObjSelection(self)

    def draw_geometry(self, painter):
        xmax = max(self.frame.x1, self.frame.x2)
        xmin = min(self.frame.x1, self.frame.x2)
        ymax = max(self.frame.y1, self.frame.y2)
        ymin = min(self.frame.y1, self.frame.y2)
        pen = QPen(self.pen_color, self.pen_width)
        points = QPolygonF([
            QPoint(int(xmin), int(ymin)),
            QPoint(int(xmin), int(ymax)),
            QPoint(int(xmax), int(ymin))
        ])

        painter.painter.addPolygon(points, pen, self.brush_color)
