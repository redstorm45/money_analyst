import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as QtCore

from modelview.models.categories import CategoriesTableModel
from modelview.models.labels import LabelsTableModel
from modelview.models.transactions import TransactionsTableModel

from modelview.delegates.categories import CategoryItemDelegate
from modelview.delegates.transactions import TransactionItemDelegate

from widgets.data_toolbar import DataToolbarWidget

from widgets.dialogs.categories_editor import CategoryDialog
from widgets.dialogs.transactions_editor import TransactionDialog


class DataWidget(Qtw.QTabWidget):
    """
    The widget for the full data tab.
    Has a categories and transaction tab
    """
    updated = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(DataWidget, self).__init__(parent)

        # model
        model_cat = CategoriesTableModel()
        model_cat.setEditStrategy(model_cat.OnFieldChange)
        model_cat.select()

        model_lab = LabelsTableModel()
        model_lab.setEditStrategy(model_lab.OnFieldChange)
        model_lab.select()

        model_tr = TransactionsTableModel(model_cat, model_lab)
        model_tr.setEditStrategy(model_tr.OnFieldChange)
        model_tr.select()

        # view
        self.categories = Qtw.QTableView(self)
        self.categories.setModel(model_cat)
        self.categories.setSelectionBehavior(self.categories.SelectRows)
        category_delegate = CategoryItemDelegate()
        category_delegate.updated.connect(self.updated.emit)
        self.categories.setItemDelegate(category_delegate)
        self.categories.show()

        self.transactions = Qtw.QTableView(self)
        self.transactions.setModel(model_tr)
        self.transactions.setSelectionBehavior(self.transactions.SelectRows)
        transaction_delegate = TransactionItemDelegate()
        transaction_delegate.updated.connect(self.updated.emit)
        self.transactions.setItemDelegate(transaction_delegate)
        self.transactions.show()
        self.transactions.hideColumn(model_tr.fieldIndex('id'))

        # frames
        cat_frame = Qtw.QWidget(self)
        cat_layout = Qtw.QHBoxLayout()
        cat_layout.addWidget(self.categories)
        cat_toolbar = DataToolbarWidget(cat_frame)
        cat_toolbar.new_entry.connect(self.new_category)
        cat_toolbar.mod_entry.connect(self.edit_category)
        cat_toolbar.del_entry.connect(self.delete_category)
        cat_layout.addWidget(cat_toolbar)
        cat_frame.setLayout(cat_layout)

        tr_frame = Qtw.QWidget(self)
        tr_layout = Qtw.QHBoxLayout()
        tr_layout.addWidget(self.transactions)
        tr_toolbar = DataToolbarWidget(tr_frame)
        tr_toolbar.new_entry.connect(self.new_transaction)
        tr_toolbar.mod_entry.connect(self.edit_transaction)
        tr_toolbar.del_entry.connect(self.delete_transaction)
        tr_layout.addWidget(tr_toolbar)
        tr_frame.setLayout(tr_layout)

        self.setTabPosition(self.West)
        self.addTab(cat_frame, "Categories")
        self.addTab(tr_frame, "Transactions")

    def new_category(self):
        D = CategoryDialog(self)
        D.exec_()
        if D.validated:
            name, color, label = D.validated_data
            record = self.categories.model().record()
            record.remove(record.indexOf('id'))
            record.setValue('name', name)
            record.setValue('color', color)
            record.setValue('label', label)
            if not self.categories.model().insertRecord(-1, record):
                print('insert failed')
            else:
                self.updated.emit()
        else:
            print("canceled")

    def models(self):
        return {
            "categories": self.categories.model(),
            "transactions": self.transactions.model(),
            "labels": self.transactions.model().model_lab
        }

    def edit_category(self):
        index = self.categories.currentIndex()
        if index.isValid():
            self.categories.edit(index)

    def delete_category(self):
        index = self.categories.currentIndex()
        if index.isValid():
            category_id = index.model().data(index.model().index(index.row(), index.model().fieldIndex('id')))
            tr_qty = self.transactions.model().get_qty_for_category(category_id)
            questionBox = Qtw.QMessageBox(self)
            questionBox.setIcon(Qtw.QMessageBox.Question)
            questionBox.setWindowTitle("Suppression")
            questionBox.setText("êtes-vous sûr de vouloir supprimer cette catégorie, associée à "+str(tr_qty)+" transactions?")
            yes_bt = questionBox.addButton("Oui", Qtw.QMessageBox.AcceptRole)
            questionBox.addButton("Non", Qtw.QMessageBox.RejectRole)
            questionBox.exec_()
            if questionBox.clickedButton() == yes_bt:
                if tr_qty > 0:
                    self.transactions.model().remove_all_category(category_id)
                    self.transactions.model().submitAll()

                if self.categories.model().removeRow(index.row()):
                    self.categories.model().submitAll()
                    self.categories.model().database().commit()
                    self.categories.model().select()
                    if tr_qty > 0:
                        self.transactions.model().select()
                    print('apply')
                    self.updated.emit()
                else:
                    self.categories.model().revertAll()
                    print('revert')
            else:
                print('cancel suppr')

    def new_transaction(self):
        D = TransactionDialog(self, self.categories.model())
        D.exec_()
        if D.validated:
            desc, cat_id, amount, date, labels = D.validated_data
            record = self.transactions.model().record()
            record.remove(record.indexOf('id'))
            record.setValue('desc', desc)
            record.setValue('category_id', cat_id)
            record.setValue('amount', amount)
            record.setValue('date', date)
            if not self.transactions.model().insertRecord(-1, record):
                print('insert failed')
            else:
                transaction_id = self.transactions.model().query().lastInsertId()
                print("insert tr at id:", transaction_id)
                self.transactions.model().model_lab.update_link(transaction_id, labels)
                self.updated.emit()
        else:
            print('canceled')

    def edit_transaction(self):
        index = self.transactions.currentIndex()
        if index.isValid():
            self.transactions.edit(index)

    def delete_transaction(self):
        selection = self.transactions.selectionModel()
        index = self.transactions.currentIndex()
        if index.isValid():
            selected_rows = len(selection.selectedRows())
            questionBox = Qtw.QMessageBox(self)
            questionBox.setIcon(Qtw.QMessageBox.Question)
            if selected_rows == 1:
                questionBox.setWindowTitle("Suppression d'une transaction")
                questionBox.setText("êtes-vous sûr de vouloir supprimer cette transaction?")
            else:
                questionBox.setWindowTitle("Suppression de "+str(selected_rows)+" transactions")
                questionBox.setText("êtes-vous sûr de vouloir supprimer ces "+str(selected_rows)+" transactions?")
            yes_bt = questionBox.addButton("Oui", Qtw.QMessageBox.AcceptRole)
            questionBox.addButton("Non", Qtw.QMessageBox.RejectRole)
            questionBox.exec_()
            if questionBox.clickedButton() == yes_bt:
                if all(self.transactions.model().removeRow(k) for k in sorted([i.row() for i in selection.selectedRows()], reverse=True)):
                    self.transactions.model().submitAll()
                    self.transactions.model().database().commit()
                    self.transactions.model().select()
                    print('apply')
                    self.updated.emit()
                else:
                    self.transactions.model().revertAll()
                    print('revert')
            else:
                print('cancel suppr')
