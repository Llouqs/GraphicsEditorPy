from PyQt5 import QtGui
from PyQt5.QtGui import *
from Frame import Frame
from GrafObject import GrafObject, Group
from Painter import Painter
from Figures import Line, Rectangle, Ellipse
from Properties import Properties, BrushProps, PenColor, PenWidth
from Painter import Painter
import copy


class EditorModel:
    """
    Класс модель редактора
    """

    def __init__(self):
        self.painter = Painter()
        self.store = Store()
        self.selection_store = SelectionStore()
        self.object_factory = ObjectFactory(self.store)
        self.scene = Scene(self.store, self.painter, self.selection_store)
        self.object_state = False
        self.move_state = False
        self.curr_object = None
        self.last_object = False

    def try_select(self, x, y):
        """
        Попытка выделения объекта при нажатии на граф сцену
        :param x: координата х при нажатии мышки
        :param y: координата y при нажатии мышки
        """
        self.object_state = False
        for object in reversed(self.store.list):
            if object.in_body(x, y):
                self.selection_store.list.append(object.create_selection())
                object.select = True
                self.scene.repaint()
                self.curr_object = object
                return True
        self.curr_object = None
        return False

    def try_grab(self, x, y):
        """
        Попытка потащить за маркер выделенной фигуры
        :param x: координата х при нажатии мышки
        :param y: координата y при нажатии мышки
        """
        return self.selection_store.try_grab(x, y)

    def try_drag_to(self, x, y):
        """
        Перерисовка при перетаскивании маркера
        :param x: координата х при нажатии мышки
        :param y: координата y при нажатии мышки
        """
        self.selection_store.try_drag_to(x, y)
        if self.selection_store.drag_state:
            self.scene.repaint()

    def clear_selection(self):
        """
        Очистка селекторов объектов
        """
        self.selection_store.list = []
        self.curr_object = None
        for object in self.store.list:
            object.select = False
        self.scene.repaint()

    def set_port(self, x1, y1, x2, y2, painter):
        """
        Установка средства рисования
        :param painter: средство рисования
        """
        self.painter.set_port(x1, y1, x2, y2, painter)

    def create_object(self, x, y):
        """
        Создание объекта фигуры (метод делегат)
        :param x: координата х при нажатии мышки
        :param y: координата y при нажатии мышки
        :return:
        """
        self.object_factory.create_object(x, y)
        self.selection_store.list.append(self.store.list[len(self.store.list) - 1].create_selection())
        self.scene.repaint()
        self.curr_object = self.store.list[-1]

    def set_pen_color(self, pen_color):
        """
        установка свойств ручки (метод делегат)
        :param pen_color: цвет ручки
        """
        self.object_factory.set_pen_color(pen_color)
        if self.curr_object is not None:
            prop = Properties()
            prop.prop_group.list_prop.append(self.object_factory.pen_color)
            self.curr_object.change_properties(prop)
            self.repaint()

    def set_pen_width(self, pen_width):
        """
        установка свойств ручки (метод делегат)
        :param pen_width: толщина ручки
        """
        self.object_factory.set_pen_width(pen_width)
        if self.curr_object is not None:
            prop = Properties()
            prop.prop_group.list_prop.append(self.object_factory.pen_width)
            self.curr_object.change_properties(prop)
            self.repaint()

    def set_brush_prop(self, brush_prop):
        """
        установка свойства заливки (метод делегат)
        :param brush_prop: заливка фигуры
        :return:
        """
        self.object_factory.set_brush_prop(brush_prop)
        if self.curr_object is not None:
            prop = Properties()
            prop.prop_group.list_prop.append(self.object_factory.brush_prop)
            self.curr_object.change_properties(prop)
            self.repaint()

    def set_object_type(self, object):
        """
        Установка типа объекта (метод делегат)
        :param object: тип объекта
        """
        self.object_factory.set_object_type(object)

    def clear(self):
        """
        Очистка хранилища редактора
        :return:
        """
        self.store.clear()
        self.selection_store.list = []
        self.scene.repaint()

    def repaint(self):
        """
        Метод перерисовки сцены
        """
        self.scene.repaint()

    def group(self):
        """
        Метод группировки фигур
        """
        list_object = []
        for object in self.store.list:
            if object.select:
                object.gr_state = True
                list_object.append(object)

        group = Group(list_object)
        self.store.list.append(group)

        list = []
        self.selection_store.clear_selection()
        for object in self.store.list:
            if object not in list_object:
                list.append(object)

        self.store.list.clear()
        self.store.list = list
        self.selection_store.list.append(group.create_selection())

        self.scene.repaint()

    def ungroup(self):
        """
        Метод разгруппировки фигур
        """
        obj = None
        for object in self.store.list:
            if isinstance(object, Group) and object.select:
                obj = object
        if obj != None:
            self.selection_store.clear_selection()
            self.repaint()
            for object in obj.gr_list:
                self.store.list.append(object)
            self.store.list.remove(obj)


