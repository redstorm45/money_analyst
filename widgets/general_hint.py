import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as QtGui


class GeneralHintWidget(Qtw.QWidget):
    """
    Widget for hints when hovering an item in the graph
    """
    def __init__(self, parent=None):
        super(GeneralHintWidget, self).__init__(parent)
        self.group = Qtw.QGroupBox(self)
        layout_group = Qtw.QVBoxLayout()
        self.text = Qtw.QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setMinimumSize(200, 400)
        self.text.setFrameStyle(self.text.NoFrame)
        # self.text.setBackgroundRole(QtGui.QPalette.Text)
        pal = self.palette()
        pal.setColor(pal.Base, QtGui.QColor("#f9f6f3"))
        self.text.setPalette(pal)
        # self.text.setAutoFillBackground(True)
        layout_group.addWidget(self.text)
        self.group.setLayout(layout_group)

        layout = Qtw.QVBoxLayout()
        layout.addWidget(self.group)
        self.setLayout(layout)

        self.update_item([None])

    def update_item(self, item_w):
        item = item_w[0]
        if item is None:
            self.group.setTitle("?")
            self.text.setText("Sélectionnez un élément")
            return
        if item.info is None:
            self.group.setTitle("?")
            self.text.setText("Pas d'information")
            return
        self.group.setTitle(item.info["title"])
        self.text.setText(item.info["text"])
