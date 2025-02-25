from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from EditorController import EditorController
from EditorModel import EditorModel
import plugin
from ObjectFactory import LineFactory, EllipseFactory, RectangleFactory


class GraphicsScene(QGraphicsScene):
    clicked = pyqtSignal(QPointF)
    released = pyqtSignal(QPointF)
    move = pyqtSignal(QPointF)
    keyPressed = pyqtSignal(bool)

    def mousePressEvent(self, event):
        """
        Событие нажатия мышки
        """
        sp = event.scenePos()
        self.clicked.emit(sp)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Событие при разжатии мыши
        """
        sp = event.scenePos()
        self.released.emit(sp)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """
        Событие передвижения нажатой кнопки мыши
        """
        sp = event.scenePos()
        self.move.emit(sp)
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        """
        Событие нажатия клавиши
        """
        ctrl = False
        if event.modifiers() & Qt.ControlModifier:
            ctrl = True
        self.keyPressed.emit(ctrl)


class View(QMainWindow):
    """
    Класс представление редактора
    """

    def __init__(self):
        super().__init__()

        self.state = ""
        # Определение размеров и title окна GraphObject
        self.resize(820, 650)
        self.setWindowTitle('GraphicsEditor')
        # Виджет для отображения GraphicsScene()
        self.grview = QGraphicsView()
        self.grview.scale(1, -1)
        # Фрейм на котором происходит отрисовка
        self.scene = GraphicsScene()
        self.scene.setSceneRect(-250, -250, 500, 500)
        # Цвета и размер по умолчанию
        self.pen_color = Qt.black
        self.brush_color = Qt.black
        self.value_width = 2
        # Включаем поддержку отслеживания нажатия/движения мыши
        self.setMouseTracking(True)
        # Подключаем GraphicsScene к QGraphicsView
        self.grview.setScene(self.scene)
        # Подключаем actions к сцене
        self.set_actions()
        # Подключаем дополнительные виджеты
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.grview)

        # Подключаем основу и контур
        self.x1 = -250
        self.y1 = -250
        self.x2 = 500
        self.y2 = 500

        # Инициализация контроллера
        self.controller = EditorController(EditorModel(), self.x1, self.y1, self.x2, self.y2, self.scene)

        # Словарь фабрик
        self.factory_dict = dict()
        self.factory_dict["LineFactory"] = LineFactory(self.controller.model.store)
        self.factory_dict["EllipseFactory"] = EllipseFactory(self.controller.model.store)
        self.factory_dict["RectangleFactory"] = RectangleFactory(self.controller.model.store)

        # Добавляем атрибуты для плагинов
        self.plugin_is_load = False
        self.plugin_buttons = []

        # Подключаем методы по нажатию на action
        self.scene.clicked.connect(self.point1)
        self.scene.released.connect(self.point2)
        self.scene.move.connect(self.point3)

        # Подключаем методы по нажатию на action в toolbar
        self.plugin_action.triggered.connect(self.click_plugin)
        self.trash_action.triggered.connect(self.clear)
        self.line_action.triggered.connect(self.click_line)
        self.rect_action.triggered.connect(self.click_rect)
        self.select_action.triggered.connect(self.click_select)
        self.circle_action.triggered.connect(self.click_circle)
        self.color_selection.triggered.connect(self.open_color_dialog)
        self.circuit_selection.triggered.connect(self.open_color_brush)
        self.spin_box.valueChanged.connect(self.spinbox_changed)
        self.group_action.triggered.connect(self.group_event)
        self.ungroup_action.triggered.connect(self.ungroup_event)

        self.show()

    def set_actions(self):
        # Тул бар
        self.figure_toolbar = QToolBar("figure")
        self.figure_toolbar.setIconSize(QSize(14, 14))
        self.basicToolBar = self.addToolBar(self.figure_toolbar)
        # кнопка line
        self.line_action = QAction(QIcon("images/line.png"), 'line', self)
        self.line_action.setStatusTip("line")
        self.figure_toolbar.addAction(self.line_action)
        # кнопка rectangle
        self.rect_action = QAction(QIcon("images/rect.png"), 'rectangle', self)
        self.rect_action.setStatusTip("rect")
        self.figure_toolbar.addAction(self.rect_action)
        # кнопка круг
        self.circle_action = QAction(QIcon("images/circle.ico"), 'circle', self)
        self.circle_action.setStatusTip("circle")
        self.figure_toolbar.addAction(self.circle_action)
        # кнопка для плагинов
        self.plugin_action = QAction(QIcon("images/Plugins.png"), 'plugin', self)
        self.plugin_action.setStatusTip("plugin")
        self.figure_toolbar.addAction(self.plugin_action)
        # кнопка select
        self.select_action = QAction(QIcon("images/select.ico"), 'select', self)
        self.select_action.setStatusTip("select")
        self.figure_toolbar.addAction(self.select_action)
        # group
        self.group_action = QAction(QIcon("images/group.ico"), 'group', self)
        self.group_action.setStatusTip("group")
        self.figure_toolbar.addAction(self.group_action)
        # ungroup
        self.ungroup_action = QAction(QIcon("images/ungroup.ico"), 'ungroup', self)
        self.ungroup_action.setStatusTip("ungroup")
        self.figure_toolbar.addAction(self.ungroup_action)
        # кнопка очистки
        self.trash_action = QAction(QIcon("images/trash.png"), 'trash', self)
        self.trash_action.setStatusTip("trash")
        self.figure_toolbar.addAction(self.trash_action)
        # кнопка выбора цвета
        self.color_selection = QAction('Сменить цвет \nфигуры', self)
        self.color_selection.setStatusTip("color")
        self.figure_toolbar.addAction(self.color_selection)
        # кнопка выбора цвета
        self.circuit_selection = QAction('Сменить цвет \nконтура', self)
        self.circuit_selection.setStatusTip("color")
        self.figure_toolbar.addAction(self.circuit_selection)
        self.label = QLabel(self)

        self.label.setText("Толщина ручки: ")
        self.figure_toolbar.addWidget(self.label)
        # спин-бокс
        self.spin_box = QSpinBox(self)
        self.spin_box.setValue(self.value_width)
        self.figure_toolbar.addWidget(self.spin_box)

    def clear(self):
        """
        Метод очистки сцены
        """
        self.controller.clear()

    def open_color_dialog(self):
        """
        Смена цвета фигуры
        """
        brush_color = QColorDialog.getColor()
        self.controller.set_brush_prop(brush_color)

    def open_color_brush(self):
        """
        Смена цвета контура фигуры
        """
        self.pen_color = QColorDialog.getColor()
        self.controller.set_pen_color(self.pen_color)

    def spinbox_changed(self, value):
        """
        Смена толщины ручки
        """
        self.value_width = value
        self.controller.set_pen_width(self.value_width)

    def click_line(self):
        """
        Смена состояния на line
        """
        self.controller.set_object_factory(self.factory_dict["LineFactory"])
        self.controller.change_state("create")

    def click_rect(self):
        """
        Смена состояния на rect
        """
        self.controller.set_object_factory(self.factory_dict["RectangleFactory"])
        self.controller.change_state("create")

    def click_circle(self):
        """
        Смена состояния на circle
        """
        self.controller.set_object_factory(self.factory_dict["EllipseFactory"])
        self.controller.change_state("create")

    def click_plugin(self):
        if self.plugin_is_load:
            print("Плагины уже загружены, выгружаем...")
            self.unload_plugins()
        else:
            print("Плагины еще не загружены, загружаем...")
            self.load_plugins()

    def load_plugins(self):
        plugin.LoadPlugins()

        for plug in plugin.Plugins:
            if plug.name in self.factory_dict:
                continue  # Плагин уже загружен

            self.factory_dict[plug.name] = plug
            plug.store = self.controller.model.store

            action = QAction(QIcon(plug.icon_path), plug.name, self)
            action.setStatusTip(f"Create {plug.name}")

            method_name = f"click_{plug.name.lower()}"
            setattr(self, method_name, lambda checked=False, p=plug: self.click_dynamic_plugin(p))
            action.triggered.connect(getattr(self, method_name))

            plugin_button = QToolButton(self)
            plugin_button.setDefaultAction(action)
            plugin_button.setIcon(QIcon(plug.icon_path))
            plugin_button.setToolButtonStyle(Qt.ToolButtonIconOnly)

            # Добавляем кнопку в тулбар и в список
            self.figure_toolbar.insertWidget(self.plugin_action, plugin_button)
            self.plugin_buttons.append((plugin_button, action))  # Сохраняем кнопку и действие

        self.controller.change_state("empty")
        self.plugin_is_load = True  # Плагины загружены

    def unload_plugins(self):
        print("Начинаем выгрузку плагинов...")

        # Удаляем кнопки плагинов из тулбара и отключаем действия
        for button, action in self.plugin_buttons:
            self.figure_toolbar.removeAction(action)  # Удаляем действие из тулбара
            button.deleteLater()  # Удаляем саму кнопку (освобождаем ресурсы)

        # Очищаем список кнопок
        self.plugin_buttons.clear()

        # Очищаем список фабрик
        for plug in plugin.Plugins:
            if plug.name in self.factory_dict:
                self.factory_dict.pop(plug.name)

        print("Выгружаем плагины...")
        plugin.ClearPlugins()
        self.controller.change_state("empty")
        self.plugin_is_load = False  # Плагины выгружены

    def click_dynamic_plugin(self, plug):
        print(f"Клик по плагину: {plug.name}")
        if plug.name not in self.factory_dict:
            print(f"Плагин {plug.name} не найден!")
            return

        self.controller.set_object_factory(self.factory_dict[plug.name])
        self.controller.change_state("create")

    def click_select(self):
        """
        Смена состояния на select
        """
        self.controller.change_state("empty")

    def point1(self, p):
        """
        Получение координат
        при нажатии мышки
        """
        self.x1 = p.x()
        self.y1 = p.y()
        self.controller.mouse_clicked(self.x1, self.y1)

    def point2(self, p):
        """
        Получение координат
        при разжатии мышки
        """
        self.x2 = p.x()
        self.y2 = p.y()
        self.controller.mouse_realised(self.x2, self.y2)

    def point3(self, p):
        self.x3 = p.x()
        self.y3 = p.y()
        self.controller.mouse_move(self.x3, self.y3)

    def keyPressEvent(self, e):
        """
        Событие нажатия клавиши клавиатуры
        """
        if e.key() == QtCore.Qt.Key_Control:
            self.controller.ctrl_on()

    def keyReleaseEvent(self, event):
        """
        Событие разжатия клавиши клавиатуры
        """
        if event.key() == QtCore.Qt.Key_Control:
            self.controller.ctrl_off()

    def group_event(self):
        """
        Метод группировки фигур
        """
        self.controller.group()

    def ungroup_event(self):
        """
        Метод разгруппировки фигур
        """
        self.controller.ungroup_state()
        self.controller.ungroup()
