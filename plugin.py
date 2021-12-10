import os
import sys

# Экземпляры загруженных плагинов
Plugins = []


# Базовый класс плагина
class Plugin(object):
    name = " "

    # Методы обратной связи
    def OnLoad(self):
        print(f"Плагин {self.name} подключен")

    def OnUnLoad(self):
        print(f"Плагин {self.name} отключен")


def LoadPlugins():
    ss = os.listdir('plugins')  # Получаем список плагинов в /plugins
    sys.path.insert(0, 'plugins')  # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить

    for s in ss:
        print('Найден плагин', s)
        __import__(os.path.splitext(s)[0])  # Импортируем исходник плагина

    for plugin in Plugin.__subclasses__():  # так как Plugin произведен от object, мы используем __subclasses__, чтобы найти все плагины, произведенные от этого класса
        p = plugin()  # Создаем экземпляр
        Plugins.append(p)
        p.__init__()
        p.OnLoad()  # Вызываем событие загруки этого плагина
    return


def DelPlugin(p):
    p.OnUnLoad()
    if p.name in sys.modules:
        del sys.modules[p.name]
    Plugins.remove(p)
    return
