from PyQt5.uic.properties import QtGui

from EditorModel import ObjectFactory
from Frame import Frame
from plugin import Plugin
import typing as t

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPen, QPolygonF

from GrafObject import Figure
from Selection import FramedObjSelection


class BowknotFactory(Plugin, ObjectFactory):
    name = "Bowknot"

    def OnLoad(self):
        print("Bowknot подключен")

    def __init__(self, store=None):
        super().__init__(store)
        if store is None:
            store = []
        self.object_type = "bowknot"

    def create_object(self, x, y):
        """
        Метод создания объекта
        :param x: координата х
        :param y: координата y
        """
        frame = Frame(x, y, x, y)
        bowknot = Bowknot(frame, self.pen_width, self.pen_color, self.brush_prop)
        self.store.add(bowknot)


class Bowknot(Figure):

    def __init__(self, frame, pen_color, pen_width, brush_prop):
        super().__init__(frame, pen_color, pen_width, brush_prop)

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

    def draw_geometry(self, painter):
        xmax = max(self.frame.x1, self.frame.x2)
        xmin = min(self.frame.x1, self.frame.x2)
        ymax = max(self.frame.y1, self.frame.y2)
        ymin = min(self.frame.y1, self.frame.y2)
        pen = QPen(self.pen_color, self.pen_width)
        points = QPolygonF([
            QPoint(xmin, ymin),
            QPoint(xmin, ymax),
            QPoint(xmax, ymin),
            QPoint(xmax, ymax)
        ])

        painter.painter.addPolygon(points, pen, self.brush_color)
