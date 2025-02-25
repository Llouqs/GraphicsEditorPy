import os
import sys
from importlib import import_module

# Загружаемые плагины
Plugins = []

class Plugin(object):
    icon_path = ""
    name = " "
    # Методы обратной связи
    def OnLoad(self):
        print(f"Плагин {self.name} подключен")

    def OnUnLoad(self):
        print(f"Плагин {self.name} отключен")


def LoadPlugins():
    """
    Загрузка всех плагинов из директории 'plugins'.
    Каждый плагин должен быть файлом Python и содержать класс, наследующий от Plugin.
    """
    plugin_dir = 'plugins'
    if not os.path.exists(plugin_dir):
        print(f"Директория '{plugin_dir}' не найдена.")
        return
    ss = os.listdir('plugins')  # Получаем список плагинов в /plugins
    sys.path.insert(0, 'plugins')  # Добавляем папку плагинов в $PATH, чтобы import_module мог их загрузить

    for s in ss:
        try:
            if os.path.splitext(s)[1] == ".py":
                plugin_module = import_module(os.path.splitext(s)[0])
                print('Найден плагин', s)
        except Exception as e:
            print(f"Ошибка при загрузке плагина {s}: {e}")

    for plugin in Plugin.__subclasses__():  # так как Plugin произведен от object, мы используем __subclasses__, чтобы найти все плагины, произведенные от этого класса
        p = plugin()  # Создаем экземпляр
        Plugins.append(p)
        p.__init__()
        p.OnLoad()  # Вызываем событие загруки этого плагина
    return

def ClearPlugins():
    for p in Plugins:
        p.OnUnLoad()
        if p.name in sys.modules:
            del sys.modules[p.name]
        Plugins.remove(p)
    return
