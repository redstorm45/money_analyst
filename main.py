import sys
import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

from widgets.tabs.data import DataWidget
from widgets.tabs.plot import PlotWidget
import migrations


class Window(Qtw.QMainWindow):
    """
    A Window widget is the main class for the application,
    it contains mainly the data and plot widgets in their tabs
    """
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        migrations.init_db()

        raw = DataWidget(self)
        plot = PlotWidget(self, raw.models())
        raw.updated.connect(plot.extract)

        tabs = Qtw.QTabWidget(self)
        tabs.setTabPosition(tabs.West)
        tabs.addTab(raw, "Données")
        tabs.addTab(plot, "Graphiques")

        self.setCentralWidget(tabs)


if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
