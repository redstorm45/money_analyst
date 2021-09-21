import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as QtCore

from modelview.editor_wrapper import EditorDialogWrapper

from widgets.dialogs.categories_editor import CategoryDialog


class CategoryItemDelegate(Qtw.QStyledItemDelegate):
    """
    A Delegate for the category table
    """
    updated = QtCore.pyqtSignal()

    def __init__(self):
        super(CategoryItemDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        wrapper = EditorDialogWrapper(parent)
        editor = CategoryDialog(wrapper)
        editor.setModal(True)
        wrapper.wrap(editor)

        def finish_editor(v):
            self.commitData.emit(wrapper)
            self.closeEditor.emit(wrapper)

        wrapper.finished.connect(finish_editor)
        return wrapper

    def setEditorData(self, editor, index):
        row = index.row()
        col_name = index.model().fieldIndex('name')
        col_color = index.model().fieldIndex('color')
        col_label = index.model().fieldIndex('label')
        name = index.model().index(row, col_name).data()
        color = index.model().index(row, col_color).data()
        label = index.model().index(row, col_label).data()
        editor.wrapped.setData(name, color, label)

    def setModelData(self, editor, model, index):
        if not editor.wrapped.validated:
            return
        row = index.row()
        col_name = index.model().fieldIndex('name')
        col_color = index.model().fieldIndex('color')
        col_label = index.model().fieldIndex('label')
        index.model().setData(index.model().index(row, col_name), editor.wrapped.validated_data[0])
        index.model().setData(index.model().index(row, col_color), editor.wrapped.validated_data[1])
        index.model().setData(index.model().index(row, col_label), editor.wrapped.validated_data[2])
        self.updated.emit()
