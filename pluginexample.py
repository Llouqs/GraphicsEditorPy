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

    def __init__(self, frame, pen_color, pen_width, brush_prop):
        super().__init__(frame, pen_color, pen_width, brush_prop)

    def draw_geometry(self, painter):
        pass
