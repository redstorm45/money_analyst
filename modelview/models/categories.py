from PyQt5.QtCore import Qt
import PyQt5.QtSql as QtSql
import PyQt5.QtGui as QtGui


class CategoriesTableModel(QtSql.QSqlTableModel):
    """
    A Model for the table of categories
    """
    def __init__(self):
        super(CategoriesTableModel, self).__init__()
        self.setTable("categories")

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.BackgroundColorRole and index.column() == 2:
            return QtGui.QColor(self.data(index))
        return super(CategoriesTableModel, self).data(index, role)

    def get_names(self):
        name_column = self.fieldIndex('name')
        names = []
        for r in range(self.rowCount()):
            names.append(self.data(self.index(r, name_column), Qt.DisplayRole))
        return names

    def get_id_for_name(self, name):
        id_column = self.fieldIndex('id')
        name_column = self.fieldIndex('name')
        for r in range(self.rowCount()):
            if self.data(self.index(r, name_column), Qt.DisplayRole) == name:
                return self.data(self.index(r, id_column), Qt.DisplayRole)
        return 0

    def get_name_for_id(self, index):
        id_column = self.fieldIndex('id')
        name_column = self.fieldIndex('name')
        for r in range(self.rowCount()):
            if self.data(self.index(r, id_column), Qt.DisplayRole) == index:
                return self.data(self.index(r, name_column), Qt.DisplayRole)
        return ''

    def get_colorstr_for_id(self, index):
        id_column = self.fieldIndex('id')
        color_column = self.fieldIndex('color')
        for r in range(self.rowCount()):
            if self.data(self.index(r, id_column), Qt.DisplayRole) == index:
                s = self.data(self.index(r, color_column), Qt.EditRole)
                print("color str:", s)
                return s
        print("no color str for", index)
        return ""

    def get_color_for_id(self, index):
        color = self.get_colorstr_for_id(index)
        if color != "":
            return QtGui.QColor(color)
        else:
            return QtGui.QColor()

    def get_labels(self):
        id_column = self.fieldIndex('id')
        name_column = self.fieldIndex('name')
        color_column = self.fieldIndex('color')
        label_column = self.fieldIndex('label')
        labels = list()
        for r in range(self.rowCount()):
            if self.data(self.index(r, label_column)) == 1:
                identifier = self.data(self.index(r, id_column))
                name = self.data(self.index(r, name_column))
                color = self.data(self.index(r, color_column))
                labels.append((identifier, name, color))
        return labels
