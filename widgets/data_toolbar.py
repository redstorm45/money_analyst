import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui


class DataToolbarWidget(Qtw.QWidget):
    """
    The widget used for the toolbar in the data tab.
    it has an add, edit and remove button.
    """
    new_entry = QtCore.pyqtSignal()
    mod_entry = QtCore.pyqtSignal()
    del_entry = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(DataToolbarWidget, self).__init__(parent)
        layout = Qtw.QVBoxLayout()
        self.setLayout(layout)

        layout.addStretch()

        buttonNew = Qtw.QPushButton(QtGui.QIcon("icons/plus.png"), '', self)
        buttonNew.setStyleSheet("padding:10px;")
        buttonNew.clicked.connect(self.new_entry)
        layout.addWidget(buttonNew)

        buttonEdit = Qtw.QPushButton(QtGui.QIcon("icons/pen.png"), '', self)
        buttonEdit.setStyleSheet("padding:10px;")
        buttonEdit.clicked.connect(self.mod_entry)
        layout.addWidget(buttonEdit)

        buttonDel = Qtw.QPushButton(QtGui.QIcon("icons/trash.png"), '', self)
        buttonDel.setStyleSheet("padding:10px;")
        buttonDel.clicked.connect(self.del_entry)
        layout.addWidget(buttonDel)

        layout.addStretch()
