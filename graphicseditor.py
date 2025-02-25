import sys
from PyQt5 import QtWidgets
from View import View

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    g = View()
    sys.exit(app.exec_())
