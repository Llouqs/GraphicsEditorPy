import typing as t

import Properties
from GrafObject import Figure


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


class SampleFigureInstance(Figure):

    def __init__(self, frame, props: Properties):
        super().__init__(frame)
        self.prop = props

    def change_properties(self, props):
        self.prop = props

    def draw(self, painter):
        """
        Метод отрисовки фигур
        :param painter: средство рисования
        """
        self.prop.apply_props(painter)
        self.draw_geometry(painter)

    def move(self, x, y):
        self.frame.move(x, y)

    def move_first_marker(self, x, y):
        self.frame.move_first_marker(x, y)

    def move_second_marker(self, x, y):
        self.frame.move_second_marker(x, y)

    def move_third_marker(self, x, y):
        self.frame.move_third_marker(x, y)

    def move_fourth_marker(self, x, y):
        self.frame.move_fourth_marker(x, y)

    def draw_geometry(self, painter):
        pass
