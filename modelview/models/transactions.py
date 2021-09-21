from PyQt5.QtCore import Qt
import PyQt5.QtSql as QtSql


class TransactionsTableModel(QtSql.QSqlTableModel):
    """
    A Model for the table of transactions
    """
    def __init__(self, model_cat, model_lab):
        super(TransactionsTableModel, self).__init__()
        self.model_cat = model_cat
        self.model_lab = model_lab
        self.setTable("transactions")

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and index.column() == self.fieldIndex('amount'):
            data = super(TransactionsTableModel, self).data(index)
            return str(data//100)+','+str(data%100).zfill(2)+'€'
        elif role == Qt.DisplayRole and index.column() == self.fieldIndex('category_id'):
            return self.model_cat.get_name_for_id(super(TransactionsTableModel, self).data(index))
        elif role == Qt.BackgroundColorRole and index.column() == self.fieldIndex('category_id'):
            return self.model_cat.get_color_for_id(super(TransactionsTableModel, self).data(index))
        return super(TransactionsTableModel, self).data(index, role)

    def get_qty_for_category(self, cat_id):
        cat_column = self.fieldIndex('category_id')
        N = 0
        for r in range(self.rowCount()):
            if super(TransactionsTableModel, self).data(self.index(r, cat_column)) == cat_id:
                N += 1
        return N

    def generate_all_transactions(self, filter_func=None):
        col_desc = self.fieldIndex('desc')
        col_category = self.fieldIndex('category_id')
        col_amount = self.fieldIndex('amount')
        col_date = self.fieldIndex('date')
        col_id = self.fieldIndex('id')
        for r in range(self.rowCount()):
            element = dict()
            element["desc"] = self.data(self.index(r, col_desc), Qt.EditRole)
            element["category_id"] = self.data(self.index(r, col_category), Qt.EditRole)
            element["amount"] = self.data(self.index(r, col_amount), Qt.EditRole)
            element["date"] = self.data(self.index(r, col_date), Qt.EditRole)
            element["id"] = self.data(self.index(r, col_id), Qt.EditRole)
            if filter_func is None or filter_func(element):
                yield element

    def remove_all_category(self, cat_id):
        cat_column = self.fieldIndex('category_id')
        done = True
        for r in range(self.rowCount())[::-1]:
            if super(TransactionsTableModel, self).data(self.index(r, cat_column)) == cat_id:
                done = done and self.removeRow(r)
        return done




