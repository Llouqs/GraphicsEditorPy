from Selection import FramedObjSelection
import copy
import abc
import typing as t


# @t.runtime_checkable (t.Protocol)
class GrafObject:
    """
    Абстрактный класс графических примитивов
    """

    def __init__(self, frame=None):
        self.list = []
        self.frame = frame
        self.is_group = False
        self.select = False
        self.gr_state = False
        self.relative_x1 = 0
        self.relative_x2 = 0
        self.relative_y1 = 0
        self.relative_y2 = 0


    def in_body(self, x1, y1):
        pass

    def draw(self, painter):
        pass

    def create_selection(self):
        pass

    def move(self, x, y):
        pass

    def move_first_marker(self, x, y):
        pass

    def move_second_marker(self, x, y):
        pass

    def move_third_marker(self, x, y):
        pass

    def move_fourth_marker(self, x, y):
        pass


class Figure(GrafObject):
    """
    Класс фигура
    """

    def __init__(self, frame, pen_width, pen_color, brush_color):
        super().__init__(frame)
        self.pen_color = pen_color
        self.pen_width = pen_width
        self.brush_color = brush_color

    def draw(self, painter):
        """
        Метод отрисовки фигур
        :param painter: средство рисования
        """
        painter.pen_color = self.pen_color
        painter.pen_width = self.pen_width
        painter.brush_color = self.brush_color
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


class Group(GrafObject):
    """
    Класс группы
    """

    def __init__(self, list):
        super().__init__(self)
        self.gr_list = list
        self.is_group = True
        self.frame = copy.deepcopy(self.gr_list[0].frame)
        self.frame.combine(self.gr_list)
        self.coord_group()

    def change_properties(self, props):
        for object in self.gr_list:
            object.prop = props

    def coord_group(self):
        """
        определение координат группы
        """
        for object in self.gr_list:
            object.relative_x1 = (object.frame.x1 - self.frame.x2) / (self.frame.x2 - self.frame.x1)
            object.relative_x2 = (object.frame.x2 - self.frame.x2) / (self.frame.x2 - self.frame.x1)
            object.relative_y1 = (object.frame.y1 - self.frame.y2) / (self.frame.y2 - self.frame.y1)
            object.relative_y2 = (object.frame.y2 - self.frame.y2) / (self.frame.y2 - self.frame.y1)

    def draw(self, painter):
        """
        Отрисовка группы
        :param painter: средство рисования
        """
        for object in self.gr_list:
            object.draw(painter)

    def move(self, x, y):
        self.frame.move(x, y)
        for object in self.gr_list:
            object.move(x, y)

    def move_first_marker(self, x, y):
        self.frame.move_first_marker(x, y)
        self.resize_object()

    def move_second_marker(self, x, y):
        self.frame.move_second_marker(x, y)
        self.resize_object()

    def move_third_marker(self, x, y):
        self.frame.move_third_marker(x, y)
        self.resize_object()

    def move_fourth_marker(self, x, y):
        self.frame.move_fourth_marker(x, y)
        self.resize_object()

    def in_body(self, x, y):
        for object in self.gr_list:
            if object.in_body(x, y):
                return True
        return False

    def resize_object(self):
        """
        Метод перераспределения координат фрейма фигуры
        """
        for object in self.gr_list:
            object.frame.x1 = object.relative_x1 * (self.frame.x2 - self.frame.x1) + self.frame.x2
            object.frame.x2 = object.relative_x2 * (self.frame.x2 - self.frame.x1) + self.frame.x2
            object.frame.y1 = object.relative_y1 * (self.frame.y2 - self.frame.y1) + self.frame.y2
            object.frame.y2 = object.relative_y2 * (self.frame.y2 - self.frame.y1) + self.frame.y2
            if object.is_group:
                object.resize_object()

    def create_selection(self):
        return FramedObjSelection(self)


@t.runtime_checkable
class FigureFactory(t.Protocol):
    @property
    def figure_id(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def icon(self) -> str:
        raise NotImplementedError

    def start_figure(self, x: int, y: int) -> Figure:
        raise NotImplementedError

    def update_figure(self, f: Figure, x: int, y: int):
        raise NotImplementedError

    def complete_figure(self, f: Figure, x: int, y: int):
        raise NotImplementedError

    def cancel_figure(self, f: Figure):
        raise NotImplementedError