class ObjectFactory:
    """
    Класс фабрики объектов
    """

    def __init__(self, store):
        self.object_type = None
        self.pen_width = PenWidth(3)
        self.pen_color = PenColor(QtGui.QColor("black"))
        self.brush_prop = BrushProps(QtGui.QColor("black"))
        self.store = store

    def set_pen_width(self, pen_width):
        """
        Установка свойств ручки
        :param pen_width: толщина ручки
        """
        self.pen_width = PenWidth(pen_width)

    def set_pen_color(self, pen_color):
        """
        Установка свойств ручки
        :param pen_color: цвет ручки
        """
        self.pen_color = PenColor(pen_color)

    def set_brush_prop(self, brush_prop):
        """
        Установка свойств ручки
        :param brush_prop: заливка
        """
        self.brush_prop = BrushProps(brush_prop)

    def set_object_type(self, object):
        """
        Установка типа объекта
        :param object: тип
        """
        self.object_type = object

    def create_object(self, x, y):
        """
        Метод создания объекта
        :param x: координата х
        :param y: координата y
        """
        frame = Frame(x, y, x, y)
        prop = Properties()
        prop.prop_group.list_prop.append(self.pen_color)
        prop.prop_group.list_prop.append(self.pen_width)
        prop.prop_group.list_prop.append(self.brush_prop)

        if self.object_type == "rect":
            rect = Rectangle(frame, prop)
            self.store.add(rect)

        elif self.object_type == "ellipse":
            ellipse = Ellipse(frame, prop)
            self.store.add(ellipse)

        elif self.object_type == "line":
            line = Line(frame, prop)
            self.store.add(line)


class Store:
    """
    Класс хранилище объектов
    """

    def __init__(self):
        self.list = []

    def add(self, object):
        """
        Метод добавления объекта в хранилище
        :param object: объект-фигура
        """
        self.list.append(object)

    def clear(self):
        """
        Очистка хранилища
        """
        self.list = []


class SelectionStore:
    """
    Класс хранилища селекторов объектов
    """

    def __init__(self):
        self.list = []

    def clear_selection(self):
        """
        Очистка хранилища селекторов
        """
        self.list = []

    def try_grab(self, x, y):
        """
        Попытка потащить за маркер выделенной фигуры
        :param x: координата х при нажатии мышки
        :param y: координата y при нажатии мышки
        """
        self.grabbed = False
        for select in self.list:
            if select.try_grab(x, y):
                self.grabbed = True
        return self.grabbed

    def try_drag_to(self, x, y):
        """
        Перерисовка при перетаскивании маркера
        :param x: координата х при нажатии мышки
        :param y: координата y при нажатии мышки
        """
        self.drag_state = False
        for select in self.list:
            select.try_drag_to(x, y)
            self.drag_state = True
        self.list[0].set_point(x, y)


class Scene:
    """
    Класс сцены
    """

    def __init__(self, store, painter, selection_store):
        self.store = store
        self.painter = painter
        self.selection_store = selection_store

    def repaint(self):
        """
        Метод перерисовки граф примитивов
        """

        self.painter.clear()
        for object in self.store.list:
            object.draw(self.painter)
        for select in self.selection_store.list:
            select.draw(self.painter)
