import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as QtCore

from widgets.labels import LabelsWidget

DATE_FORMAT = 'yyyy-MM-dd'


class TransactionDialog(Qtw.QDialog):
    """
    A dialog used to edit a transaction
    """
    def __init__(self, parent, model_cat, desc='', category=0, amount=0, date=''):
        super(TransactionDialog, self).__init__(parent)

        self.validated = False
        self.validated_data = None
        self.model_cat = model_cat
        self.all_labels = model_cat.get_labels()

        self.setModal(True)

        edit_desc_label = Qtw.QLabel("Description:", self)
        self.edit_desc = Qtw.QLineEdit(self)

        edit_cat_label = Qtw.QLabel("Catégorie:", self)
        self.edit_cat = Qtw.QComboBox(self)
        self.edit_cat.insertItems(0, self.model_cat.get_names())
        self.edit_cat.setInsertPolicy(self.edit_cat.NoInsert)

        edit_amount_label = Qtw.QLabel("Montant (centimes):", self)
        self.edit_amount = Qtw.QLineEdit('0', self)
        self.edit_amount.textChanged.connect(self.updateAmountHint)
        self.edit_amount_hint = Qtw.QLabel('soit: 0,00€', self)

        self.edit_date = Qtw.QCalendarWidget(self)

        self.edit_labels = LabelsWidget(self, self.all_labels)

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
        layout.addWidget(edit_desc_label, 0, 0)
        layout.addWidget(self.edit_desc, 1, 0)
        layout.addWidget(edit_cat_label, 2, 0)
        layout.addWidget(self.edit_cat, 3, 0)
        layout.addWidget(edit_amount_label, 4, 0)
        layout.addWidget(self.edit_amount, 5, 0)
        layout.addWidget(self.edit_amount_hint, 6, 0)
        layout.addWidget(self.edit_date, 0, 1, 7, 1)
        layout.addWidget(self.edit_labels, 7, 0, 1, 2)
        layout.addWidget(buttons_widget, 8, 0, 1, 2)
        self.setLayout(layout)

    def updateAmountHint(self):
        try:
            val = int(self.edit_amount.text())
            S = 'soit: ' + str(val//100) + ',' + str(val%100).zfill(2) + '€'
            self.edit_amount_hint.setText(S)
        except ValueError:
            self.edit_amount_hint.setText('soit: ?')

    def setData(self, desc, category, amount, date, labels):
        self.edit_desc.setText(desc)
        self.edit_cat.setCurrentText(self.model_cat.get_name_for_id(category))
        self.edit_amount.setText(str(amount))
        self.edit_date.setSelectedDate(QtCore.QDate.fromString(date, DATE_FORMAT))
        self.edit_labels.set_labels(labels)

    def validate(self):
        if self.edit_desc.text() == '':
            box = Qtw.QMessageBox()
            box.setText('Rajoutez une description à la transaction')
            box.exec_()
            return
        try:
            amount = int(self.edit_amount.text())
        except ValueError:
            box = Qtw.QMessageBox()
            box.setText('Montant invalide')
            box.exec_()
            return
        self.validated = True
        cat_id = self.model_cat.get_id_for_name(self.edit_cat.currentText())
        date = self.edit_date.selectedDate().toString(DATE_FORMAT)
        labels = self.edit_labels.labels.copy()
        self.validated_data = (self.edit_desc.text(), cat_id, amount, date, labels)
        self.accept()
