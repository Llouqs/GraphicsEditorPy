import typing as t

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPen, QPolygonF

from GrafObject import Figure
from Selection import FramedObjSelection
from EditorModel import ObjectFactory


def setup() -> t.List:
    return [OurFactory()]


class OurFactory:
    @property
    def figure_id(self) -> str:
        return "SampleFigure"

    @property
    def name(self) -> str:
        return self.figure_id

    @property
    def icon(self) -> str:
        return ""

    def start_figure(self, x: int, y: int) -> Figure:
        raise NotImplementedError

    def update_figure(self, f: Figure, x: int, y: int):
        raise NotImplementedError

    def complete_figure(self, f: Figure, x: int, y: int):
        raise NotImplementedError

    def cancel_figure(self, f: Figure):
        raise NotImplementedError


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
