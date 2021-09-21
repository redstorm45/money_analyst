import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as QtGui


class CategoryDialog(Qtw.QDialog):
    """
    A dialog used to edit a category
    """
    def __init__(self, parent, name='', color=QtGui.QColor('#000000'), label=0):
        super(CategoryDialog, self).__init__(parent)

        self.validated = False
        self.validated_data = None

        self.setModal(True)

        edit_name_label = Qtw.QLabel("Nom de la catégorie:", self)
        self.edit_name = Qtw.QLineEdit(self)
        self.edit_name.setText(name)

        edit_color_label = Qtw.QLabel("Couleur représentative:", self)
        self.edit_color = Qtw.QLineEdit(color.name(), self)
        self.edit_color_button = Qtw.QPushButton(self.makeColorIcon(color), '', self)
        self.edit_color_button.clicked.connect(self.selectColor)

        self.edit_is_label = Qtw.QCheckBox("Etiquette", self)
        self.edit_is_label.setChecked(bool(label))

        buttons_widget = Qtw.QWidget(self)
        buttons_layout = Qtw.QHBoxLayout()
        cancel_button = Qtw.QPushButton("Annuler", buttons_widget)
        cancel_button.clicked.connect(self.reject)
        validate_button = Qtw.QPushButton("Valider", buttons_widget)
        validate_button.clicked.connect(self.validate)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(validate_button)
        buttons_widget.setLayout(buttons_layout)

        layout = Qtw.QGridLayout()
        layout.addWidget(edit_name_label, 0, 0, 1, 2)
        layout.addWidget(self.edit_name, 1, 0, 1, 2)
        layout.addWidget(edit_color_label, 2, 0, 1, 2)
        layout.addWidget(self.edit_color, 3, 0)
        layout.addWidget(self.edit_color_button, 3, 1)
        layout.addWidget(self.edit_is_label, 4, 0, 1, 2)
        layout.addWidget(buttons_widget, 5, 0, 1, 2)
        self.setLayout(layout)

    def setData(self, name, color_name, label):
        self.edit_name.setText(name)
        self.edit_color.setText(color_name)
        self.edit_color_button.setIcon(self.makeColorIcon(QtGui.QColor(color_name)))
        self.edit_is_label.setChecked(bool(label))

    def selectColor(self):
        initial = QtGui.QColor(self.edit_color.text())
        new = Qtw.QColorDialog.getColor(initial, self)
        self.edit_color.setText(new.name())
        self.edit_color_button.setIcon(self.makeColorIcon(new))

    def makeColorIcon(self, color):
        pix = QtGui.QPixmap(64, 64)
        pix.fill(color)
        return QtGui.QIcon(pix)

    def validate(self):
        if self.edit_name.text() == '':
            box = Qtw.QMessageBox()
            box.setText('Rajoutez un nom à la catégorie')
            box.exec_()
            return
        self.validated = True
        self.validated_data = (self.edit_name.text(), self.edit_color.text(), int(self.edit_is_label.isChecked()))
        self.accept()

