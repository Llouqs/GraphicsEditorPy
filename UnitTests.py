from PyQt5 import QtWidgets

import plugin
from EditorModel import Store
from View import View
import sys
import unittest
from ObjectFactory import *

# Загрузку плагинов достаточно произвести один раз, т.к. функция setUp запускается перед каждым тестом
plugin.LoadPlugins()


# Класс для тестирования фабрик фигур
class TestObjectFactory(unittest.TestCase):
    # Переопределяем метод инициализации полей перед каждым тестом (класса предка unittest.TestCase)
    def setUp(self):
        # Создадим множество из фабрик чтобы убедится что все они работают корретно
        self.factory_set = set()
        # Так же создадим для них единое хранилище
        self.store = Store()
        # Добавим в лист фабрики по умолчанию
        self.factory_set.add(RectangleFactory(self.store))  # Создаем экземпляр фабрики прямоугольников
        self.factory_set.add(EllipseFactory(self.store))  # Создаем экземпляр фабрики эллипсов
        self.factory_set.add(LineFactory(self.store))  # Создаем экземпляр фабрики линий
        # Также добавим в этот лист фабрики из плагинов
        for plug in plugin.Plugins:
            # При загрузке плагинов экземпляры создаются с пустым полем Store, т.к. не знают об общем хранилище
            plug.store = self.store
            self.factory_set.add(plug)
        # Далее тестируем все фабрики на одинаковое поведение

    # тестирование создания фигуры
    def test_create_object(self):
        for object_factory in self.factory_set:
            # это менеджер контекста, если в итерации цикла произойдет ошибка, то он выведет информацию о фабрике
            with self.subTest(object_factory=object_factory.name):
                object_factory.create_object(10, 20)  # При создании указываются координаты объекта
                # метод для тестирования принимает на вход два значения bool
                self.assertEqual(len(self.store.list) == 1, True)
                object_factory.store.clear()  # Очищаем лист для дальнейшего тестирования

    # тестирование изменения цвета контура
    def test_set_pen_color(self):
        for object_factory in self.factory_set:
            # это менеджер контекста, если в итерации цикла произойдет ошибка, то он выведет информацию о фабрике
            with self.subTest(object_factory=object_factory.name):
                object_factory.set_pen_color(QtGui.QColor("black"))
                object_factory.create_object(10, 20)
                object_factory.set_pen_color(QtGui.QColor("red"))
                object_factory.create_object(40, 30)
                flag = self.store.list[0].pen_color == self.store.list[1].pen_color
                self.assertEqual(flag, False)
                object_factory.store.clear()

    # тестирование изменения толщины контура
    def test_set_pen_width(self):
        for object_factory in self.factory_set:
            # это менеджер контекста, если в итерации цикла произойдет ошибка, то он выведет информацию о фабрике
            with self.subTest(object_factory=object_factory.name):
                object_factory.set_pen_width(1)
                object_factory.create_object(10, 20)
                object_factory.set_pen_width(10)
                object_factory.create_object(40, 30)
                flag = self.store.list[0].pen_width == self.store.list[1].pen_width
                self.assertEqual(flag, False)
                object_factory.store.clear()

    # тестирование изменения цвета заливки
    def test_set_brush_color(self):
        for object_factory in self.factory_set:
            # это менеджер контекста, если в итерации цикла произойдет ошибка, то он выведет информацию о фабрике
            with self.subTest(object_factory=object_factory.name):
                object_factory.set_brush_prop(QtGui.QColor("black"))
                object_factory.create_object(10, 20)
                object_factory.set_brush_prop(QtGui.QColor("red"))
                object_factory.create_object(40, 30)
                flag = self.store.list[0].brush_color == self.store.list[1].brush_color
                self.assertEqual(flag, False)
                object_factory.store.clear()


# Вызываем класс тестирования
if __name__ == "__main__":
    unittest.main()
