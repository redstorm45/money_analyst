from PyQt5.QtCore import Qt
import PyQt5.QtSql as QtSql
import PyQt5.QtCore as QtCore

from modelview.editor_wrapper import EditorDialogWrapper

from widgets.dialogs.transactions_editor import TransactionDialog


class TransactionItemDelegate(QtSql.QSqlRelationalDelegate):
    """
    A Delegate for the transactions table
    """
    updated = QtCore.pyqtSignal()

    def __init__(self):
        super(TransactionItemDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        wrapper = EditorDialogWrapper(parent)
        editor = TransactionDialog(wrapper, index.model().model_cat)
        editor.setModal(True)
        wrapper.wrap(editor)

        def finish_editor(v):
            self.commitData.emit(wrapper)
            self.closeEditor.emit(wrapper)

        wrapper.finished.connect(finish_editor)
        return wrapper

    def setEditorData(self, editor, index):
        row = index.row()
        col_desc = index.model().fieldIndex('desc')
        col_category = index.model().fieldIndex('category')
        col_amount = index.model().fieldIndex('amount')
        col_date = index.model().fieldIndex('date')
        col_id = index.model().fieldIndex('id')
        desc = index.model().index(row, col_desc).data()
        category = index.model().index(row, col_category).data(Qt.EditRole)
        amount = index.model().index(row, col_amount).data(Qt.EditRole)
        date = index.model().index(row, col_date).data()
        identifier = index.model().index(row, col_id).data()
        labels = index.model().model_lab.get_labels_for_transaction(identifier)
        editor.wrapped.setData(desc, category, amount, date, labels)

    def setModelData(self, editor, model, index):
        print('finished tr editor')
        if not editor.wrapped.validated:
            return
        row = index.row()
        col_id = index.model().fieldIndex('id')
        col_desc = index.model().fieldIndex('desc')
        col_category = index.model().fieldIndex('category')
        col_amount = index.model().fieldIndex('amount')
        col_date = index.model().fieldIndex('date')
        identifier = index.model().index(row, col_id).data()
        index.model().setData(index.model().index(row, col_desc), editor.wrapped.validated_data[0])
        index.model().setData(index.model().index(row, col_category), editor.wrapped.validated_data[1])
        index.model().setData(index.model().index(row, col_amount), editor.wrapped.validated_data[2])
        index.model().setData(index.model().index(row, col_date), editor.wrapped.validated_data[3])
        index.model().model_lab.update_link(identifier, editor.wrapped.validated_data[4])
        self.updated.emit()
