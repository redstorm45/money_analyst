import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as QtCore


class EditorDialogWrapper(Qtw.QWidget):
    """
    A wrapper for the delegates to use a dialog as an editor
    maps the signals through
    """
    finished = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super(EditorDialogWrapper, self).__init__(parent)
        self.wrapped = None

    def wrap(self, wrapped):
        self.wrapped = wrapped
        wrapped.finished.connect(lambda v: self.finished.emit(v))

    def showEvent(self, e):
        return self.wrapped.show()
