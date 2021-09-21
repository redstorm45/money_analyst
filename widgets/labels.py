#!/usr/bin/python3

import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt

from widgets.flow_layout import FlowLayout


class LabelWidget(Qtw.QLabel):
    """
    A widget displaying a single label, with it's color
    """
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent, identifier, name, color):
        super(LabelWidget, self).__init__(parent)
        self.color = QtGui.QColor(color)
        self.identifier = identifier
        self.setText(name+u" <strong>\x00\xd7</strong>")
        self.setStyleSheet("""
                           QLabel{{
                               border-radius: 5px;
                               border: 1px solid black;
                               background-color: {};
                           }}
                           """.format(color))

    def mousePressEvent(self, event):
        self.clicked.emit()


class NewLabelWidget(Qtw.QLineEdit):
    """
    A widget enabling adding a single label by typing in it
    """
    validate_new = QtCore.pyqtSignal(int)

    def __init__(self, parent, all_labels):
        super(NewLabelWidget, self).__init__(parent)
        self.all_labels = all_labels
        self.setStyleSheet("""
                           QLineEdit{{
                               border-radius: 5px;
                               border: 1px dashed grey;
                               background-color: #f5f5f5;
                           }}
                           """.format())
        self.propositions = NewLabelPropositionWidget(self, all_labels)
        self.propositions.validate_new.connect(lambda e: self.validate_new.emit(e))
        self.textChanged.connect(self.handle_change)
        self.editingFinished.connect(self.handle_editing_finished)

    def focusInEvent(self, event):
        print("show prop")
        self.propositions.show()
        self.propositions.move(self.mapToGlobal(QtCore.QPoint(0, self.height())))

    def focusOutEvent(self, event):
        print("hide prop")
        self.propositions.hide()

    def handle_change(self, text):
        self.propositions.set_search(text)

    def handle_editing_finished(self):
        pass


class NewLabelPropositionWidget(Qtw.QWidget):
    """
    A widget displaying propositions for labels,
    used as a drop-down help list when entering text in a NewLabelWidget
    """
    validate_new = QtCore.pyqtSignal(int)

    def __init__(self, parent, all_labels):
        super(NewLabelPropositionWidget, self).__init__(parent)
        self.all_labels = all_labels
        self.search_term = ""

        self.setWindowFlag(Qt.Widget)
        layout = Qtw.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setWindowFlag(Qt.Window + Qt.FramelessWindowHint + Qt.WindowDoesNotAcceptFocus)
        # self.setWindowModality(Qt.NonModal)

        self.setStyleSheet("""
                           QWidget{
                               border: 1px solid grey;
                               padding: 0;
                               margin 0;
                               background-color: #ffffff;
                           }
                           """)

        self.update_list()

    def set_search(self, text):
        """
        Update the propositions, by hiding those not matching the text
        """
        self.search_term = text
        self.update_list()

    def update_list(self):
        # clear sub-widgets
        while True:
            item = self.layout().takeAt(0)
            if item is None:
                break
            item.widget().setParent(None)
        # make the list of propositions, using the search term
        props = []
        if len(self.search_term) == 0:
            props = self.all_labels
        else:
            for label_id, name, color in self.all_labels:
                if self.search_term.lower() in name.lower():
                    props.append((label_id, name, color))
        # add the propositions
        for label_id, name, color in props:
            label = NewLabelDropdownEntry(self, name, color)
            label.clicked.connect(lambda ident=label_id: self.validate_new.emit(ident))
            self.layout().addWidget(label)
        # text to display if no label is available
        if len(props) == 0:
            label = Qtw.QLabel("Pas d'étiquette trouvée")
            label.setStyleSheet("""
                                QLabel{
                                    border: 0;
                                    margin: 0;
                                    background-color: #f5f5f5;
                                    color: #858585;
                                }
                                """)
            self.layout().addWidget(label)
        self.setFixedSize(self.sizeHint())


class NewLabelDropdownEntry(Qtw.QLabel):
    """
    A widget which is a single dropdown entry in the proposition widget,
    basically a colorable clickable label
    """
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent, text, color):
        super(NewLabelDropdownEntry, self).__init__(text, parent)
        self.setStyleSheet("""
                           QLabel{{
                               border: 0;
                               margin: 0;
                               background-color: {};
                               color: #020304;
                           }}
                           """.format(color))

    def mousePressEvent(self, event):
        self.clicked.emit()


class LabelsWidget(Qtw.QWidget):
    """
    A widget showing all the labels of a transaction
    """
    def __init__(self, parent, all_labels):
        super(LabelsWidget, self).__init__(parent)
        layout = FlowLayout(self)
        self.all_labels = all_labels
        self.labels = []
        self.setLayout(layout)
        self.update_labels()

    def add_label(self, identifier):
        print("added:", identifier)
        if identifier not in self.labels and identifier in [lb[0] for lb in self.all_labels]:
            self.labels.append(identifier)
            self.labels.sort()
            self.update_labels()

    def remove_label(self, identifier):
        print("removed:", identifier)
        if identifier in self.labels and identifier in [lb[0] for lb in self.all_labels]:
            self.labels.remove(identifier)
            self.labels.sort()
            self.update_labels()

    def set_labels(self, labels):
        self.labels = labels
        self.update_labels()

    def update_labels(self):
        # remove all previous labels (+ editor)
        while True:
            item = self.layout().takeAt(0)
            if item is None:
                break
            item.widget().setParent(None)

        # add all the labels
        for identifier, name, color in self.all_labels:
            if identifier in self.labels:
                label = LabelWidget(self, identifier, name, color)
                label.clicked.connect(lambda ident=identifier: self.remove_label(ident))
                self.layout().addWidget(label)

        # append the editor
        editor = NewLabelWidget(self, self.all_labels)
        editor.validate_new.connect(lambda e: self.add_label(e))
        self.layout().addWidget(editor)
