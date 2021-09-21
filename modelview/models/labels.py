from PyQt5.QtCore import Qt
import PyQt5.QtSql as QtSql


class LabelsTableModel(QtSql.QSqlTableModel):
    """
    A Model for the table of labels
    """
    def __init__(self):
        super(LabelsTableModel, self).__init__()
        self.setTable("labels")

    def get_labels_for_transaction(self, tr_index):
        cat_column = self.fieldIndex('category_id')
        tr_column = self.fieldIndex('transaction_id')
        labels = []
        for r in range(self.rowCount()):
            if self.data(self.index(r, tr_column), Qt.DisplayRole) == tr_index:
                labels.append(self.data(self.index(r, cat_column), Qt.DisplayRole))
        print("got link", tr_index, labels)
        return labels

    def update_link(self, tr_index, categories):
        print("update link:", tr_index, categories)
        cat_column = self.fieldIndex('category_id')
        tr_column = self.fieldIndex('transaction_id')
        to_link = categories.copy()
        # remove links that do not exist (start at the end)
        for r in reversed(range(self.rowCount())):
            if self.data(self.index(r, tr_column), Qt.DisplayRole) == tr_index:
                cat_index = self.data(self.index(r, cat_column), Qt.DisplayRole)
                if cat_index not in categories:
                    self.removeRow(r)
                else:
                    to_link.remove(cat_index)
        # add rows for new links
        if len(to_link) > 0:
            for offset, cat_index in enumerate(to_link):
                record = self.record()
                record.remove(record.indexOf('id'))
                record.setValue('category_id', cat_index)
                record.setValue('transaction_id', tr_index)
                self.insertRecord(-1, record)
