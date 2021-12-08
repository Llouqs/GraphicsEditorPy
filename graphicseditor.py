from PyQt5 import QtWidgets
from View import View
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    g = View()
    sys.exit(app.exec_())
